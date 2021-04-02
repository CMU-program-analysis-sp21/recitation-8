from z3 import *

x = Int('x')
y = Int('y')

constraints = (And(0 < x, x < 10),
               And(0 < y, y < 10),
               x * x + 1 == y - 2)

solve(*constraints)
