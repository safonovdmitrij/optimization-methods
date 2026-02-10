import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import time

function_calls = 0


# Styblinski–Tang function
#
# Область визначення
# x1_vals = np.linspace(-5, 5, 400)
# x2_vals = np.linspace(-5, 5, 400)
#
# def G(x1, x2):
#     global function_calls
#     function_calls += 1
#     return 0.5 * ((x1 ** 4 - 16 * x1 ** 2 + 5 * x1) + (x2 ** 4 - 16 * x2 ** 2 + 5 * x2))


# Goldstein-Price function
#
# Область визначення
# x1_vals = np.linspace(-2, 2, 400)
# x2_vals = np.linspace(-2, 2, 400)
def G(x, y):
    global function_calls
    function_calls += 1
    term1 = 1 + (x + y + 1)**2 * (19 - 14*x + 3*x**2 - 14*y + 6*x*y + 3*y**2)
    term2 = 30 + (2*x - 3*y)**2 * (18 - 32*x + 12*x**2 + 48*y - 36*x*y + 27*y**2)
    return term1 * term2

def golden_ratio(f, a, b, eps):
    l = b - a
    x1 = a + 0.382 * l
    x2 = a + 0.618 * l
    g1 = f(x1)
    g2 = f(x2)

    while b - a > eps:
        if g1 > g2:
            a = x1
            l = b - a
            x1 = x2
            g1 = g2
            x2 = a + 0.618 * l
            g2 = f(x2)
        elif g1 < g2:
            b = x2
            l = b - a
            x2 = x1
            g2 = g1
            x1 = a + 0.382 * l
            g1 = f(x1)
        else:
            a = x1
            b = x2
            l = b - a
            x1 = a + 0.382 * l
            x2 = a + 0.618 * l
            g1 = f(x1)
            g2 = f(x2)

    return (a + b) / 2

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


def fletcher_reeves(x1, x2, accuracy, delta, max_iter):
    path = [(x1, x2)]
    # Обчислюємо градієнт ьа задаємо початковий напрямок

    grad_x1, grad_x2 = central_differences(x1, x2, delta)
    d_x1, d_x2 = -grad_x1, -grad_x2

    for i in range(max_iter):

        # одновимірна функція, яка описує значення початкової функції G вздовж напрямку d = (d_x1, d_x2)
        def phi(lam):
            return G(x1 + lam * d_x1, x2 + lam * d_x2)

        lam = golden_ratio(phi, 0, 0.0009, accuracy)

        # переходимо в нову точку
        x1_new = x1 + lam * d_x1
        x2_new = x2 + lam * d_x2

        old_grad_x1 = grad_x1
        old_grad_x2 = grad_x2
        q = old_grad_x1 ** 2 + old_grad_x2 ** 2

        grad_x1, grad_x2 = central_differences(x1_new, x2_new, delta)

        p = grad_x1 ** 2 + grad_x2 ** 2

        if q == 0:
            print(f'Ділення на 0')
            break

        b = p/q

        d_x1 = -grad_x1 + b * d_x1
        d_x2 = -grad_x2 + b * d_x2

        if np.sqrt((x1_new - x1)**2 + (x2_new - x2)**2) < accuracy:
            print(f'Метод зійшовся за {i + 1} ітерацій')
            break

        x1, x2 = x1_new, x2_new

        path.append((x1, x2))

    return x1, x2, G(x1, x2), path





# Початкові значення
x_start = [-1.4, 0]
delta = 0.0001
alpha = 0.05
accuracy = 0.0000001
max_iter = 1000

# print(f"Метод найщвидшого спсуску:")
#
# start1 = time.perf_counter_ns()
# x1_fin, x2_fin, G_fin, path_gd = gradient_descent(x_start[0], x_start[1], alpha, delta, accuracy, max_iter)
# end1 = time.perf_counter_ns()
# elapsed1 = end1 - start1
#
# print(f'Точка мінімуму: ({x1_fin},{x2_fin})\nЗначення функції: {G_fin}')
# print(f'КОЦФ: {function_calls}')
# print(f"Час виконання: {elapsed1 / 1_000_000_000:.6f} секунд")
#


print(f"Метод Флетчера-Рівса:")


function_calls = 0
start = time.perf_counter_ns()
x1_fin, x2_fin, G_fin, path_fr = fletcher_reeves(x_start[0], x_start[1], delta, accuracy, max_iter)
end = time.perf_counter_ns()
elapsed = end - start

print(f'Точка мінімуму: ({x1_fin},{x2_fin})\nЗначення функції: {G_fin}')
print(f'КОЦФ: {function_calls}')
print(f"Час виконання: {elapsed / 1_000_000_000:.6f} секунд")

# Візуалізація

x1_vals = np.linspace(-2, 2, 400)
x2_vals = np.linspace(-2, 2, 400)
X1, X2 = np.meshgrid(x1_vals, x2_vals)
Z = G(X1, X2)

# # Для найшвидшого спуску
# path_x1_gd = [p[0] for p in path_gd]
# path_x2_gd = [p[1] for p in path_gd]
# path_G_gd = [G(p[0], p[1]) for p in path_gd]

# Для Флетчера-Рівса
path_x1_fr = [p[0] for p in path_fr]
path_x2_fr = [p[1] for p in path_fr]
path_G_fr = [G(p[0], p[1]) for p in path_fr]


fig = plt.figure(figsize=(12, 5))

# 3D графік
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax1.plot_surface(X1, X2, Z, cmap=cm.winter_r, alpha=0.4)
# ax1.plot(path_x1_gd, path_x2_gd, path_G_gd, color='black', label='Найшвидший спуск', marker='.')
ax1.plot(path_x1_fr, path_x2_fr, path_G_fr, color='red', label='Флетчера–Рівса', marker='.')
ax1.set_zlim(np.min(Z), np.max(Z))
ax1.set_xlabel('$x_1$')
ax1.set_ylabel('$x_2$')
ax1.set_zlabel('$G(x_1, x_2)$')
ax1.set_title('3Д поверхня')
ax1.legend()


# Контурний графік
ax2 = fig.add_subplot(1, 2, 2)
contour = ax2.contour(X1, X2, Z, cmap=cm.winter_r, levels=40, linestyles='dashed')
# ax2.plot(path_x1_gd, path_x2_gd, color='black', label='Найшвидший спуск', marker='.')
ax2.plot(path_x1_fr, path_x2_fr, color='red', label='Флетчера–Рівса', marker='.')
plt.colorbar(contour, ax=ax2)
ax2.set_xlabel('$x_1$')
ax2.set_ylabel('$x_2$')
ax2.set_title('Ізолінії')
ax2.legend()

plt.tight_layout()
plt.show()
