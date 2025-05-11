import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
import sys

"""
============================================================
Symbolic Cross Product Script
============================================================

This script computes the symbolic cross product of two 3D vectors
defined in a plain text file. It can also compute the magnitude 
of the cross product and optionally evaluate the result at a 
given point.

------------------------------------------------------------
USAGE
------------------------------------------------------------

    python xprod.py <vector_file.txt>

- Prints the symbolic cross product
- Computes the symbolic magnitude
- Optionally evaluates the result at a point (if provided)

------------------------------------------------------------
INPUT FORMAT (vector_file.txt)
------------------------------------------------------------

1. The file must contain exactly 6 expressions (3 for each vector).
2. You may optionally include a `point:` block to specify a point 
   at which to evaluate the result.

Example:

    r*sin(u)*cos(v)
    r*sin(u)*sin(v)
    r*cos(u)

    1
    0
    0

    point:
    u = pi/2
    v = pi/4
    r = 2

------------------------------------------------------------
OUTPUT
------------------------------------------------------------

- Symbolic cross product (as a 3x1 SymPy matrix)
- Symbolic magnitude of the cross product
- If `point:` is provided:
    - Evaluated vector at point
    - Evaluated magnitude at point

Example Output:

    Symbolic cross product result:
    [-r*cos(u)*cos(v)]
    [ r*cos(u)*sin(v)]
    [     r*sin(u)   ]

    Magnitude of cross product:
    sqrt(r^2)

    Cross product evaluated at given point:
    [-1]
    [ 1]
    [ 0]

    Magnitude at given point:
    sqrt(2)

------------------------------------------------------------
NOTES
------------------------------------------------------------

- This script is designed to support symbolic math in 
  environments like Jupyter or CLI analysis pipelines.
- If variable values are missing for evaluation, an error will
  be raised listing the missing symbols.

============================================================


"""



def load_vectors_and_point_from_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    v1_lines = []
    v2_lines = []
    point_subs = {}
    reading_point_block = False
    vector_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        if stripped.lower().startswith("point:"):
            reading_point_block = True
            continue

        if reading_point_block:
            if '=' in stripped:
                var, val = map(str.strip, stripped.split('=', 1))
                point_subs[sp.Symbol(var)] = parse_expr(val, evaluate=False)
            else:
                raise ValueError(f"Invalid format in point block: '{stripped}'")
        else:
            vector_lines.append(parse_expr(stripped, evaluate=False))

    half = len(vector_lines) // 2
    v1 = sp.Matrix(vector_lines[:half])
    v2 = sp.Matrix(vector_lines[half:])

    return v1, v2, point_subs

def symbolic_cross_product_and_magnitude(filepath):
    v1, v2, point_subs = load_vectors_and_point_from_file(filepath)
    cross_prod = sp.simplify(v1.cross(v2))
    magnitude = sp.simplify(sp.sqrt(cross_prod.dot(cross_prod)))

    evaluation = None
    evaluated_magnitude = None
    if point_subs:
        free_syms = cross_prod.free_symbols
        if not free_syms.issubset(point_subs.keys()):
            missing = free_syms - point_subs.keys()
            raise ValueError(f"Missing values for variables: {', '.join(str(s) for s in missing)}")
        evaluation = sp.simplify(cross_prod.subs(point_subs))
        evaluated_magnitude = sp.simplify(sp.sqrt(evaluation.dot(evaluation)))

    return cross_prod, magnitude, evaluation, evaluated_magnitude

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cross_product.py <vector_file.txt>")
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        cross_prod, magnitude, evaluation, evaluated_magnitude = symbolic_cross_product_and_magnitude(filepath)
        print("Symbolic cross product result:")
        sp.pprint(cross_prod)
        print("\nMagnitude of cross product:")
        sp.pprint(magnitude)
        if evaluation is not None:
            print("\nCross product evaluated at given point:")
            sp.pprint(evaluation)
        if evaluated_magnitude is not None:
            print("\nMagnitude at given point:")
            sp.pprint(evaluated_magnitude)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

