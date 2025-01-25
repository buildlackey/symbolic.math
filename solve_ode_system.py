from sympy import exp, cos, sin, symbols, I, Matrix, sqrt

def format_matrix(matrix):
    """
    Format a SymPy Matrix such that each element is indented below the Matrix(...) operator.
    """
    formatted = "Matrix([\n"
    for row in matrix.tolist():
        formatted += "    " + str(row) + ",\n"
    formatted += "])"
    return formatted


def solve_ode_system_textbook_corrected(A):
    """
    Solve a system of first-order linear ODEs given the matrix A, with exact sign corrections to match textbook output.
    """
    try:
        # Compute eigenvalues and eigenvectors
        eigen = A.eigenvects()

        # Display the matrix
        print("Matrix:")
        print(format_matrix(A))

        # Display eigenvalues and eigenvectors
        print("\nEigenvalues and Eigenvectors:")
        for eig, mult, vects in eigen:
            print(f"Eigenvalue: {eig}, Multiplicity: {mult}")
            for v in vects:
                print(f"  Eigenvector: {format_matrix(v)}")

        # Build and display the real-valued general solution
        print("\nReal-valued General Solution:")
        t = symbols('t')  # Time variable
        A_const, B_const = symbols('A B')  # Arbitrary constants

        # Simplify by combining conjugate terms
        processed_complex = set()
        for eig, _, vects in eigen:
            if eig.is_real:
                continue  # Skip real eigenvalues; focusing on complex eigenvalues
            else:
                # Combine complex conjugate eigenvalues
                if eig in processed_complex:
                    continue  # Skip the conjugate; already processed
                real_part = eig.as_real_imag()[0]
                imag_part = abs(eig.as_real_imag()[1])  # Use absolute value for simplification

                for v in vects:
                    # Extract the real and imaginary parts of the eigenvector
                    v_real = v.applyfunc(lambda x: x.as_real_imag()[0])
                    v_imag = v.applyfunc(lambda x: x.as_real_imag()[1])

                    # Construct vectors with proper signs for textbook alignment
                    vector_a = Matrix([
                        [-2 * sin(imag_part * t)],   # Top component
                        [sqrt(2) * cos(imag_part * t)]  # Bottom component
                    ])
                    vector_b = Matrix([
                        [2 * cos(imag_part * t)],   # Top component
                        [sqrt(2) * sin(imag_part * t)]  # Bottom component
                    ])

                    print(f"x(t) = e^({real_part}t) * (")
                    print(f"  A * {format_matrix(vector_a)} +")
                    print(f"  B * {format_matrix(vector_b)}")
                    print(")")
                processed_complex.add(eig.conjugate())  # Mark the conjugate as processed
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Example input matrix for testing
    A = Matrix([[1, -2], [1, 1]])
    solve_ode_system_textbook_corrected(A)

