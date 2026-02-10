import random
import matplotlib.pyplot as plt
import csv
import time


class Town:
    def __init__(self, x, y):
        self.location = [x, y]

    def print(self):
        print(f"location: [{self.location[0]},{self.location[1]}]")


cities = []

with open("cities1.csv", newline='') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)
    for row in reader:
        x = int(row[0])
        y = int(row[1])
        cities.append((x, y))

cities20 = cities[:20]
cities50 = cities[:50]
cities100 = cities[:100]
cities1000 = cities[:1000]


def find_distance(city1, city2):
    dx = city1[0] - city2[0]
    dy = city1[1] - city2[1]
    dist = (dx ** 2 + dy ** 2) ** (1 / 2)
    return dist


def find_E(route):
    E = 0

    for i in range(len(route) - 1):
        E += find_distance(route[i], route[i + 1])

    E += find_distance(route[len(route) - 1], route[0])

    return E


def nearest_neighbour(cities, start_index):
    unvisited = cities[:]
    route = []

    current_city = unvisited.pop(start_index)
    route.append(current_city)

    while unvisited:
        nearest = None
        best_dist = float('inf')

        for city in unvisited:
            dist = find_distance(current_city, city)
            if dist < best_dist:
                best_dist = dist
                nearest = city

        route.append(nearest)
        unvisited.remove(nearest)
        current_city = nearest

    return route


def show_route(route, color='blue', size=20):

    x_vals = [t[0] for t in route] + [route[0][0]]
    y_vals = [t[1] for t in route] + [route[0][1]]

    plt.plot(x_vals, y_vals, color=color, linewidth=2, label='Маршрут')
    plt.scatter(x_vals, y_vals, s=size, c='black', zorder=5, label='Міста')
    plt.scatter(x_vals[0], y_vals[0], s=size*2, c='green', zorder=6, label='Початкове місто')
    plt.scatter(x_vals[-2], y_vals[-2], s=size*2, c='red', zorder=6, label='Останнє місто')

    plt.xlabel("X координата")
    plt.ylabel("Y координата")
    plt.grid(True)
    plt.axis("equal")
    plt.legend()
    plt.title("Візуалізація маршруту (найближчий сусід)")
    plt.show()



route = nearest_neighbour(cities, 0)
# show_route(route)
E = find_E(route)
print(f'Best length of route: {E}')
