import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time

function_calls = 0


def G(x1, x2):
    global function_calls
    function_calls += 1
    return 0.5 * ((np.pow(x1, 4) - 16 * np.pow(x1, 2) + 5 * x1) + (np.pow(x2, 4) - 16 * np.pow(x2, 2) + 5 * x2))


def new_point(x, h, index):
    x = x.copy()

    val_start = G(x[0], x[1])

    x_right = x.copy()
    x_right[index] += h
    val_right = G(x_right[0], x_right[1])

    x_left = x.copy()
    x_left[index] -= h
    val_left = G(x_left[0], x_left[1])

    if val_right < val_start and val_right < val_left:
        return x_right
    elif val_left < val_start and val_left < val_right:
        return x_left
    else:
        return x


def exploratory_search(x, h, accuracy):
    x_new = x.copy()
    h_new = h
    G_start = G(x[0], x[1])

    # Досліджуємо вздовж x1
    x1_new = new_point(x_new, h, 0)
    G_x1_new = G(x1_new[0], x1_new[1])

    if G_x1_new < G_start:
        x_new = x1_new

    # Досліджуємо вздовж x2
    x2_new = new_point(x_new, h, 1)
    G_x2_new = G(x2_new[0], x2_new[1])

    if G_x2_new < G_start:
        x_new = x2_new

    if h_new < accuracy:
        return x_new, h_new

    # Не знайшои кращу точку - повторюємо з меншим кроком
    if x_new == x:
        h_new = h / 40
        return exploratory_search(x_new, h_new, accuracy)

    return x_new, h_new


def pattern_move(x, h, accuracy):
    x_prev = x
    x_current, h_current = exploratory_search(x, h, accuracy)
    x_next = [x_current[i] + (x_current[i] - x_prev[i]) for i in range(len(x))]

    G2 = G(x_current[0], x_current[1])
    G3 = G(x_next[0], x_next[1])

    if G3 < G2:
        return exploratory_search(x_next, h, accuracy)
    else:
        return exploratory_search(x_current, h, accuracy)


def hooke_jeeves(x_start, h_start, accuracy, max_iter):
    x = x_start.copy()
    h = h_start
    path = [x.copy()]
    iterations = 0

    while h > accuracy and iterations < max_iter:
        x_new, h = pattern_move(x, h, accuracy)
        path.append(x_new.copy())
        x = x_new
        iterations += 1

    return x, G(x[0], x[1]), path


x_start = [0.156731, 0]
h_start = 0.75
accuracy = 0.001
max_iter = 1000

start = time.perf_counter_ns()
min_point, min_value, path = hooke_jeeves(x_start, h_start, accuracy, max_iter)
end = time.perf_counter_ns()
elapsed = end - start

print(f'Точка мінімуму: ({min_point})\nЗначення функції: {min_value}')
print(f'КОЦФ: {function_calls}')
print(f"Час виконання: {elapsed / 1_000_000_000:.6f} секунд")


# Візуалізація

x1_vals = np.linspace(-4, 4, 200)
x2_vals = np.linspace(-4, 4, 200)
X1, X2 = np.meshgrid(x1_vals, x2_vals)
Z = G(X1, X2)

path_x1 = []
path_x2 = []
path_G = []

for p in path:
    path_x1.append(p[0])
    path_x2.append(p[1])
    path_G.append(G(p[0], p[1]))

fig = plt.figure(figsize=(12, 5))

# 3D графік
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax1.plot_surface(X1, X2, Z, cmap=cm.coolwarm, alpha=0.6)
ax1.plot(path_x1, path_x2, path_G, color='g', ls="-", lw=0.5, marker='.', ms=3, label='Шлях спуску')
ax1.set_zlim(-80, 60)
ax1.set_xlabel('$x_1$')
ax1.set_ylabel('$x_2$')
ax1.set_zlabel('$G(x_1, x_2)$')
ax1.set_title('3Д поверхня + шлях спуску')
ax1.legend()

# Контурний графік
ax2 = fig.add_subplot(1, 2, 2)
contour = ax2.contour(X1, X2, Z, cmap=cm.coolwarm, levels=12, linestyles='dashed')
ax2.plot(path_x1, path_x2, color='g', ls="-", lw=0.5, marker='.', ms=3, label='Шлях спуску')
plt.colorbar(contour, ax=ax2)
ax2.set_xlabel('$x_1$')
ax2.set_ylabel('$x_2$')
ax2.set_title('Ізолінії + шлях спуску')
ax2.legend()

plt.tight_layout()
plt.show()
