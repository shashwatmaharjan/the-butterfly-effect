# Import necessary libraries
import os
import numpy as np

# For solving the ODEs
from scipy.integrate import solve_ivp

# For the web app
import matplotlib.pyplot as plt
from dash import Dash, dcc, html
from plotly.tools import mpl_to_plotly
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


# Function to make subplots for plotting seven combination of trajectories
def make_subplots(x1, y1, z1, x2, y2, z2, timepoints, color1 = 'blue', color2 = 'yellow'):
    
    # Define the spacing for the y-ticks
    abscissa_num_ticks = 10
    ordinate_num_ticks = 5
    
    # Define the x-tick labels
    x_tick_labels = np.arange(timepoints.min(), timepoints.max() + 1, abscissa_num_ticks)
    
    # Define the y-tick labels
    # For "x" plots
    smallest_x_value = int(min(x1.min(), x2.min()).round(0))
    largest_x_value = int(max(x1.max(), x2.max()).round(0))
    x_value_ticks = np.linspace(smallest_x_value, largest_x_value, ordinate_num_ticks).astype(int)
    
    # For "y" plots
    smallest_y_value = int(min(y1.min(), y2.min()).round(0))
    largest_y_value = int(max(y1.max(), y2.max()).round(0))
    y_value_ticks = np.linspace(smallest_y_value, largest_y_value, ordinate_num_ticks).astype(int)
    
    # For "z" plots
    smallest_z_value = int(min(z1.min(), z2.min()).round(0))
    largest_z_value = int(max(z1.max(), z2.max()).round(0))
    z_value_ticks = np.linspace(smallest_z_value, largest_z_value, ordinate_num_ticks).astype(int)
    
    # Figure
    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(21, 9))
    
    ##### First subplot: time vs x1 values #####
    ax[0, 0].plot(timepoints, x1, color=color1, linestyle='--')
    ax[0, 0].plot(timepoints, x2, color=color2)
    
    # Set the title for the first subplot
    ax[0, 0].set_title('Time (t) vs x(t)')
    
    # Set the label for the first subplot
    ax[0, 0].set_ylabel('x(t)')
    ax[0, 0].set_xlabel('Time (t)')
    
    # Define the x-ticks
    ax[0, 0].set_xticks(x_tick_labels)
    
    # Define the y-ticks
    ax[0, 0].set_yticks(x_value_ticks)
    
    ##### Second subplot: time vs y1 values #####
    ax[0, 1].plot(timepoints, y1, color=color1, linestyle='--')
    ax[0, 1].plot(timepoints, y2, color=color2)
    
    # Set the title for the second subplot
    ax[0, 1].set_title('Time (t) vs y(t)')
    ax[0, 1].set_xlabel('Time (t)')
    
    # Set the y-label for the second subplot
    ax[0, 1].set_ylabel('y(t)')
    
    # Define the x-ticks
    ax[0, 1].set_xticks(x_tick_labels)
    
    # Define the y-ticks
    ax[0, 1].set_yticks(y_value_ticks)
    
    ##### Third subplot: time vs z1 values #####
    ax[0, 2].plot(timepoints, z1, color=color1, linestyle='--')
    ax[0, 2].plot(timepoints, z2, color=color2)
    
    # Set the title for the third subplot
    ax[0, 2].set_title('Time (t) vs z(t)')
    
    # Set the y-label for the third subplot
    ax[0, 2].set_ylabel('z(t)')
    ax[0, 2].set_xlabel('Time (t)')
    
    # Define the x-ticks
    ax[0, 2].set_xticks(x_tick_labels)
    
    # Define the y-ticks
    ax[0, 2].set_yticks(z_value_ticks)
    
    ##### Fourth subplot: x vs y #####
    ax[1, 0].plot(x1, y1, color=color1, linestyle='--')
    ax[1, 0].plot(x2, y2, color=color2)
    
    # Set the title for the fourth subplot
    ax[1, 0].set_title('x(t) vs y(t)')
    
    # Set the x-label for the fourth subplot
    ax[1, 0].set_xlabel('x(t)')
    
    # Set the y-label for the fourth subplot
    ax[1, 0].set_ylabel('y(t)')
    
    # Define the x-ticks
    ax[1, 0].set_xticks(x_value_ticks)
    
    # Define the y-ticks
    ax[1, 0].set_yticks(y_value_ticks)
    
    ##### Fifth subplot: x vs z #####
    ax[1, 1].plot(x1, z1, color=color1, linestyle='--')
    ax[1, 1].plot(x2, z2, color=color2)
    
    # Set the title for the fifth subplot
    ax[1, 1].set_title('x(t) vs z(t)')
    
    # Set the x-label for the fifth subplot
    ax[1, 1].set_xlabel('x(t)')
    
    # Set the y-label for the fifth subplot
    ax[1, 1].set_ylabel('z(t)')
    
    # Define the x-ticks
    ax[1, 1].set_xticks(x_value_ticks)
    
    # Define the y-ticks
    ax[1, 1].set_yticks(z_value_ticks)
    
    ##### Sixth subplot: y vs z #####
    ax[1, 2].plot(y1, z1, color=color1, linestyle='--')
    ax[1, 2].plot(y2, z2, color=color2)
    
    # Set the title for the sixth subplot
    ax[1, 2].set_title('y(t) vs z(t)')
    
    # Set the x-label for the sixth subplot
    ax[1, 2].set_xlabel('y(t)')
    
    # Set the y-label for the sixth subplot
    ax[1, 2].set_ylabel('z(t)')
    
    # Define the x-ticks
    ax[1, 2].set_xticks(y_value_ticks)
    
    # Define the y-ticks
    ax[1, 2].set_yticks(z_value_ticks)
    
    # Adjust the padding between subplots
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.4, hspace=0.4)
    
    return fig
    

