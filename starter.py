from z3 import *

oracle = 0x1ae78b0243cbcf

x1 = Int('x1')
x2 = Int('x2')

constraints = []

constraint_x1 = x1 < 99
constraint_x2 = x2 > 20

constraints.append(constraint_x1)
constraints.append(constraint_x2)
# The above two lines are the same as using logical 'And' included in z3, used
# like this: constraints.append(And(constraint_x1, constraint_x2))

s = tuple(constraints)
print(f"Constraints: {s}")
solve(*s)
