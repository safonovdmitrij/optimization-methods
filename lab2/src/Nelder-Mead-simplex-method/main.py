import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time
import math

function_calls = 0


def G(x1, x2):
    global function_calls
    function_calls += 1
    return 0.5 * ((np.pow(x1, 4) - 16 * np.pow(x1, 2) + 5 * x1) + (np.pow(x2, 4) - 16 * np.pow(x2, 2) + 5 * x2))

def build_regular_simplex_around_point(x0, alpha):
    x0 = np.array(x0, dtype=float)
    simplex = []

    for i in range(3):
        angle = 2 * math.pi * i / 3
        dx = alpha * math.cos(angle)
        dy = alpha * math.sin(angle)
        point = x0 + np.array([dx, dy])
        simplex.append(point.tolist())

    return simplex


def find_centre(simplex, remove_index):
    sum_coords = []
    for j in range(N + 1):
        if j != remove_index:
            sum_coords.append(simplex[j])

    centre = [0, 0]
    for i in range(N):
        for j in range(N):
            centre[i] += sum_coords[j][i]
        centre[i] /= N
    return centre


def reflect_point(simplex, index, coef):
    xc = find_centre(simplex, index)
    xprev = simplex[index]

    xnew = [0, 0]
    for i in range(N):
        xnew[i] = xc[i] + coef * (xc[i] - xprev[i])

    return xnew


def myFunc(e):
    return e[0]


def function_range(evaluated):
    values = [val for val, _ in evaluated]
    return max(values) - min(values)



def nedler_mead(x0, a, accuracy, max_iter):
    simplex_path = []
    simplex = build_regular_simplex_around_point(x0, a)
    simplex_path.append([p.copy() for p in simplex])

    iter = 0

    while iter < max_iter:
        evaluated = [(G(p[0], p[1]), p) for p in simplex]
        evaluated.sort(key=myFunc)

        if function_range(evaluated) < accuracy:
            break

        best_point = evaluated[0][1]
        best_value = evaluated[0][0]
        worst_point = evaluated[2][1]
        worst_value = evaluated[2][0]
        worst_index = simplex.index(worst_point)

        # Три пробні точки
        new_points = [
            reflect_point(simplex, worst_index, 1),  # Розтягнення
            reflect_point(simplex, worst_index, 1.5),   # Сильне розтягнення
            reflect_point(simplex, worst_index, 0.75)  # Стиснення
        ]

        new_evaluated = [(G(p[0], p[1]), p) for p in new_points]

        # Обираємо найкращу з нових точок
        best_new_value, best_new_point = min(new_evaluated, key=lambda x: x[0])

        if best_new_value < worst_value:
            simplex[worst_index] = best_new_point
        else:
            for i in range(N + 1):
                if simplex[i] != best_point:
                    simplex[i] = [(simplex[i][j] + best_point[j]) / 2 for j in range(N)]

        simplex_path.append([p.copy() for p in simplex])
        iter += 1

    evaluated = [(G(p[0], p[1]), p) for p in simplex]
    evaluated.sort(key=myFunc)
    xmin = evaluated[0][1]
    gmin = evaluated[0][0]

    return xmin, gmin, simplex_path



x_start = [0.156731, 0.156731]
a = 2
accuracy = 0.001
max_iter = 100
N = 2

xmin = 0
gmin = 0

start = time.perf_counter_ns()
xmin, gmin, simplex_path = nedler_mead(x_start, a, accuracy, max_iter)
end = time.perf_counter_ns()
elapsed = end - start

print(f'Точка мінімуму: ({xmin})\nЗначення функції: {gmin}')
print(f'КОЦФ: {function_calls}')
print(f"Час виконання: {elapsed / 1_000_000_000:.6f} секунд")

# Візуалізація

x1_vals = np.linspace(-4, 4, 200)
x2_vals = np.linspace(-4, 4, 200)
X1, X2 = np.meshgrid(x1_vals, x2_vals)
Z = G(X1, X2)

fig = plt.figure(figsize=(12, 5))

# 3D графік
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax1.plot_surface(X1, X2, Z, cmap=cm.viridis, alpha=0.5)

for triangle in simplex_path:
    triangle_closed = triangle + [triangle[0]]
    xs = [p[0] for p in triangle_closed]
    ys = [p[1] for p in triangle_closed]
    zs = [G(p[0], p[1]) for p in triangle_closed]
    ax1.plot(xs, ys, zs, color='blue', lw=0.8)

ax1.set_zlim(-80, 60)
ax1.set_xlabel('$x_1$')
ax1.set_ylabel('$x_2$')
ax1.set_zlabel('$G(x_1, x_2)$')
ax1.set_title('3D поверхня + симплекс')

# Ізолінії
ax2 = fig.add_subplot(1, 2, 2)
contour = ax2.contour(X1, X2, Z, cmap=cm.viridis, levels=12, linestyles='dashed')

for triangle in simplex_path:
    triangle_closed = triangle + [triangle[0]]
    xs = [p[0] for p in triangle_closed]
    ys = [p[1] for p in triangle_closed]
    ax2.plot(xs, ys, color='blue', linewidth=0.8, label='_simplex')

plt.colorbar(contour, ax=ax2)
ax2.set_xlabel('$x_1$')
ax2.set_ylabel('$x_2$')
ax2.set_title('Ізолінії + симплекс')

plt.tight_layout()
plt.show()

