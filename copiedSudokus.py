#!/usr/bin/env python3
"""
This sudoku problem is copied 
from Pierre Ruyssen's post available at:
http://dev.af83.io/2010/03/19/rsolution-de-problmes-avec-la-programmation-par-contraintes.html
(here version simplified) with educational purpose.
See also http://www.hakank.org/numberjack/
Expected result:
Number of variables: 81
Numbder of constraints: 27
[[1, 2, 3, 4, 5, 6, 7, 8, 9],
 [4, 5, 6, 7, 8, 9, 1, 2, 3],
 [7, 8, 9, 1, 2, 3, 4, 5, 6],
 [2, 6, 1, 9, 3, 4, 8, 7, 5],
 [8, 3, 4, 5, 1, 7, 6, 9, 2],
 [9, 7, 5, 2, 6, 8, 3, 1, 4],
 [3, 1, 2, 6, 7, 5, 9, 4, 8],
 [5, 4, 8, 3, 9, 1, 2, 6, 7],
 [6, 9, 7, 8, 4, 2, 5, 3, 1]]
Nodes: 45, Time: 0.0
--
JohaGL
"""
import itertools
import math
from Numberjack import *

SIZE = 9


SIZE_SQRT = int(math.sqrt(SIZE))
assert SIZE_SQRT ** 2 == SIZE
squares = Matrix(SIZE, SIZE, 1, SIZE)
square_groups = []
#here variables are defined
for x_begin, y_begin in itertools.product(range(0,SIZE,SIZE_SQRT),
                            range(0, SIZE,SIZE_SQRT)):
    square_groups.append([squares[(x,y)]
    for x, y in itertools.product(range(x_begin, x_begin+SIZE_SQRT),
                        range(y_begin, y_begin+SIZE_SQRT))])
#print(square_groups) #prints memory allocation addresses of variables

#here constraints are defined
model = Model()
for group in squares.row + squares.col + square_groups:
    #print(type(AllDiff(group))) #just class Numberjack.AllDiff
    model += AllDiff(group) 

print("Number of variables: %i" % len(model.variables))
print("Numbder of constraints: %i" % len(model.get_exprs()))

solver = model.load("Mistral")
solver.solve()
print(squares)
print(f'Nodes: {solver.getNodes()}, Time: {solver.getTime()}')






