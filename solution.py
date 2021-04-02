from z3 import *

oracle = 0x1ae78b0243cbcf

for n in range(2, 10):
    print(f"Trying for n = {n}")
    # create a list of n vars
    vars = [Int(f'x{i}') for i in range(n)]
    # constraint to ASCII character range
    constraint_vars = [And(ord('a') <= i, i <= ord('z')) for i in vars]

    # initial constraint on first variable
    current_constraint = (0x1505 * 33) + vars[0]

    # build the constraint in a loop
    for v in vars[1:]:
        current_constraint = (current_constraint * 33) + v

    # add the final constraint
    constraint = (current_constraint == oracle)
    constraint_vars.append(constraint)

    s = tuple(constraint_vars)
    print(f"Constraints: {s}\n")
    solve(*s)
    print()
