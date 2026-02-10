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

# Генетичний алгоритм

def fitness(route):
    return find_E(route)


def build_population(cities, pop_size):
    population = []
    for _ in range(pop_size):
        population.append(nearest_neighbour(cities, 4))
    return population


def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))

    child = [None] * size
    child[start:end] = parent1[start:end]

    p2_filtered = [city for city in parent2 if city not in child]
    i = 0
    for j in range(size):
        if child[j] is None:
            child[j] = p2_filtered[i]
            i += 1

    return child

def mutation(route):
    a, b = random.sample(range(len(route)), 2)
    route[a], route[b] = route[b], route[a]
    return route


def tournament_selection(population, towns, k=3):
    selected = []
    for _ in range(len(population)):
        contenders = random.sample(population, k)
        best = min(contenders, key=lambda route: fitness(route))
        selected.append(best)
    return selected



def genetic_tsp(towns, pop_size, cross_prob, mut_prob, generations, patience, time_limit):
    population = build_population(towns, pop_size)
    best = min(population, key=fitness)
    best_score = fitness(best)
    start_time = time.time()
    no_improv = 0

    time_points = []
    E_points = []

    # plt.ion()
    # fig = plt.figure()

    for generation in range(generations):
        if time.time() - start_time > time_limit or no_improv >= patience:
            break

        new_population = []

        for _ in range(pop_size):
            p1, p2 = random.sample(population, 2)
            child = crossover(p1, p2) if random.random() < cross_prob else p1[:]
            if random.random() < mut_prob:
                child = mutation(child)
            new_population.append(child)

        population = tournament_selection(new_population, towns)

        current_best = min(population, key=fitness)
        current_score = fitness(current_best)

        if current_score < best_score:
            best = current_best
            best_score = current_score
            no_improv = 0
        else:
            no_improv += 1

        time_points.append(time.time() - start_time)
        E_points.append(best_score)
        # show_route_live(best)

        print(f"Gen {generation} | Best length: {best_score:.2f}")

    # plt.ioff()
    # plt.show()
    build_time_improvements_graphic(time_points, E_points)

    return best


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


result = genetic_tsp(cities50, pop_size=10, cross_prob=0.9, mut_prob=0.3, generations=500, patience=50, time_limit=60)
# show_route(result)
print(f"Best length: {find_E(result)}")
