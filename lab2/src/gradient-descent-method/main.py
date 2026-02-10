import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time

function_calls = 0

def G(x1, x2):
    global function_calls
    function_calls += 1
    return 0.5 * ((np.pow(x1, 4) - 16 * np.pow(x1, 2) + 5 * x1) + (np.pow(x2, 4) - 16 * np.pow(x2, 2) + 5 * x2))


def central_differences(x1, x2, delta):
    derivative_x1 = (G(x1 + delta, x2) - G(x1 - delta, x2)) / (2 * delta)
    derivative_x2 = (G(x1, x2 + delta) - G(x1, x2 - delta)) / (2 * delta)
    return derivative_x1, derivative_x2


def gradient_descent(x1, x2, alpha, delta, accuracy, max_iter):
    path = [(x1, x2)]

    for i in range(max_iter):
        grad_x1, grad_x2 = central_differences(x1, x2, delta)

        x1_new = x1 - alpha * grad_x1
        x2_new = x2 - alpha * grad_x2

        path.append((x1_new, x2_new))

        if np.sqrt((x1_new - x1) ** 2 + (x2_new - x2) ** 2) < accuracy:
            print(f'Метод зійшовся за {i + 1} ітерацій')
            break

        x1, x2 = x1_new, x2_new

    return x1, x2, G(x1, x2), path


# Початкові значення
x_start = [0, 0]
delta = 0.0001
alpha = 0.04 # поексперементувати зі значенням
accuracy = 0.0001
max_iter = 1000

start = time.perf_counter_ns()
x1_fin, x2_fin, G_fin, path = gradient_descent(x_start[0], x_start[1], alpha, delta, accuracy, max_iter)
end = time.perf_counter_ns()
elapsed = end - start

print(f'Точка мінімуму: ({x1_fin},{x2_fin})\nЗначення функції: {G_fin}')
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
