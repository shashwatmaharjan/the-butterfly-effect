# Import necessary libraries
import os
import numpy as np

# For solving the ODEs
from scipy.integrate import solve_ivp

# For the web app
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash

# Function to define the Lorenz ODEs
def lorenz_ode(t, state, sigma, rho, beta):
    
    # Unpack the state vector
    # These are the dependent variables
    x, y, z = state
    
    # Define the system of Lorenz ODEs
    dx_dt = sigma * (y - x)
    dy_dt = x * (rho - z) - y
    dz_dt = x * y - beta * z
    
    return [dx_dt, dy_dt, dz_dt]


# Function to solve the Lorenz ODEs
def solve_lorenz_ode(sigma, rho, beta, initial_state, t0, tf, dt):
    
    # Timepoints for the solution
    timepoints = np.arange(t0, tf, dt)
    
    # Solve the ODEs using solve_ivp
    solution = solve_ivp(lorenz_ode, [t0, tf], initial_state, args=(sigma, rho, beta), t_eval=timepoints)

    # Extract the solution components
    x, y, z = solution.y
    
    return x, y, z


# Function to plot the Lorenz ODEs time vs x, y, z
def plot_time_versus_xyz(solution_1, solution_2, timepoints, color_1, color_2, background_color, font_size, font_style, points_per_frame=40):
    
    # Get the lowest and highest values for the timepoints
    t_min = timepoints.min()
    t_max = timepoints.max()
    t_ticks = np.arange(t_min, t_max, 5)
    
    # Make the same y-axis regardless of the plot
    ordinate_min = min(solution_1.min(), solution_2.min())
    ordinate_max = max(solution_1.max(), solution_2.max())
    ordinate_ticks = np.arange(ordinate_min, ordinate_max+1, 6).astype(int)
    
    # Make subplots
    fig = make_subplots(rows=1, cols=3,
                        specs=[[{'type': 'xy'}, {'type': 'xy'}, {'type': 'xy'}]],
                        subplot_titles=('time (t) vs x(t)', 'time (t) vs y(t)', 'time (t) vs z(t)'))
    
    # Plot time vs x(t)
    fig.add_trace(go.Scatter(x=timepoints, y=solution_1[0], mode='lines', line=dict(color=color_1), name='time (t) vs x(t)', legendgroup='group_1', legendgrouptitle_text='Chaotic Path A'), row=1, col=1)
    fig.add_trace(go.Scatter(x=timepoints, y=solution_2[0], mode='lines', line=dict(color=color_2), name='time (t) vs x(t)', legendgroup='group_2', legendgrouptitle_text='Chaotic Path B'), row=1, col=1)
    
    # Plot time vs y(t)
    fig.add_trace(go.Scatter(x=timepoints, y=solution_1[1], mode='lines', line=dict(color=color_1), name='time (t) vs y(t)', legendgroup='group_1', legendgrouptitle_text='Chaotic Path A'), row=1, col=2)
    fig.add_trace(go.Scatter(x=timepoints, y=solution_2[1], mode='lines', line=dict(color=color_2), name='time (t) vs y(t)', legendgroup='group_2', legendgrouptitle_text='Chaotic Path B'), row=1, col=2)
    
    # Plot time vs z(t)
    fig.add_trace(go.Scatter(x=timepoints, y=solution_1[2], mode='lines', line=dict(color=color_1), name='time (t) vs z(t)', legendgroup='group_1', legendgrouptitle_text='Chaotic Path A'), row=1, col=3)
    fig.add_trace(go.Scatter(x=timepoints, y=solution_2[2], mode='lines', line=dict(color=color_2), name='time (t) vs z(t)', legendgroup='group_2', legendgrouptitle_text='Chaotic Path B'), row=1, col=3)
    
    # Create frames
    frames = []
    for n_frame in range(1, len(timepoints), points_per_frame):
        frame = go.Frame(data=[go.Scatter(x=timepoints[:n_frame+1], y=solution_1[0][:n_frame+1], mode='lines', line=dict(color=color_1)),
                               go.Scatter(x=timepoints[:n_frame+1], y=solution_2[0][:n_frame+1], mode='lines', line=dict(color=color_2)),
                               go.Scatter(x=timepoints[:n_frame+1], y=solution_1[1][:n_frame+1], mode='lines', line=dict(color=color_1)),
                               go.Scatter(x=timepoints[:n_frame+1], y=solution_2[1][:n_frame+1], mode='lines', line=dict(color=color_2)),
                               go.Scatter(x=timepoints[:n_frame+1], y=solution_1[2][:n_frame+1], mode='lines', line=dict(color=color_1)),
                               go.Scatter(x=timepoints[:n_frame+1], y=solution_2[2][:n_frame+1], mode='lines', line=dict(color=color_2))])
        frames.append(frame)
        
    # Update layout to remove grid and add animation controls
    fig.update_layout(
        xaxis=dict(showgrid=False, title='time(t)', title_font=dict(size=font_size), tickfont=dict(size=font_size), tickvals=t_ticks),
        yaxis=dict(showgrid=False, title='x(t)', title_font=dict(size=font_size), tickfont=dict(size=font_size), tickvals=ordinate_ticks, range=[ordinate_min, ordinate_max]),
        xaxis2=dict(showgrid=False, title='time(t)', title_font=dict(size=font_size), tickfont=dict(size=font_size), tickvals=t_ticks),
        yaxis2=dict(showgrid=False, title='y(t)', title_font=dict(size=font_size), tickfont=dict(size=font_size), tickvals=ordinate_ticks, range=[ordinate_min, ordinate_max]),
        xaxis3=dict(showgrid=False, title='time(t)', title_font=dict(size=font_size), tickfont=dict(size=font_size), tickvals=t_ticks),
        yaxis3=dict(showgrid=False, title='z(t)', title_font=dict(size=font_size), tickfont=dict(size=font_size), tickvals=ordinate_ticks, range=[ordinate_min, ordinate_max]),
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.2,
            xanchor="center",
            x=0.5,
            font=dict(size=font_size)),
        font=font_style,
        updatemenus=[dict(type='buttons', buttons=[dict(label='Animate',
                                                         method='animate',
                                                         args=[None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}])])],
    )
    
    fig.frames = frames
    
    return fig
    

