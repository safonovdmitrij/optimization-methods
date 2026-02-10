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


def random_permutation(towns):
    route = towns[:]
    random.shuffle(route)
    return route

def brute_force(towns, duration):
    best_route = None
    best_E = float('inf')
    start_time = time.time()

    time_points = []
    E_points = []

    # plt.ion()
    # fig = plt.figure()

    while time.time() - start_time < duration:
        route = random_permutation(towns)
        E = find_E(route)

        if E < best_E:
            best_E = E
            best_route = route[:]
            current_time = time.time() - start_time
            time_points.append(current_time)
            E_points.append(best_E)

            # show_route_live(best_route)

    print(f'Best length: {best_E}')
    # plt.ioff()
    # plt.show()

    build_time_improvments_graphic(time_points, E_points)

    return best_route, best_E

def show_route_live(route, color='green', size=20):
    plt.clf()

    x_vals = [t[0] for t in route] + [route[0][0]]
    y_vals = [t[1] for t in route] + [route[0][1]]

    plt.plot(x_vals, y_vals, color=color, linewidth=2, label="Маршрут")
    plt.scatter(x_vals, y_vals, s=size, c='black', zorder=5)
    plt.title("Поточний найкращий маршрут")
    plt.xlabel("X координата")
    plt.ylabel("Y координата")
    plt.grid(True)
    plt.axis("equal")
    plt.legend()
    plt.pause(0.5)



def build_time_improvments_graphic(time_points, E_points):
    plt.figure()
    plt.plot(time_points, E_points, marker='o')
    plt.title("Залежність довжини найкращого маршруту від часу")
    plt.xlabel("Час (секунди)")
    plt.ylabel("Довжина маршруту")
    plt.grid(True)
    plt.show()


def show_route(route, color='blue', size=20):
    x_vals = [t[0] for t in route] + [route[0][0]]
    y_vals = [t[1] for t in route] + [route[0][1]]

    plt.plot(x_vals, y_vals, color=color, linewidth=2, label='Маршрут')
    plt.scatter(x_vals, y_vals, s=size, c='black', zorder=5, label='Міста')
    plt.scatter(x_vals[0], y_vals[0], s=size * 2, c='green', zorder=6, label='Початкове місто')
    plt.scatter(x_vals[-2], y_vals[-2], s=size * 2, c='red', zorder=6, label='Останнє місто')

    plt.title("Візуалізація маршруту (brute force)")
    plt.xlabel("X координата")
    plt.ylabel("Y координата")
    plt.grid(True)
    plt.axis("equal")
    plt.legend()
    plt.show()


route, E = brute_force(cities, 60)
show_route(route)




