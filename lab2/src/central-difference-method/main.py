import numpy as np


def G(x1, x2):
    return 0.5 * ((np.pow(x1, 4) - 16 * np.pow(x1, 2) + 5 * x1) + (np.pow(x2, 4) - 16 * np.pow(x2, 2) + 5 * x2))


def central_differences(x1, x2, delta):
    derivative_x1 = (G(x1 + delta, x2) - G(x1 - delta, x2)) / (2 * delta)
    derivative_x2 = (G(x1, x2 + delta) - G(x1, x2 - delta)) / (2 * delta)
    return derivative_x1, derivative_x2


points = [(-3, 1), (4, -2), (0, 0), (2, 0)]
deltas = [1, 0.1, 0.01, 0.001, 0.0001]

for delta in deltas:
    print(f"\ndelta = {delta}")
    for x1, x2 in points:
        der_x1, der_x2 = central_differences(x1, x2, delta)
        print(f"Похідна G за x1 в точці ({x1}, {x2}): {der_x1}")
        print(f"Похідна G за x2 в точці ({x1}, {x2}): {der_x2}")
