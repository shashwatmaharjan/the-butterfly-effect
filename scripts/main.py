# Import necessary libraries
import os
import numpy as np

# For solving the ODEs
from scipy.integrate import solve_ivp

# For the web app
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
    
    app = Dash(__name__)
    
    app.layout = html.Div([
        
        # Title
        html.H1(id='title',
                children='The Butterfly Effect',
                style={'textAlign': 'center'}),
        
        html.H2(id='sub-title',
                children='Try changing the initial conditions and see how the trajectories diverge.',
                style={'textAlign': 'center'}),
        
        # Visualize button
        html.Div([html.Button(id='visualize-button', children='Visualize', style={'display': 'block',
                                                                                  'background-color': '#4CAF50',
                                                                                  'color': 'white',
                                                                                  'border': 'none',
                                                                                  'border-radius': '10px',
                                                                                  'cursor': 'pointer',
                                                                                  'text-align': 'center',
                                                                                  'padding': '5px 10px'},)],
                 style={'display': 'flex',
                        'justify-content':'center',
                        'padding': '5px'}),
                    
        # Container for the two columns
        html.Div([
            # Left column
            # Initial condition 1
            html.Div([
                html.H3(id='ic-1',
                        children='Initial Condition 1',
                        style={'textAlign': 'center'}),
                        
                html.Div([html.Div(['x: ', dcc.Input(id='x0_1', type = 'number', value = 0, min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                   'text-align': 'center'}),]),
                        html.Div(['y: ', dcc.Input(id='y0_1', type = 'number', value = 1, min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                 'text-align': 'center'}),]),
                        html.Div(['z: ', dcc.Input(id='z0_1', type = 'number', value = 0, min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                 'text-align': 'center'}),]),],
                        
                        style={'display': 'flex',
                               'justify-content': 'center',
                               'gap': '20px'}), 
                
                ], style={'width': '50%',
                          'padding': '20px'}),
            
            # Right column
            # Initial condition 2
            html.Div([
                html.H3(id='ic-2',
                        children='Initial Condition 2',
                        style={'textAlign': 'center'}),
                        
                html.Div([html.Div(['x: ', dcc.Input(id='x0_2', type = 'number', value = 0, min=-10, max=10, required=True,  style={'width': '40px',
                                                                                                                                    'text-align': 'center'}),]),
                        html.Div(['y: ', dcc.Input(id='y0_2', type = 'number', value = 1, min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                 'text-align': 'center'}),]),
                        html.Div(['z: ', dcc.Input(id='z0_2', type = 'number', value = 0, min=-10, max=10, required=True, style={'width': '40px',
                                                                                                                                 'text-align': 'center'}),]),],
                        
                        style={'display': 'flex',
                               'justify-content': 'center',
                               'gap': '20px'}), 
                
                ], style={'width': '50%',
                          'padding': '20px'}),
            
        ], style={'display': 'flex',
                  'justify-content': 'space-between'}),

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