# Function to plot the Lorenz ODEs x, y, z against each other
def plot_xyz(solution_1, solution_2, color_1, color_2, background_color, font_size, font_style, points_per_frame=15):
    
    # Specify spacing for the ticks
    tick_spacing = 5
    
    # Make uniform axis for all plots
    # x-axis
    x_value_min = min(solution_1[0].min(), solution_2[0].min()) - 2
    x_value_max = max(solution_1[0].max(), solution_2[0].max()) + 2
    x_value_ticks = np.arange(x_value_min, x_value_max, tick_spacing).astype(int)
    
    # y-axis
    y_value_min = min(solution_1[1].min(), solution_2[1].min()) - 2
    y_value_max = max(solution_1[1].max(), solution_2[1].max()) + 2
    y_value_ticks = np.arange(y_value_min, y_value_max, tick_spacing).astype(int)
    
    # z-axis
    z_value_min = min(solution_1[2].min(), solution_2[2].min()) - 2
    z_value_max = max(solution_1[2].max(), solution_2[2].max()) + 2
    z_value_ticks = np.arange(z_value_min, z_value_max, tick_spacing).astype(int)
    
    # Make subplots
    fig = make_subplots(rows=1, cols=3,
                        specs=[[{'type': 'xy'}, {'type': 'xy'}, {'type': 'xy'}],],
                        subplot_titles=('x(t) vs y(t)', 'x(t) vs z(t)', 'y(t) vs z(t)'))
    
    # Plot x(t) vs y(t)
    fig.add_trace(go.Scatter(x=solution_1[0], y=solution_1[1], mode='lines', line=dict(color=color_1), name='x(t) vs y(t)', legendgroup='group_1', legendgrouptitle_text='Chaotic Path A'), row=1, col=1)
    fig.add_trace(go.Scatter(x=solution_2[0], y=solution_2[1], mode='lines', line=dict(color=color_2), name='x(t) vs y(t)', legendgroup='group_2', legendgrouptitle_text='Chaotic Path B'), row=1, col=1)
    
    # Plot x(t) vs z(t)
    fig.add_trace(go.Scatter(x=solution_1[0], y=solution_1[2], mode='lines', line=dict(color=color_1), name='x(t) vs z(t)', legendgroup='group_1', legendgrouptitle_text='Chaotic Path A'), row=1, col=2)
    fig.add_trace(go.Scatter(x=solution_2[0], y=solution_2[2], mode='lines', line=dict(color=color_2), name='x(t) vs z(t)', legendgroup='group_2', legendgrouptitle_text='Chaotic Path B'), row=1, col=2)
    
    # Plot y(t) vs z(t)
    fig.add_trace(go.Scatter(x=solution_1[1], y=solution_1[2], mode='lines', line=dict(color=color_1), name='y(t) vs z(t)', legendgroup='group_1', legendgrouptitle_text='Chaotic Path A'), row=1, col=3)
    fig.add_trace(go.Scatter(x=solution_2[1], y=solution_2[2], mode='lines', line=dict(color=color_2), name='y(t) vs z(t)', legendgroup='group_2', legendgrouptitle_text='Chaotic Path B'), row=1, col=3)
    
    # Create frames
    frames = []
    for n_frame in range(1, len(solution_1[0]), points_per_frame):
        
        frame = go.Frame(data=[go.Scatter(x=solution_1[0][:n_frame+1], y=solution_1[1][:n_frame+1], mode='lines', line=dict(color=color_1)),
                               go.Scatter(x=solution_2[0][:n_frame+1], y=solution_2[1][:n_frame+1], mode='lines', line=dict(color=color_2)),
                               go.Scatter(x=solution_1[0][:n_frame+1], y=solution_1[2][:n_frame+1], mode='lines', line=dict(color=color_1)),
                               go.Scatter(x=solution_2[0][:n_frame+1], y=solution_2[2][:n_frame+1], mode='lines', line=dict(color=color_2)),
                               go.Scatter(x=solution_1[1][:n_frame+1], y=solution_1[2][:n_frame+1], mode='lines', line=dict(color=color_1)),
                               go.Scatter(x=solution_2[1][:n_frame+1], y=solution_2[2][:n_frame+1], mode='lines', line=dict(color=color_2))])
        frames.append(frame)
    
    # Update layout to remove grid
    fig.update_layout(
        xaxis=dict(showgrid=False, title='x(t)', title_font=dict(size=font_size), tickfont=dict(size=font_size), tickvals=x_value_ticks, range=[x_value_min, x_value_max]),
        yaxis=dict(showgrid=False, title='y(t)', title_font=dict(size=font_size), tickfont=dict(size=font_size), tickvals=y_value_ticks, range=[y_value_min, y_value_max]),
        xaxis2=dict(showgrid=False, title='x(t)', title_font=dict(size=font_size), tickfont=dict(size=font_size), tickvals=x_value_ticks, range=[x_value_min, x_value_max]),
        yaxis2=dict(showgrid=False, title='z(t)', title_font=dict(size=font_size), tickfont=dict(size=font_size), tickvals=z_value_ticks, range=[z_value_min, z_value_max]),
        xaxis3=dict(showgrid=False, title='y(t)', title_font=dict(size=font_size), tickfont=dict(size=font_size), tickvals=y_value_ticks, range=[y_value_min, y_value_max]),
        yaxis3=dict(showgrid=False, title='z(t)', title_font=dict(size=font_size), tickfont=dict(size=font_size), tickvals=z_value_ticks, range=[z_value_min, z_value_max]),
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.2,
            xanchor="center",
            x=0.5,
            font=dict(size=font_size)),
        font=font_style,
        updatemenus=[dict(type='buttons', buttons=[dict(label='Animate',
                                                         method='animate',
                                                         args=[None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}])])],
    )
    
    fig.frames = frames
    
    return fig
    

