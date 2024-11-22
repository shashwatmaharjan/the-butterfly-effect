# Import necessary libraries
import os
import sympy as sp

# Lorenz ODE
def lorenz_ode(sigma, rho, beta):
    
    # Define the independent variable
    t = sp.symbols('t')
    
    # Define the dependent variables
    x = sp.Function('x')(t)
    y = sp.Function('y')(t)
    z = sp.Function('z')(t)
    
    # Define derivatives for the Lorenz ODE
    x_dot = sigma*(y - x)
    y_dot = x*(rho - z) - y
    z_dot = x*y - beta*z
    
    # Convert the derivatives to numerical functions using lambdify
    x_dot = sp.lambdify((x, y, z), x_dot)
    y_dot = sp.lambdify((x, y, z), y_dot)
    z_dot = sp.lambdify((x, y, z), z_dot)
    
    return x_dot, y_dot, z_dot
    

# Main function
def main():
    
    # Define constants
    sigma = 10
    rho = 8/3
    beta = 28
    
    # Get the ODE for lorenz equation
    x_dot, y_dot, z_dot = lorenz_ode(sigma, rho, beta)
    

if __name__ == '__main__':
    
    # Clear the console regardless of the OS
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Call the main function
    main()