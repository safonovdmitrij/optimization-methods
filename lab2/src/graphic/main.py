import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def G(x1, x2):
    return 0.5 * ((np.pow(x1, 4) - 16 * np.pow(x1, 2) + 5 * x1) + (np.pow(x2, 4) - 16 * np.pow(x2, 2) + 5 * x2))


x1_vals = np.linspace(-4, 4, 100)
x2_vals = np.linspace(-4, 4, 100)
X1, X2 = np.meshgrid(x1_vals, x2_vals)
Z = G(X1, X2)

fig = plt.figure(figsize=(12, 5))

# 3Д графік
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax1.plot_surface(X1, X2, Z, cmap=cm.coolwarm)
ax1.set_zlim(-80, 60)
ax1.set_xlabel('$x_1$')
ax1.set_ylabel('$x_2$')
ax1.set_zlabel('$G(x_1, x_2)$')
ax1.set_title('3D surface')

# контурний графік
ax2 = fig.add_subplot(1, 2, 2)
contour = ax2.contour(X1, X2, Z, cmap=cm.coolwarm, levels=12, linestyles='dashed')
plt.colorbar(contour, ax=ax2)
ax2.set_xlabel('$x_1$')
ax2.set_ylabel('$x_2$')
ax2.set_title('level lines (isolines)')

plt.tight_layout()
plt.show()