# Function to plot the Lorenz ODEs in 3D
def plot_3d(solution_1, solution_2, color_1, color_2, background_color, font_size, font_style, points_per_frame=10):
    
    # Specify spacing for the ticks
    tick_spacing = 7
    
    # Make uniform axis for all plots
    # x-axis
    x_value_min = min(solution_1[0].min(), solution_2[0].min()) - 2
    x_value_max = max(solution_1[0].max(), solution_2[0].max()) + 2
    x_value_ticks = np.arange(x_value_min, x_value_max, tick_spacing).astype(int)
    
    # y-axis
    y_value_min = min(solution_1[1].min(), solution_2[1].min()) - 2
    y_value_max = max(solution_1[1].max(), solution_2[1].max()) + 2
    y_value_ticks = np.arange(y_value_min, y_value_max, tick_spacing).astype(int)
    
    # z-axis
    z_value_min = min(solution_1[2].min(), solution_2[2].min()) - 2
    z_value_max = max(solution_1[2].max(), solution_2[2].max()) + 2
    z_value_ticks = np.arange(z_value_min, z_value_max, tick_spacing).astype(int)
    
    # Make subplots
    fig = make_subplots(rows=1, cols=1,
                        specs=[[{'type': 'scatter3d'}],],)
    
    # Plot x(t) vs y(t) vs z(t)
    fig.add_trace(go.Scatter3d(x=solution_1[0], y=solution_1[1], z=solution_1[2], mode='lines', line=dict(color=color_1), name='Chaotic Path A'), row=1, col=1)
    fig.add_trace(go.Scatter3d(x=solution_2[0], y=solution_2[1], z=solution_2[2], mode='lines', line=dict(color=color_2), name='Chaotic Path B'), row=1, col=1)
    
    # Create frames
    frames = []
    for n_frame in range(1, len(solution_1[0]), points_per_frame):
        
        frame = go.Frame(data=[go.Scatter3d(x=solution_1[0][:n_frame+1], y=solution_1[1][:n_frame+1], z=solution_1[2][:n_frame+1], mode='lines', line=dict(color=color_1)),
                               go.Scatter3d(x=solution_2[0][:n_frame+1], y=solution_2[1][:n_frame+1], z=solution_2[2][:n_frame+1], mode='lines', line=dict(color=color_2))])
        frames.append(frame)
    
    # Update layout to remove grid
    fig.update_layout(
        scene=dict(
            xaxis=dict(showgrid=False, showbackground=False, title='x(t)', title_font=dict(size=font_size), tickfont=dict(size=font_size-2), tickvals=x_value_ticks, range=[x_value_min, x_value_max]),
            yaxis=dict(showgrid=False, showbackground=False, title='y(t)', title_font=dict(size=font_size), tickfont=dict(size=font_size-2), tickvals=y_value_ticks, range=[y_value_min, y_value_max]),
            zaxis=dict(showgrid=False, showbackground=False, title='z(t)', title_font=dict(size=font_size), tickfont=dict(size=font_size-2), tickvals=z_value_ticks, range=[z_value_min, z_value_max]),
            
            camera=dict(up=dict(x=0, y=0, z=1), # Keeps the z-axis pointing up
                        center=dict(x=0, y=0, z=0), # Set rotation center
                        eye=dict(x=4, y=1.5, z=1.5), # Set the initial viewing angle
                        projection=dict(type='orthographic'), # Set the projection type
                        ),
            ),
                        
        plot_bgcolor=background_color,
        paper_bgcolor=background_color,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.85,
            xanchor="center",
            x=0.5,
            font=dict(size=font_size),),
        font=font_style,
        margin=dict(l=0, r=0, t=0, b=0),  # Adjust margins
        scene_aspectmode='cube',  # Make the plot aspect uniform,
        updatemenus=[dict(type='buttons', buttons=[dict(label='Animate',
                                                         method='animate',
                                                         args=[None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}])])],
    )
        
    fig.frames = frames
    
    return fig


