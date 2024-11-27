# Import necessary libraries
import os
import numpy as np

# For solving the ODEs
from scipy.integrate import solve_ivp

# For the web app
import dash
from dash import Dash, dcc, html, Input, Output, State
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


# Main function
def main():
    
    # Define constants 
    sigma = 10
    rho = 28
    beta = 8/3
    
    # Timepoints
    t0 = 0
    tf = 10
    dt = 0.01
    
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
        
        # Container for the plots
        html.Div([
            # x vs time
            html.Div([dcc.Graph(id='x-time-plot', style={'width': '33%'})]),
            html.Div([dcc.Graph(id='y-time-plot', style={'width': '33%'})]),
            html.Div([dcc.Graph(id='z-time-plot', style={'width': '33%'})]),],
                 
                 style={'display': 'flex',
                        'justify-content': 'space-between',
                        'width': '100%'}),
        
        ], style={'background-color': '#f0f5f9',
                  'min-height': '100vh'})
        
    return app


if __name__ == '__main__':
    
    # Call the main function
    app = main()
    
    # Run the app server
    app.run_server(debug=True)
    
    # Clear the console regardless of the OS
    os.system('cls' if os.name == 'nt' else 'clear')