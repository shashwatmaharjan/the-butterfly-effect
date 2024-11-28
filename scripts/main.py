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
def plot_time_versus_xyz(solution_1, solution_2, timepoints, color_1, color_2):
    
    # Make subplots
    fig = make_subplots(rows=1, cols=3,
                        specs=[[{'type': 'xy'}, {'type': 'xy'}, {'type': 'xy'}],],
                        subplot_titles=('time (t) vs x(t)', 'time (t) vs y(t)', 'time (t) vs z(t)'))
    
    # Plot time vs x(t)
    fig.add_trace(go.Scatter(x=timepoints, y=solution_1[0], mode='lines', line=dict(color=color_1)), row=1, col=1)
    fig.add_trace(go.Scatter(x=timepoints, y=solution_2[1], mode='lines', line=dict(color=color_2)), row=1, col=1)
    
    # Plot time vs y(t)
    fig.add_trace(go.Scatter(x=timepoints, y=solution_1[1], mode='lines', line=dict(color=color_1)), row=1, col=2)
    fig.add_trace(go.Scatter(x=timepoints, y=solution_2[1], mode='lines', line=dict(color=color_2)), row=1, col=2)
    
    # Plot time vs z(t)
    fig.add_trace(go.Scatter(x=timepoints, y=solution_1[2], mode='lines', line=dict(color=color_1)), row=1, col=3)
    fig.add_trace(go.Scatter(x=timepoints, y=solution_2[1], mode='lines', line=dict(color=color_2)), row=1, col=3)
    
    return fig
    

# Function to plot the Lorenz ODEs x, y, z against each other
def plot_xyz(solution_1, solution_2, color_1, color_2):
    
    # Make subplots
    fig = make_subplots(rows=1, cols=3,
                        specs=[[{'type': 'xy'}, {'type': 'xy'}, {'type': 'xy'}],],
                        subplot_titles=('x(t) vs y(t)', 'y(t) vs z(t)', 'z(t) vs x(t)'))
    
    # Plot x(t) vs y(t)
    fig.add_trace(go.Scatter(x=solution_1[0], y=solution_1[1], mode='lines', line=dict(color=color_1)), row=1, col=1)
    fig.add_trace(go.Scatter(x=solution_2[0], y=solution_2[1], mode='lines', line=dict(color=color_2)), row=1, col=1)
    
    # Plot y(t) vs z(t)
    fig.add_trace(go.Scatter(x=solution_1[1], y=solution_1[2], mode='lines', line=dict(color=color_1)), row=1, col=2)
    fig.add_trace(go.Scatter(x=solution_2[1], y=solution_2[2], mode='lines', line=dict(color=color_2)), row=1, col=2)
    
    # Plot z(t) vs x(t)
    fig.add_trace(go.Scatter(x=solution_1[2], y=solution_1[0], mode='lines', line=dict(color=color_1)), row=1, col=3)
    fig.add_trace(go.Scatter(x=solution_2[2], y=solution_2[0], mode='lines', line=dict(color=color_2)), row=1, col=3)
    
    return fig
    

# Function to plot the Lorenz ODEs in 3D
def plot_3d(solution_1, solution_2, color_1, color_2):
    
    # Make subplots
    fig = make_subplots(rows=1, cols=1,
                        specs=[[{'type': 'scatter3d'}],],
                        subplot_titles=('x(t) vs y(t) vs z(t)'))
    
    # Plot x(t) vs y(t) vs z(t)
    fig.add_trace(go.Scatter3d(x=solution_1[0], y=solution_1[1], z=solution_1[2], mode='lines', line=dict(color=color_1)), row=1, col=1)
    fig.add_trace(go.Scatter3d(x=solution_2[0], y=solution_2[1], z=solution_2[2], mode='lines', line=dict(color=color_2)), row=1, col=1)
    
    return fig


