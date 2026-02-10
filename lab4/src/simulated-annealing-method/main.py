import random
import matplotlib.pyplot as plt
import csv
import time
import math


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


def nearest_neighbour(cities, index):
    unvisited = cities[:]
    route = []

    current_city = unvisited.pop(index)
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


# рандомний вибір індексів

def two_opt_optimization_random(route):
    n = len(route)

    i = random.randint(1, n - 3)
    j = random.randint(i + 1, n - 2)

    A = route[0:i + 1]
    B = route[i + 1:j + 1]
    C = route[j + 1:]

    candidate = A + B[::-1] + C

    return candidate


# алгоритм імітації відпалу

def annealing(route, time_limit, T, T_end, a):
    best_route = route[:]
    best_E = find_E(best_route)

    start_time = time.time()

    time_points = []
    E_points = []

    # plt.ion()
    # fig = plt.figure()

    while time.time() - start_time < time_limit and T > T_end:

        candidate = two_opt_optimization_random(best_route)
        candidate_E = find_E(candidate)

        dE = candidate_E - best_E

        if dE < 0:
            best_route = candidate
            best_E = candidate_E
        else:
            P = math.exp(-dE / T) # спробувати прибрати можливість вибору гіршого шляху
            if random.uniform(0, 1) < P:
                best_route = candidate
                best_E = candidate_E

        current_time = time.time() - start_time
        time_points.append(current_time)
        E_points.append(best_E)

        # show_route_live(best_route)

        T = T * a

    # plt.ioff()
    # plt.show()
    # build_time_improvements_graphic(time_points, E_points)

    return best_route, time_points, E_points


# повний перебір

def two_opt_algorithm_enum(route, time_limit):
    best_route = route[:]
    best_E = find_E(best_route)
    without_impr = 0
    improved = True
    n = len(route)

    time_points = []
    E_points = []

    # plt.ion()
    # fig = plt.figure()

    start_time = time.time()

    while time.time() - start_time < time_limit and without_impr < 10:
        improved = False
        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                A = best_route[:i]
                B = best_route[i:j + 1]
                C = best_route[j + 1:]

                candidate = A + B[::-1] + C
                candidate_E = find_E(candidate)

                if candidate_E < best_E:
                    best_route = candidate
                    best_E = candidate_E
                    # show_route_live(best_route)
                    improved = True
                    without_impr = 0

                    current_time = time.time() - start_time
                    time_points.append(current_time)
                    E_points.append(best_E)

                    break

            if improved:
                break
        if not improved:
            without_impr += 1

    # plt.ioff()
    # plt.show()
    # build_time_improvements_graphic(time_points, E_points)

    return best_route, time_points, E_points

# комбінація 2-opt та імітації відпалу

def two_opt_plus_annealing(route, time_limit, T, T_end, a):

    sa_time = time_limit * 0.9
    opt_time = time_limit * 0.1

    route_after_sa, sa_time_points, sa_E_points = annealing(route, sa_time, T, T_end, a)
    time_shift = sa_time_points[-1] if sa_time_points else 0

    final_route, opt_time_points, opt_E_points = two_opt_algorithm_enum(route_after_sa, opt_time)
    opt_time_points = [t + time_shift for t in opt_time_points]

    time_points = sa_time_points + opt_time_points
    E_points = sa_E_points + opt_E_points

    build_time_improvements_graphic(time_points, E_points)

    return final_route




def build_time_improvements_graphic(time_points, E_points):
    plt.figure()
    plt.plot(time_points, E_points, marker='o')
    plt.title("Залежність довжини найкращого маршруту від часу")
    plt.xlabel("Час (секунди)")
    plt.ylabel("Довжина маршруту")
    plt.grid(True)
    plt.show()


def show_route_live(route, color='blue', size=20):
    plt.clf()

    x_vals = [t[0] for t in route] + [route[0][0]]
    y_vals = [t[1] for t in route] + [route[0][1]]

    plt.plot(x_vals, y_vals, color=color, linewidth=2, label='Маршрут')
    plt.scatter(x_vals, y_vals, s=size, c='black', zorder=5, label='Міста')
    plt.scatter(x_vals[0], y_vals[0], s=size * 2, c='green', zorder=6, label='Початкове місто')
    plt.scatter(x_vals[-2], y_vals[-2], s=size * 2, c='red', zorder=6, label='Останнє місто')

    plt.title("Поточний найкращий маршрут")
    plt.xlabel("X координата")
    plt.ylabel("Y координата")
    plt.grid(True)
    plt.axis("equal")
    plt.legend()
    plt.pause(0.05)


def show_route(route, color='blue', size=20):
    x_vals = [t[0] for t in route] + [route[0][0]]
    y_vals = [t[1] for t in route] + [route[0][1]]

    plt.plot(x_vals, y_vals, color=color, linewidth=2, label='Маршрут')
    plt.scatter(x_vals, y_vals, s=size, c='black', zorder=5, label='Міста')
    plt.scatter(x_vals[0], y_vals[0], s=size * 2, c='green', zorder=6, label='Початкове місто')
    plt.scatter(x_vals[-2], y_vals[-2], s=size * 2, c='red', zorder=6, label='Останнє місто')

    plt.title("Візуалізація маршруту (найближчий сусід)")
    plt.xlabel("X координата")
    plt.ylabel("Y координата")
    plt.grid(True)
    plt.axis("equal")
    plt.legend()
    plt.show()


start_route = nearest_neighbour(cities20, 2)
route, e, p = annealing(start_route, 20, 100, 0, 0.99)
show_route(route)

E_start = find_E(start_route)
E = find_E(route)
print(f'Start length of route: {E_start}')
print(f'Best length of route: {E}')
