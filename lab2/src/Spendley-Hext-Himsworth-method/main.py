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


def build_regular_simplex(x0, alpha):
    x0 = np.array(x0, dtype=float)
    simplex = [x0.tolist()]

    sigma1 = ((np.sqrt(N + 1) + N - 1) / (N * np.sqrt(2))) * alpha
    sigma2 = ((np.sqrt(N + 1) - 1) / (N * np.sqrt(2))) * alpha

    for i in range(N):
        xi = np.array(x0)
        for j in range(N):
            if i != j:
                xi[j] = xi[j] + sigma1
            else:
                xi[j] = xi[j] + sigma2
        simplex.append(xi.tolist())

    return simplex

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


def reflect_point(simplex, index):
    xc = find_centre(simplex, index)
    xprev = simplex[index]

    xnew = [0, 0]
    for i in range(N):
        xnew[i] = xc[i] + (xc[i] - xprev[i])


    return xnew


def myFunc(e):
    return e[0]

def function_range(evaluated):
    values = [val for val, _ in evaluated]
    return max(values) - min(values)


def shh(x0, a, accuracy, max_iter):
    simplex_path = []
    simplex = build_regular_simplex_around_point(x0, a)
    simplex_path.append([p.copy() for p in simplex])

    repeat_count = [0] * (N + 1)
    M = round(1.65 * N + 0.05 * N ** 2)

    iter = 0

    while iter < max_iter:
        # Обчислюємо значення у кожній вершині
        evaluated = []

        for point in simplex:
            value = G(point[0], point[1])
            evaluated.append((value, point))

        evaluated.sort(key=myFunc)

        if function_range(evaluated) < accuracy:
            break

        # відобразити вершину з найгіршим значенням
        worst_index = simplex.index(evaluated[2][1])
        xnew = reflect_point(simplex, worst_index)

        new_value = G(xnew[0], xnew[1])
        evaluated[2] = (new_value, xnew)

        evaluated.sort(key=myFunc)

        # 1 правило
        if xnew == evaluated[2][1]:  # нова точка виявилася найгіршою
            worst_index = simplex.index(evaluated[1][1])  # потрібно виключити другу за значенням точку
            xnew = reflect_point(simplex, worst_index)
            simplex[worst_index] = xnew
        else:
            simplex[worst_index] = xnew

        # 2 правило
        for i in range(N+1):
            if i == worst_index:
                repeat_count[i] = 0
            else:
                repeat_count[i] += 1

        if max(repeat_count) >= M:
            best_point = evaluated[0][1]
            a = a / 2  # редукція
            simplex = build_regular_simplex_around_point(best_point, a)
            repeat_count = [0] * (N + 1)

        simplex_path.append([p.copy() for p in simplex])
        iter += 1

    # Знаходимо найкращу точку після завершення
    best_value = float('inf')
    xmin = evaluated[0][1]
    gmin = evaluated[0][0]

    return xmin, gmin, simplex_path


x_start = [0.156731, 0]
a = 0.5
accuracy = 0.001
max_iter = 1000
N = 2

start = time.perf_counter_ns()
xmin, gmin, simplex_path = shh(x_start, a, accuracy, max_iter)
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
