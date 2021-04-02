# Set up

Set up the Python interface for Z3 using `pip`. I did this on my machine using
`pip3 install z3-solver --user`

If the installation is successful you should be able to run `python3
example.py`, which solves the constraints `0 < x < 10`, `0 < y < 10`, `x * x + 1
== y - 2` and computes the result `[y = 7, x = 2]`

# Example
Here are the contents of `example.py`:

```python
from z3 import *

x = Int('x')
y = Int('y')

constraints = (And(0 < x, x < 10),
               And(0 < y, y < 10),
               x * x + 1 == y - 2)

solve(*constraints)
```

This declares two Z3 `Int` constants named `x` and `y`, then creates a tuple of
constraints and calls the solver. An equivalent SMT-LIB formula (Z3's native
language) is in `example.z3`

```
(declare-const x (Int))
(declare-const y (Int))

(assert (and (> x 0) (< x 10)))
(assert (and (> y 0) (< y 10)))
(assert (= (+ (* x x) 1) (- y 2)))

(check-sat)
(get-model)
(exit)
```

If you have Z3 installed, you can run this with `z3 example.z3`. You can also
run Z3 using Microsoft's online sandbox at
[Rise4Fun](https://rise4fun.com/z3/tutorial).

# Challenge

Here is some code that computes a checksum of a string `s`:

```python
def checksum(s):
  v = 0x1505
  for char in s:
    v = (v * 33) + ord(char)
  return v
```

Your job is to find a string (using z3) that satisfies the checksum
`0x1ae78b0243cbcf`. Specifically, your string should cause the following to be
true:

`checksum(SOLUTION) == 0x1ae78b0243cbcf`

**Don't brute force it, that will take too long.**

The set of possible characters is `a-z`. I'm not telling you the length.

## Python API

While you can solve this using SMT-LIB and Z3, we will instead use the Python
library which: (a) takes care of creating constants and (b) lets you use infix
notation for arithmetic expressions.

You can declare `Int` variables in Python like this:

```
my_int_variable = Int('x')
```

Here's a boilerplate code to get you started:

```python
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
```

If you have z3 set up correctly, you should see:

```
Constraints:  (x1 < 99, x2 > 20)
[x2 = 21, x1 = 98]
```

## Hint

<details>
  <summary>Click to expand a hint</summary>

The idea is to build up constraints based on the checksum function. Let's
pretend our string was simply "a". The checksum will calculate: `v = 33 *
0x1505 + ord('a') = 177670 = 0x2b606`.

How about if our string was "ab"? The checksum will calculate: `v = 33 * (33 *
0x1505 + ord('a')) + ord('b') = 0x597728`

And so on.

So `checksum` can be summarized by a bunch of constraints on some number of
characters. We can express the constraints and use symbolic variables for the
characters.  Here is a Z3 example for the one character case, where we want to
solve some character for the checksum `0x2b606` (decimal `177670`). Above, we
know that "a" will work. Can z3 tell us this?

```
(declare-const x (Int))
(assert (= (+ (* 33 5381) x) 177670))

(check-sat)
(get-model)
(exit)
```

Running this gives the output:
```
sat
(model
  (define-fun x () Int
    97)
)
```
Which is correct, since ASCII `a` is decimal 97 (You can see this by printing
`ord('a')` or `chr(97)` in Python).

Here's a program that solves two characters for the checksum `0x597728`:

```
(declare-const x1 (Int))
(declare-const x2 (Int))

(assert (= (+ (* 33 (+ (* 33 5381) x1)) x2) 5863208))

(check-sat)
(get-model)
(exit)
```

Solution:

```
sat
(model
  (define-fun x1 () Int
    0)
  (define-fun x2 () Int
    3299)
)
```

Oh! Z3 gives us a strange solution. `x1` is `0` and `x2` is `3299`. While that
satisfies the constraints, we can't represent `3299` in ASCII.  Can we add more
constraints to convince Z3 to give us a reasonable solution?
</details>

## Hint 2

<details>
  <summary>Click to expand another hint</summary>

What if we tell Z3 that the variables must be within ascii printable range? `z`
is the value 122, or 0x7a. We can tell Z3 that `x1` and `x2` must be less than
or equal to that:

```
(assert (<= x1 122))
(assert (<= x2 122))
```

(In Python, we can simply add the constraint `constraint_x1 = x1 <= 0x7a`)

</details>



# References

- [Z3 online](https://rise4fun.com/Z3)
- [Z3 Guide](https://rise4fun.com/z3/tutorialcontent/guide#h23)
- [Python Z3 examples](http://ericpony.github.io/z3py-tutorial/guide-examples.htm)
- [Python API](http://z3prover.github.io/api/html/namespacez3py.html)