# Main function
def main():
    
    # Timepoints
    t0 = 0
    tf = 21
    dt = 0.01
    timepoints = np.arange(t0, tf, dt)
    
    # First initial state
    default_initial_state_1 = [0, 1, 0] # x0_1, y0_1, z0_1
    
    # Define constants 
    default_sigma_1 = 10
    default_rho_1 = 28
    default_beta_1 = 2.3
    
    # Solve the ODEs
    solution_1 = solve_lorenz_ode(default_sigma_1, default_rho_1, default_beta_1, default_initial_state_1, t0, tf, dt) # x1, y1, z1
    
    # Convert the solution to a numpy array
    solution_1 = np.array(solution_1)
    
    # Second initial state
    default_initial_state_2 = [1, 0, 1] # x0_2, y0_2, z0_2
    
    # Define constants 
    default_sigma_2 = 10
    default_rho_2 = 28
    default_beta_2 = 2.3
    
    # Solve the ODEs
    solution_2 = solve_lorenz_ode(default_sigma_2, default_rho_2, default_beta_2, default_initial_state_2, t0, tf, dt) # x2, y2, z2
    
    # Convert the solution to a numpy array
    solution_2 = np.array(solution_2)
    
    # Define colors
    dashboard_background_color = '#f0f5f9'
    plot_color_1 = '#0000FF' # blue
    plot_color_2 = '#FFA500' # orange
    
    # Define common styles for font
    font_style = {'family': 'Courier New, Courier, monospace'}
    font_size_inputs = '18px'
    font_size_plots = 15
    
    # Plot of time vs x, y, z
    fig1 = plot_time_versus_xyz(solution_1, solution_2, timepoints, plot_color_1, plot_color_2, dashboard_background_color, font_size_plots, font_style)
    
    # Plot of x, y, z against each other
    fig2 = plot_xyz(solution_1, solution_2, plot_color_1, plot_color_2, dashboard_background_color, font_size_plots, font_style)
    
    # Plot of x, y, z in 3D
    fig3 = plot_3d(solution_1, solution_2, plot_color_1, plot_color_2, dashboard_background_color, font_size_plots, font_style)
    
    # Define the default border radius
    border_radius = '2px'
    
    # Create the Dash app
    app = Dash(__name__)
    
    app.layout = html.Div([
        
        # Title
        html.H1(id='title',
                children='The Butterfly Effect',
                style={'textAlign': 'center',
                       'font-family': font_style['family'],}),
        
        html.H2(id='sub-title',
                children='Try changing the initial conditions and see how the trajectories diverge.',
                style={'textAlign': 'center',
                       'font-family': font_style['family'],}),
        
        # Horizontal line
        html.Hr(),
                    
        # Container for the two columns for the initial conditions
        html.Div([
            # Left column
            # Initial condition 1
            html.Div([
                html.H3(id='ic-1',
                        children='Initial Position 1',
                        style={'textAlign': 'center',
                               'font-family': font_style['family'],
                                'color': plot_color_1}),
                        
                html.Div([html.Div(['x: ', dcc.Input(id='x0_1', type = 'number', value = default_initial_state_1[0], min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                   'text-align': 'center',
                                                                                                                                   'font-family': font_style['family'],
                                                                                                                                   'border-radius': border_radius,
                                                                                                                                   'font-size': font_size_inputs}),]),
                        html.Div(['y: ', dcc.Input(id='y0_1', type = 'number', value = default_initial_state_1[1], min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                 'text-align': 'center',
                                                                                                                                 'font-family': font_style['family'],
                                                                                                                                 'border-radius': border_radius,
                                                                                                                                 'font-size': font_size_inputs}),]),
                        html.Div(['z: ', dcc.Input(id='z0_1', type = 'number', value = default_initial_state_1[2], min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                 'text-align': 'center',
                                                                                                                                 'font-family': font_style['family'],
                                                                                                                                 'border-radius': border_radius,
                                                                                                                                 'font-size': font_size_inputs}),]),],
                        
                        style={'display': 'flex',
                               'justify-content': 'center',
                               'gap': '20px',
                               'font-family': font_style['family']}),
                
                    html.H3(children='Sigma (σ)',
                            style={'textAlign': 'center',
                                   'font-family': font_style['family'],
                                    'color': plot_color_1}),
                    
                    html.Div([html.Div([dcc.Slider(id='sigma-1', min=7, max=12, step=1,
                                                   value=default_sigma_1,
                                                   marks={tick: {'label': str(tick), 'style': {'font-size': '16px'}} for tick in range(7, 13)})]),
                
                    html.H3(children='Rho (ρ)',
                            style={'textAlign': 'center',
                                   'font-family': font_style['family'],
                                   'color': plot_color_1}),
                    
                    html.Div([html.Div([dcc.Slider(id='rho-1', min=27, max=32, step=1,
                                                   value=default_rho_1,
                                                   marks={tick: {'label': str(tick), 'style': {'font-size': '16px'}} for tick in range(27, 33)}),]),]),
                    
                    html.H3(children='Beta (β)',
                            style={'textAlign': 'center',
                                   'font-family': font_style['family'],
                                   'color': plot_color_1}),
                    
                    html.Div([html.Div([dcc.Slider(id='beta-1', min=2, max=2.5, step=0.1,
                                                   value=default_beta_1,
                                                   marks={tick: {'label': str(tick), 'style': {'font-size': font_size_inputs}} for tick in [2, 2.1, 2.2, 2.3, 2.4, 2.5]})]),])
                              
                    ]) 
                
                ], style={'width': '50%',
                          'padding': '20px'}),
            
            # Right column
            # Initial condition 2
            html.Div([
                html.H3(id='ic-2',
                        children='Initial Position 2',
                        style={'textAlign': 'center',
                               'font-family': font_style['family'],
                               'color': plot_color_2}),
                        
                html.Div([html.Div(['x: ', dcc.Input(id='x0_2', type = 'number', value = default_initial_state_2[0], min=-10, max=10, required=True,  style={'width': '40px',
                                                                                                                                    'text-align': 'center',
                                                                                                                                   'font-family': font_style['family'],
                                                                                                                                   'border-radius': border_radius,
                                                                                                                                   'font-size': font_size_inputs}),]),
                        html.Div(['y: ', dcc.Input(id='y0_2', type = 'number', value = default_initial_state_2[1], min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                 'text-align': 'center',
                                                                                                                                 'font-family': font_style['family'],
                                                                                                                                 'border-radius': border_radius,
                                                                                                                                 'font-size': font_size_inputs}),]),
                        html.Div(['z: ', dcc.Input(id='z0_2', type = 'number', value = default_initial_state_2[2], min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                 'text-align': 'center',
                                                                                                                                 'font-family': font_style['family'],
                                                                                                                                 'border-radius': border_radius,
                                                                                                                                 'font-size': font_size_inputs}),]),],
                        
                        style={'display': 'flex',
                               'justify-content': 'center',
                               'gap': '20px',
                               'font-family': font_style['family']}), 
                
                    html.H3(children='Sigma (σ)',
                            style={'textAlign': 'center',
                                   'font-family': font_style['family'],
                                   'color': plot_color_2}),
                    
                    html.Div([html.Div([dcc.Slider(id='sigma-2', min=7, max=12, step=1,
                                                   value=default_sigma_2,
                                                   marks={tick: {'label': str(tick), 'style': {'font-size': '16px'}} for tick in range(7, 13)})]),
                
                    html.H3(children='Rho (ρ)',
                            style={'textAlign': 'center',
                                   'font-family': font_style['family'],
                                   'color': plot_color_2}),
                    
                    html.Div([html.Div([dcc.Slider(id='rho-2', min=27, max=32, step=1,
                                                   value=default_rho_2,
                                                   marks={tick: {'label': str(tick), 'style': {'font-size': '16px'}} for tick in range(27, 33)})]),]),
                    
                    html.H3(children='Beta (β)',
                            style={'textAlign': 'center',
                                   'font-family': font_style['family'],
                                   'color': plot_color_2}),
                    
                    html.Div([html.Div([dcc.Slider(id='beta-2',min=2, max=2.5, step=0.1,
                                                   value=default_beta_2,
                                                   marks={n_tick: {'label': str(n_tick), 'style': {'font-size': font_size_inputs}} for n_tick in [2, 2.1, 2.2, 2.3, 2.4, 2.5]})]),])
                    ]) 
                
                ], style={'width': '50%',
                          'padding': '20px'}),
            
            ], style={'display': 'flex',
                    'justify-content': 'space-between',
                    'width': '100%',}),
        
        # Visualize button
        html.Div([html.Button(id='visualize-button', children='Generate', n_clicks = 0, style={'display': 'block',
                                                                                               'background-color': '#4CAF50',
                                                                                               'color': 'white',
                                                                                               'border': 'none',
                                                                                               'border-radius': border_radius,
                                                                                               'cursor': 'pointer',
                                                                                               'text-align': 'center',
                                                                                               'padding': '5px 10px',
                                                                                               'font-family': font_style['family'],
                                                                                               'font-size': '25px',
                                                                                               'margin-right': '10px'},),
                  
                  html.Button(id='reset-button', children='Reset', n_clicks = 0, style={'display': 'block',
                                                                                        'background-color': '#FF8DA1',
                                                                                        'color': 'white',
                                                                                        'border': 'none',
                                                                                        'border-radius': border_radius,
                                                                                        'cursor': 'pointer',
                                                                                        'text-align': 'center',
                                                                                        'padding': '5px 10px',
                                                                                        'font-family': font_style['family'],
                                                                                        'font-size': '25px',
                                                                                        'margin-left': '10px',
                                                                                        'margin-right': '10px'},),
                  ],
                 style={'display': 'flex',
                        'justify-content':'center',
                        'padding': '5px'}),
        
        # Horizontal line
        html.Hr(),
        
        # Container for the plots
        # Plot of time vs x, y, z
        html.Div([
            dcc.Graph(id='fig1',
                      figure=fig1,
                      style={'width': '100%',},
                      config={'scrollZoom': False, 'displayModeBar': True, 'displaylogo': False}
                      )
            ],
            
            style={'width': '100%',
                   'background-color': dashboard_background_color,
                   'margin': '0 auto',}
        ),
        
        # Create a container for the animate button
        html.Div([html.Button(id='fig1-animate-button', children='Animate', n_clicks = 0, style={'display': 'block',
                                                                                        'background-color': '#964B00',
                                                                                        'color': 'white',
                                                                                        'border': 'none',
                                                                                        'border-radius': border_radius,
                                                                                        'cursor': 'pointer',
                                                                                        'text-align': 'center',
                                                                                        'padding': '5px 10px',
                                                                                        'font-family': font_style['family'],
                                                                                        'font-size': '25px',
                                                                                        'margin-left': '10px'},),],
                 style={'display': 'flex',
                        'justify-content':'center',
                        'padding': '5px'}),
        
        # Plot of x, y, z against each other
        html.Div([
            dcc.Graph(id='fig2',
                      figure=fig2,
                      style={'width': '100%',},
                      config={'scrollZoom': False, 'displayModeBar': True, 'displaylogo': False}
                      )
            ],
            
            style={'width': '100%',
                   'background-color': dashboard_background_color,
                   'margin': '0 auto',}
        ),
        
        # Create a container for the animate button
        html.Div([html.Button(id='fig2-animate-button', children='Animate', n_clicks = 0, style={'display': 'block',
                                                                                        'background-color': '#964B00',
                                                                                        'color': 'white',
                                                                                        'border': 'none',
                                                                                        'border-radius': border_radius,
                                                                                        'cursor': 'pointer',
                                                                                        'text-align': 'center',
                                                                                        'padding': '5px 10px',
                                                                                        'font-family': font_style['family'],
                                                                                        'font-size': '25px',
                                                                                        'margin-left': '10px'},),],
                 style={'display': 'flex',
                        'justify-content':'center',
                        'padding': '5px'}),
        
        # Plot of x, y, z in 3D
        html.Div([
            dcc.Graph(id='fig3',
                      figure=fig3,
                      style={'width': '100%',
                             'height': '100vh'},
                      config={'scrollZoom': False, 'displayModeBar': True, 'displaylogo': False}
                      )
            ],
            
            style={'width': '100%',
                   'background-color': dashboard_background_color,
                   'margin': '0 auto',}
        ),
        
        # Create a container for the animate button
        html.Div([html.Button(id='fig3-animate-button', children='Animate', n_clicks = 0, style={'display': 'block',
                                                                                        'background-color': '#964B00',
                                                                                        'color': 'white',
                                                                                        'border': 'none',
                                                                                        'border-radius': border_radius,
                                                                                        'cursor': 'pointer',
                                                                                        'text-align': 'center',
                                                                                        'padding': '5px 10px',
                                                                                        'font-family': font_style['family'],
                                                                                        'font-size': '25px',
                                                                                        'margin-left': '10px'},),],
                 style={'display': 'flex',
                        'justify-content':'center',
                        'padding': '5px'}),
        
        ], style={'background-color': dashboard_background_color,
                  'min-height': '100vh'})
    
    # Add callbacks to reset the values to default
    @app.callback(
        [Output('x0_1', 'value'),
         Output('y0_1', 'value'),
         Output('z0_1', 'value'),
         Output('x0_2', 'value'),
         Output('y0_2', 'value'),
         Output('z0_2', 'value'),
         
         Output('sigma-1', 'value'),
         Output('rho-1', 'value'),
         Output('beta-1', 'value'),
         Output('sigma-2', 'value'),
         Output('rho-2', 'value'),
         Output('beta-2', 'value')],
        
        [Input('reset-button', 'n_clicks')],
        
        [State('x0_1', 'value'),
         State('y0_1', 'value'),
         State('z0_1', 'value'),
         State('x0_2', 'value'),
         State('y0_2', 'value'),
         State('z0_2', 'value'),
         
         State('sigma-1', 'value'),
         State('rho-1', 'value'),
         State('beta-1', 'value'),
         State('sigma-2', 'value'),
         State('rho-2', 'value'),
         State('beta-2', 'value')])
    
    # Function to reset the values
    def reset_values(n_clicks, x0_1, y0_1, z0_1, x0_2, y0_2, z0_2, sigma_1, rho_1, beta_1, sigma_2, rho_2, beta_2):
        
        if n_clicks > 0:
            return default_initial_state_1[0], default_initial_state_1[1], default_initial_state_1[2], default_initial_state_2[0], default_initial_state_2[1], default_initial_state_2[2], default_sigma_1, default_rho_1, default_beta_1, default_sigma_2, default_rho_2, default_beta_2
        
        return x0_1, y0_1, z0_1, x0_2, y0_2, z0_2, sigma_1, rho_1, beta_1, sigma_2, rho_2, beta_2
    
    # Add callbacks to update the plots when 'Generate' button is clicked
    @app.callback(
        [Output('fig1', 'figure'),
         Output('fig2', 'figure'),
         Output('fig3', 'figure')],
        
        [Input('visualize-button', 'n_clicks')],
        
        [State('x0_1', 'value'),
         State('y0_1', 'value'),
         State('z0_1', 'value'),
         State('x0_2', 'value'),
         State('y0_2', 'value'),
         State('z0_2', 'value'),
         
         State('sigma-1', 'value'),
         State('rho-1', 'value'),
         State('beta-1', 'value'),
         State('sigma-2', 'value'),
         State('rho-2', 'value'),
         State('beta-2', 'value')])
    
    def update_plots(n_clicks, x0_1, y0_1, z0_1, x0_2, y0_2, z0_2, sigma_1, rho_1, beta_1, sigma_2, rho_2, beta_2):
        
        # Solve the ODEs
        solution_1 = solve_lorenz_ode(sigma_1, rho_1, beta_1, [x0_1, y0_1, z0_1], t0, tf, dt)
        solution_2 = solve_lorenz_ode(sigma_2, rho_2, beta_2, [x0_2, y0_2, z0_2], t0, tf, dt)
        
        # Convert the solution to a numpy array
        solution_1 = np.array(solution_1)
        solution_2 = np.array(solution_2)
        
        # Plot of time vs x, y, z
        fig1 = plot_time_versus_xyz(solution_1, solution_2, timepoints, plot_color_1, plot_color_2, dashboard_background_color, font_size_plots, font_style)
        
        # Plot of x, y, z against each other
        fig2 = plot_xyz(solution_1, solution_2, plot_color_1, plot_color_2, dashboard_background_color, font_size_plots, font_style)
        
        # Plot of x, y, z in 3D
        fig3 = plot_3d(solution_1, solution_2, plot_color_1, plot_color_2, dashboard_background_color, font_size_plots, font_style)
        
        return fig1, fig2, fig3
                
    return app


if __name__ == '__main__':
    
    # Call the main function
    app = main()
    
    # Run the app server
    app.run_server(debug=True)
    
    # Clear the console regardless of the OS
    os.system('cls' if os.name == 'nt' else 'clear')