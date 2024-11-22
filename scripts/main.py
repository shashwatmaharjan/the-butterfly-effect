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
    

# Main function
def main():
    
    # Define constants
    sigma = 10
    rho = 28
    beta = 8/3
    
    # Initial conditions
    x0 = 1
    y0 = 1
    z0 = 1
    initial_state = [x0, y0, z0]
    
    # Time parameters
    t0 = 0
    tf = 10
    dt = 0.01
    
    # Timepoints for the solution
    timepoints = np.arange(t0, tf, dt)
    
    # Solve the ODEs using solve_ivp
    solution = solve_ivp(lorenz_ode, [t0, tf], initial_state, args=(sigma, rho, beta), t_eval=timepoints)

    # Extract the solution components
    x, y, z = solution.y


if __name__ == '__main__':
    
    # Clear the console regardless of the OS
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Call the main function
    main()