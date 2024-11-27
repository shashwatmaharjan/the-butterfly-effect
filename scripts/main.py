# Import necessary libraries
import os
import numpy as np

from scipy.integrate import solve_ivp

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
    
    # Get first set of solution for a particular initial condition
    initial_state = [0, 1, 0] # x0, y0, z0
    x1, y1, z1 = solve_lorenz_ode(sigma, rho, beta, initial_state, 0, 10, 0.01)


if __name__ == '__main__':
    
    # Clear the console regardless of the OS
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Call the main function
    main()