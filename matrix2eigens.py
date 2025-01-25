import sys
from sympy import Matrix, I  # I represents sqrt(-1) in SymPy

def read_matrix_from_file(file_path, delimiter=" "):
    """
    Read a matrix from a file where rows are separated by newlines and elements
    are separated by spaces (or other delimiters).
    
    Parameters:
    - file_path (str): Path to the file containing the matrix definition.
    - delimiter (str): Character separating elements in a row (default: space).
    
    Returns:
    - Matrix: A SymPy Matrix object representing the input matrix.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()
    matrix = []
    for line in lines:
        if line.strip():  # Ignore empty or whitespace-only lines
            row = [eval(entry.strip()) for entry in line.strip().split(delimiter) if entry.strip()]
            matrix.append(row)
    return Matrix(matrix)

def compute_eigen(matrix):
    """
    Compute eigenvalues and eigenvectors of a given matrix symbolically.
    
    Parameters:
    - matrix (Matrix): A SymPy Matrix object.
    
    Returns:
    - dict: A dictionary with the matrix, its eigenvalues, and eigenvectors.
    """
    eigenvals = matrix.eigenvals()  # Eigenvalues
    eigenvects = matrix.eigenvects()  # Eigenvectors
    return {"Matrix": matrix, "Eigenvalues": eigenvals, "Eigenvectors": eigenvects}

def compute_eigen_from_file(file_path):
    """
    Compute eigenvalues and eigenvectors from a matrix defined in a file.
    
    Parameters:
    - file_path (str): Path to the file containing the matrix definition.
    
    Returns:
    - dict: A dictionary with the matrix, its eigenvalues, and eigenvectors.
    """
    matrix = read_matrix_from_file(file_path)
    return compute_eigen(matrix)

if __name__ == "__main__":
    """
    Command-line interface for computing eigenvalues and eigenvectors of a matrix
    from a file.
    
    Usage:
    python matrix_eigen.py <matrix_file_path>
    
    Example:
    python matrix_eigen.py matrix.txt
    """
    if len(sys.argv) != 2:
        print("Usage: python matrix_eigen.py <matrix_file_path>")
        sys.exit(1)

    # Get the file path
    file_path = sys.argv[1]

    # Compute eigenvalues and eigenvectors
    try:
        result = compute_eigen_from_file(file_path)
        print("Matrix:")
        print(result["Matrix"])
        print("\nEigenvalues:")
        for eig, mult in result["Eigenvalues"].items():
            print(f"  {eig}: multiplicity {mult}")
        print("\nEigenvectors:")
        for eig, mult, vects in result["Eigenvectors"]:
            print(f"  Eigenvalue: {eig}, Multiplicity: {mult}")
            for v in vects:
                print(f"    Eigenvector: {v}")
    except Exception as e:
        print(f"An error occurred: {e}")

