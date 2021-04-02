from z3 import *

oracle = 0x1ae78b0243cbcf

for n in range(1,21):
    print(f'Trying for {n} variables')
    
    # Create n variables
    vars = [Int(f'x{i}') for i in range(n)]

    # Initialize constraints with upper bounds and lower bounds
    constraints = [And(x >= ord('a'), x <= ord('z')) for x in vars]

    # Build up and add checksum constraint
    check_expr = 0x1505
    for x in vars:
        check_expr = (check_expr) * 33 + x

    check_constraint = (check_expr == oracle)
    constraints.append(check_constraint)

    # Pass constraints to solver
    s = tuple(constraints)
    print(f"Constraints: {s}")
    solve(*s)
