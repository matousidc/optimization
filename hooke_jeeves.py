"""
How to run:
python -m hooke_jeeves
"""

import matplotlib.pyplot as plt
import numpy as np

# test functions
def rosen(p: list) -> int:              
    x1, x2 = p
    a = 1
    b = 100
    y = (a - x1) ** 2 + b * (x2 - x1 ** 2) ** 2
    return y


def booth(p: list) -> int:
    x1, x2 = p
    y = (x1 + 2*x2 - 7)**2 + (2*x1 + x2 - 5)**2
    return y


def himmel(p: list) -> int:
    x1, x2 = p
    y = (x1**2 + x2 - 11)**2 + (x1 + x2**2 - 7)**2
    return y
  
  
# hooke-jeeves 2D
def search(p: list, step: int, values: list, fun):
    i = 1
    p_c = p.copy()
    while i <= 2:
        if i == 1:
            cross = [[p_c[0] + step, p_c[1]], [p_c[0] - step, p_c[1]], p]
        elif i ==2:
            cross = [[p_c[0] , p_c[1] + step], [p_c[0], p_c[1] - step], p]
        p_c = cross[[fun(j) for j in cross].index(min(fun(j) for j in cross))]
        i += 1
    if p_c == p:                    # check if changed starting point
        return p, values, None
    p = [p_c[j] + (p_c[j] - p[j]) for j in range(len(p_c))] # pattern move
    values.append(fun(p))
    return p, values, True
 

point = [0, 0]  # starting point
step = 0.5
threshold = 0.01
values = []
points = []
while step > threshold:
    point, values, check = search(point, step, values, himmel)       # change 4th argument for different function
    if not check:
        step /= 2
        continue
    points.append(point)
    if len(values) > 1:
        if values[-1] >= values[-2]:
            step /= 2
            point = points[-2]
print('result:', point)
