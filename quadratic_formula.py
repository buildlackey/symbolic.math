import argparse
from sympy import symbols, Eq, solve, Rational

def quadratic_formula(a, b, c):
    """
    Solve a quadratic equation of the form ax^2 + bx + c = 0 symbolically.

    Parameters:
    - a (Rational): Coefficient of x^2 (must be non-zero for a valid quadratic equation)
    - b (Rational): Coefficient of x
    - c (Rational): Constant term

    Returns:
    - list: A list of solutions (roots) to the quadratic equation.
    """

    # Define the variable x
    x = symbols('x')
    
    # Define the quadratic equation ax^2 + bx + c = 0
    equation = Eq(a * x**2 + b * x + c, 0)
    
    # Solve the equation symbolically
    solutions = solve(equation, x)
    
    return solutions

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Solve a quadratic equation ax^2 + bx + c = 0 symbolically.")
    parser.add_argument("-a", type=float, required=True, help="Coefficient a (cannot be 0 for a quadratic equation)")
    parser.add_argument("-b", type=float, default=0, help="Coefficient b")
    parser.add_argument("-c", type=float, required=True, help="Coefficient c")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Convert inputs to Rational for exact symbolic computation
    a = Rational(args.a)
    b = Rational(args.b)
    c = Rational(args.c)
    
    # Ensure it's a valid quadratic equation
    if a == 0:
        print("Error: Coefficient 'a' must not be 0 for a quadratic equation.")
    else:
        # Solve the quadratic equation
        roots = quadratic_formula(a, b, c)
        print("The roots are:", roots)