# Main function
def main():
    
    # Define constants 
    default_sigma = 10
    default_rho = 28
    default_beta = 2.3
    
    # Timepoints
    t0 = 0
    tf = 50
    dt = 0.01
    timepoints = np.arange(t0, tf, dt)
    
    # First initial state
    default_initial_state_1 = [0, 1, 0] # x0_1, y0_1, z0_1
    solution_1 = solve_lorenz_ode(default_sigma, default_rho, default_beta, default_initial_state_1, t0, tf, dt) # x1, y1, z1
    
    # Second initial state
    default_initial_state_2 = [1, 0, 1] # x0_2, y0_2, z0_2
    solution_2 = solve_lorenz_ode(default_sigma, default_rho, default_beta, default_initial_state_2, t0, tf, dt) # x2, y2, z2
    
    # Define common styles for font
    font_style = {'family': 'Courier New, Courier, monospace'}
    
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
                                                                                        'background-color': '#0000FF',
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
                    
        # Container for the two columns for the initial conditions
        html.Div([
            # Left column
            # Initial condition 1
            html.Div([
                html.H3(id='ic-1',
                        children='Initial Position 1',
                        style={'textAlign': 'center',
                               'font-family': font_style['family'],}),
                        
                html.Div([html.Div(['x: ', dcc.Input(id='x0_1', type = 'number', value = default_initial_state_1[0], min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                   'text-align': 'center',
                                                                                                                                   'font-family': font_style['family'],
                                                                                                                                   'border-radius': border_radius}),]),
                        html.Div(['y: ', dcc.Input(id='y0_1', type = 'number', value = default_initial_state_1[1], min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                 'text-align': 'center',
                                                                                                                                 'font-family': font_style['family'],
                                                                                                                                 'border-radius': border_radius}),]),
                        html.Div(['z: ', dcc.Input(id='z0_1', type = 'number', value = default_initial_state_1[2], min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                 'text-align': 'center',
                                                                                                                                 'font-family': font_style['family'],
                                                                                                                                 'border-radius': border_radius}),]),],
                        
                        style={'display': 'flex',
                               'justify-content': 'center',
                               'gap': '20px',
                               'font-family': font_style['family']}),
                
                    html.H3(children='Sigma (σ)',
                            style={'textAlign': 'center',
                                   'font-family': font_style['family'],}),
                    
                    html.Div([html.Div([dcc.Slider(id='sigma-1', min=7, max=12, step=1,
                                                   value=default_sigma)]),
                
                    html.H3(children='Rho (ρ)',
                            style={'textAlign': 'center',
                                   'font-family': font_style['family'],}),
                    
                    html.Div([html.Div([dcc.Slider(id='rho-1', min=27, max=32, step=1,
                                                   value=default_rho)]),]),
                    
                    html.H3(children='Beta (β)',
                            style={'textAlign': 'center',
                                   'font-family': font_style['family'],}),
                    
                    html.Div([html.Div([dcc.Slider(id='beta-1', min=2, max=2.5, step=0.1,
                                                   value=default_beta)]),])
                              
                    ]) 
                
                ], style={'width': '50%',
                          'padding': '20px'}),
            
            # Right column
            # Initial condition 2
            html.Div([
                html.H3(id='ic-2',
                        children='Initial Position 2',
                        style={'textAlign': 'center',
                               'font-family': font_style['family'],}),
                        
                html.Div([html.Div(['x: ', dcc.Input(id='x0_2', type = 'number', value = default_initial_state_2[0], min=-10, max=10, required=True,  style={'width': '40px',
                                                                                                                                    'text-align': 'center',
                                                                                                                                   'font-family': font_style['family'],
                                                                                                                                   'border-radius': border_radius}),]),
                        html.Div(['y: ', dcc.Input(id='y0_2', type = 'number', value = default_initial_state_2[1], min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                 'text-align': 'center',
                                                                                                                                 'font-family': font_style['family'],
                                                                                                                                 'border-radius': border_radius}),]),
                        html.Div(['z: ', dcc.Input(id='z0_2', type = 'number', value = default_initial_state_2[2], min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                 'text-align': 'center',
                                                                                                                                 'font-family': font_style['family'],
                                                                                                                                 'border-radius': border_radius}),]),],
                        
                        style={'display': 'flex',
                               'justify-content': 'center',
                               'gap': '20px',
                               'font-family': font_style['family']}), 
                
                    html.H3(children='Sigma (σ)',
                            style={'textAlign': 'center',
                                   'font-family': font_style['family'],}),
                    
                    html.Div([html.Div([dcc.Slider(id='sigma-2', min=7, max=12, step=1,
                                                   value=default_sigma)]),
                
                    html.H3(children='Rho (ρ)',
                            style={'textAlign': 'center',
                                   'font-family': font_style['family'],}),
                    
                    html.Div([html.Div([dcc.Slider(id='rho-2', min=27, max=32, step=1,
                                                   value=default_rho)]),]),
                    
                    html.H3(children='Beta (β)',
                            style={'textAlign': 'center',
                                   'font-family': font_style['family'],}),
                    
                    html.Div([html.Div([dcc.Slider(id='beta-2',min=2, max=2.5, step=0.1,
                                                   value=default_beta)]),])
                    ]) 
                
                ], style={'width': '50%',
                          'padding': '20px'}),
            
            ], style={'display': 'flex',
                    'justify-content': 'space-between',
                    'width': '100%',}),
        
        ], style={'background-color': '#f0f5f9',
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
            return default_initial_state_1[0], default_initial_state_1[1], default_initial_state_1[2], default_initial_state_2[0], default_initial_state_2[1], default_initial_state_2[2], default_sigma, default_rho, default_beta, default_sigma, default_rho, default_beta
        
        return x0_1, y0_1, z0_1, x0_2, y0_2, z0_2, sigma_1, rho_1, beta_1, sigma_2, rho_2, beta_2
    
    # Define colors for the plots
    color_1 = 'teal'
    color_2 = 'orange'
    
    # Plot of time vs x, y, z
    fig1 = plot_time_versus_xyz(solution_1, solution_2, timepoints, color_1, color_2)
    
    # Plot of x, y, z against each other
    fig2 = plot_xyz(solution_1, solution_2, color_1, color_2)
    
    # Plot of x, y, z in 3D
    fig3 = plot_3d(solution_1, solution_2, color_1, color_2)
    
    return app


if __name__ == '__main__':
    
    # Call the main function
    app = main()
    
    # Run the app server
    app.run_server(debug=True)
    
    # Clear the console regardless of the OS
    os.system('cls' if os.name == 'nt' else 'clear')