# Main function
def main():
    
    # Define constants 
    sigma = 10
    rho = 28
    beta = 8/3
    
    # Timepoints
    t0 = 0
    tf = 50
    dt = 0.01
    timepoints = np.arange(t0, tf, dt)
    
    # First initial state
    initial_state_1 = [0, 1, 0] # x0_1, y0_1, z0_1
    solution_1 = solve_lorenz_ode(sigma, rho, beta, initial_state_1, t0, tf, dt) # x1, y1, z1
    
    # Second initial state
    initial_state_2 = [1, 0, 1] # x0_2, y0_2, z0_2
    solution_2 = solve_lorenz_ode(sigma, rho, beta, initial_state_2, t0, tf, dt) # x2, y2, z2
    
    # Define common styles for font
    font_style = {'family': 'Courier New, Courier, monospace'}
    
    # Define the default border radius
    border_radius = '2px'
    
    # Define tight layout for the plots
    tight_layout = go.Layout(margin=dict(t=20, b=20, l=20, r=20),
                             xaxis = dict(showgrid=False, range=[0, None]),
                             yaxis = dict(showgrid=False))
    
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
        html.Div([html.Button(id='visualize-button', children='Generate', style={'display': 'block',
                                                                                  'background-color': '#4CAF50',
                                                                                  'color': 'white',
                                                                                  'border': 'none',
                                                                                  'border-radius': border_radius,
                                                                                  'cursor': 'pointer',
                                                                                  'text-align': 'center',
                                                                                  'padding': '5px 10px',
                                                                                  'font-family': font_style['family'],
                                                                                  'font-size': '25px'},)],
                 style={'display': 'flex',
                        'justify-content':'center',
                        'padding': '5px'}),
                    
        # Container for the two columns for the initial conditions
        html.Div([
            # Left column
            # Initial condition 1
            html.Div([
                html.H3(id='ic-1',
                        children='Initial Condition 1',
                        style={'textAlign': 'center',
                               'font-family': font_style['family'],}),
                        
                html.Div([html.Div(['x: ', dcc.Input(id='x0_1', type = 'number', value = 0, min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                   'text-align': 'center',
                                                                                                                                   'font-family': font_style['family'],
                                                                                                                                   'border-radius': border_radius}),]),
                        html.Div(['y: ', dcc.Input(id='y0_1', type = 'number', value = 1, min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                 'text-align': 'center',
                                                                                                                                 'font-family': font_style['family'],
                                                                                                                                 'border-radius': border_radius}),]),
                        html.Div(['z: ', dcc.Input(id='z0_1', type = 'number', value = 0, min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                 'text-align': 'center',
                                                                                                                                 'font-family': font_style['family'],
                                                                                                                                 'border-radius': border_radius}),]),],
                        
                        style={'display': 'flex',
                               'justify-content': 'center',
                               'gap': '20px',
                               'font-family': font_style['family']}), 
                
                ], style={'width': '50%',
                          'padding': '20px'}),
            
            # Right column
            # Initial condition 2
            html.Div([
                html.H3(id='ic-2',
                        children='Initial Condition 2',
                        style={'textAlign': 'center',
                               'font-family': font_style['family'],}),
                        
                html.Div([html.Div(['x: ', dcc.Input(id='x0_2', type = 'number', value = 0, min=-10, max=10, required=True,  style={'width': '40px',
                                                                                                                                    'text-align': 'center',
                                                                                                                                   'font-family': font_style['family'],
                                                                                                                                   'border-radius': border_radius}),]),
                        html.Div(['y: ', dcc.Input(id='y0_2', type = 'number', value = 1, min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                 'text-align': 'center',
                                                                                                                                 'font-family': font_style['family'],
                                                                                                                                 'border-radius': border_radius}),]),
                        html.Div(['z: ', dcc.Input(id='z0_2', type = 'number', value = 0, min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                 'text-align': 'center',
                                                                                                                                 'font-family': font_style['family'],
                                                                                                                                 'border-radius': border_radius}),]),],
                        
                        style={'display': 'flex',
                               'justify-content': 'center',
                               'gap': '20px',
                               'font-family': font_style['family']}), 
                
                ], style={'width': '50%',
                          'padding': '20px'}),
            
            ], style={'display': 'flex',
                    'justify-content': 'space-between',
                    'width': '100%',}),
        
        ], style={'background-color': '#f0f5f9',
                  'min-height': '100vh'})
    
    # Get the figure
    fig = make_subplots(solution_1[0], solution_1[1], solution_1[2], solution_2[0], solution_2[1], solution_2[2], timepoints)
    
    # Show plot
    plt.show()
        
    return app


if __name__ == '__main__':
    
    # Set default font and math text font for the plots
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['mathtext.fontset'] = 'dejavuserif'

    # Define font size for plots
    plt.rcParams.update({'font.size': 15})
    
    # Call the main function
    app = main()
    
    # Run the app server
    app.run_server(debug=True)
    
    # Clear the console regardless of the OS
    os.system('cls' if os.name == 'nt' else 'clear')