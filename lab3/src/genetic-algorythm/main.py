import matplotlib.pyplot as plt
import matplotlib.patches as patches
import csv
import random
import time

# вхідні дані
call_count = 0  # глобальний лічильник

class Town:
    def __init__(self, x, y, population):
        self.location = [x, y]
        self.population = population

    def print(self):
        print(f"location: [{self.location[0]},{self.location[1]}], population: {self.population}")


class ADS:
    def __init__(self, x, y, radius):
        self.location = [x, y]
        self.radius = radius

    def print(self):
        print(f"location: [{self.location[0], self.location[1]}], radius: {self.radius}")


adss = []
towns = []

with open("towns1.csv", mode="r") as file:
    reader = csv.reader(file)
    next(reader)  # Пропускаємо заголовок

    for row in reader:
        x = float(row[0])
        y = float(row[1])
        population = int(row[2])

        town = Town(x, y, population)
        towns.append(town)

with open("ADSs.csv", mode="r") as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        x = float(row[0])
        y = float(row[1])
        radius = float(row[2])

        ads = ADS(x, y, radius)
        adss.append(ads)


# Цільова функція

def optimality_lvl_1(adss, towns):
    global call_count
    call_count += 1

    covered = set()
    for i, ads in enumerate(adss):
        for j, town in enumerate(towns):
            dx = ads.location[0] - town.location[0]
            dy = ads.location[1] - town.location[1]
            distance = (dx ** 2 + dy ** 2) ** (1 / 2)
            if distance <= ads.radius:
                covered.add(j)

    return len(covered)


# цільова функція для одної системи

def optimality_single(ads, towns):
    global call_count
    call_count += 1

    covered = set()
    for i, town in enumerate(towns):
        dx = ads.location[0] - town.location[0]
        dy = ads.location[1] - town.location[1]
        distance = (dx ** 2 + dy ** 2) ** (1 / 2)
        if distance <= ads.radius:
            covered.add(i)

    return len(covered)


# Генетичний алгоритм

def build_population(template_adss, population_size):
    population = []

    for _ in range(population_size):
        individual = []

        for ads in template_adss:
            x = random.uniform(-1500, 1500)
            y = random.uniform(-1500, 1500)
            radius = ads.radius

            new_ads = ADS(x, y, radius)
            individual.append(new_ads)

        population.append(individual)

    return population


# Проходимось по спискам та для кожної ппо схрещуємо координати, і на виході отримуємо хромосому нащадка

def crossover(ancestor1, ancestor2):
    descendant = []

    for i in range(len(ancestor1)):
        # # Перша стратегія схрещування
        # x = ancestor1[i].location[0]
        # y = ancestor2[i].location[1]

        # # Друга стратегія (усереднення)
        # x = (ancestor1[i].location[0] + ancestor2[i].location[0]) / 2
        # y = (ancestor1[i].location[1] + ancestor2[i].location[1]) / 2

        # Можна також комбінувати першу і другу стратегії
        if random.randint(0, 1):
            x = ancestor1[i].location[0]
            y = ancestor2[i].location[1]
        else:
            x = (ancestor1[i].location[0] + ancestor2[i].location[0]) / 2
            y = (ancestor1[i].location[1] + ancestor2[i].location[1]) / 2

        radius = ancestor2[i].radius

        new_ads = ADS(x, y, radius)
        descendant.append(new_ads)

    return descendant


# Функції для ін/аутбрідінгу

def count_chromosome_distance(set1, set2):
    total = 0

    for i in range(len(set1)):
        dx = set1[i].location[0] - set2[i].location[0]
        dy = set1[i].location[1] - set2[i].location[1]
        dist = (dx ** 2 + dy ** 2) ** (1 / 2)
        total += dist
    return total


def find_same(population, set1):
    i2 = 0
    minimum = float("inf")

    for i in range(len(population)):
        dif = count_chromosome_distance(population[i], set1)
        if dif < minimum:
            minimum = dif
            i2 = i

    return i2


def find_different(population, set1):
    i2 = 0
    maximum = float("-inf")

    for i in range(len(population)):
        dif = count_chromosome_distance(population[i], set1)
        if dif > maximum:
            maximum = dif
            i2 = i

    return i2


# Мутація

def mutation(descendant):
    i = random.randint(0, len(descendant) - 1)

    # стратегія 1 - рандомно обрати одну з координат
    if random.randint(0, 1):
        descendant[i].location[0] = random.uniform(-1500, 1500)
    else:
        descendant[i].location[1] = random.uniform(-1500, 1500)

    # # стратегія 2 - зсунути координату
    # delta = random.uniform(-100, 100)
    #
    # if random.randint(0, 1):
    #     descendant[i].location[0] += delta
    # else:
    #     descendant[i].location[1] += delta

    return descendant


# Схрещування

def crossbreeding(population, crossbreeding_probability, mutation_probability, amount_of_descendants):
    population_size = len(population)
    new_generation = []

    for _ in range(amount_of_descendants):

        if random.randint(0, 100) / 100 < crossbreeding_probability:

            # # Панміксія (обидва батьки обираються випадково)
            # i1 = random.randint(0, population_size - 1)
            # i2 = random.randint(0, population_size - 1)
            #
            # ancestor1 = population[i1]
            # ancestor2 = population[i2]

            # # Інбрідінг (перший - випадково, другий - найбільш схожим (схожість - схожість координат))
            # i1 = random.randint(0, population_size - 1)
            # ancestor1 = population[i1]
            #
            # i2 = find_same(population, ancestor1)
            # ancestor2 = population[i2]
            #
            # Аутбрідінг (перший - випадково, другий - найменш схожим)
            i1 = random.randint(0, population_size - 1)
            ancestor1 = population[i1]

            i2 = find_different(population, ancestor1)
            ancestor2 = population[i2]

            descendant = crossover(ancestor1, ancestor2)

            # Мутація

            if random.randint(0, 100) / 100 < mutation_probability:
                descendant = mutation(descendant)

            new_generation.append(descendant)

    return new_generation


# Селекція

def top_selection(population, pop_size, new_generation, towns):
    elite = []
    children = []
    parent_scores = []

    elite_size = int(pop_size * 0.2)
    children_size = pop_size - elite_size

    for individual in population:
        score = optimality_lvl_1(individual, towns)
        parent_scores.append((individual, score))

    parent_scores.sort(key=lambda x: x[1], reverse=True)

    elite = [pair[0] for pair in parent_scores[:elite_size]]

    new_children_count = min(children_size, len(new_generation))
    for _ in range(new_children_count):
        index = random.randint(0, len(new_generation) - 1)
        children.append(new_generation.pop(index))

    while len(children) < children_size:
        backup_index = elite_size + (len(children) % (pop_size - elite_size))
        children.append(parent_scores[backup_index][0])

    return elite + children



def tournament_selection(population, pop_size, new_generation, towns):

    new_population = []
    population += new_generation
    num_of_comparison = len(population) // 2

    for i in range(num_of_comparison):
        i1 = random.randint(0, len(population) - 1)
        i2 = random.randint(0, len(population) - 1)

        value1 = optimality_lvl_1(population[i1], towns)
        value2 = optimality_lvl_1(population[i2], towns)

        if value1 > value2:
            winner = population[i1]
        else:
            winner = population[i2]

        new_population.append(winner)

    return new_population

def roulette_selection(population, pop_size, new_generation, towns):

    population += new_generation

    scores = []
    for chromosome in population:
        score = optimality_lvl_1(chromosome, towns)
        scores.append(score)

    total_score = 0
    for score in scores:
        total_score += score

    probabilities = []
    for score in scores:
        prob = score / total_score
        probabilities.append(prob)


    selected = []
    for _ in range(pop_size):
        r = random.random()
        cumulative = 0
        for i in range(len(population)):
            cumulative += probabilities[i]
            if r <= cumulative:
                selected.append(population[i])
                break

    return selected



def selection(population, pop_size, new_generation, towns):
    # # Топ найкращих
    # return top_selection(population, pop_size, new_generation, towns)

    # Турнірна селекція
    return tournament_selection(population, pop_size, new_generation, towns)

    # # Метод рулетки
    # return roulette_selection(population, pop_size, new_generation, towns)

# Перевірка досягнення результату

def find_best_chromosome(population, towns):
    best_score = 0
    best_chromosome = population[0]

    for individual in population:
        score = optimality_lvl_1(individual, towns)
        if score > best_score:
            best_score = score
            best_chromosome = individual

    return best_chromosome, best_score



# Генетичний алгоритм


def genetic(adss, towns, pop_size, cross_prob, mut_prob, amount_of_generations, target_score, patience, time_limit_sec):
    # 1 Генерція початкової популяції
    population = build_population(adss, pop_size)
    amount_of_descendants = pop_size

    best_score = 0
    best_chromosome = None
    generations_without_improvement = 0

    start_time = time.time()

    for generation in range(amount_of_generations):
        # 2 Схрещування / мутація
        descendants = crossbreeding(population, cross_prob, mut_prob, amount_of_descendants)

        # 3 Селекція  і формування нового покоління
        population = selection(population, pop_size, descendants, towns)

        # 5 Перевірка досягнення результату
        # Пошук найкразого представника
        current_best, current_score = find_best_chromosome(population, towns)

        # Умова 1: Досягнуто заданого значення
        if current_score >= target_score:
            print(f"Знайдено ціль на {generation + 1}-му поколінні")
            best_chromosome = current_best
            best_score = current_score
            break

        # Умова 2 — немає покращень K поколінь
        if current_score > best_score:
            best_score = current_score
            best_chromosome = current_best
            generations_without_improvement = 0
        else:
            generations_without_improvement += 1

        if generations_without_improvement >= patience:
            print(f"Зупинка через відсутність покращень {patience} поколінь")
            break

        # Умова 3 — досягнення максимальної кількості поколінь
        if generation == amount_of_generations - 1:
            print("Досягнуто максимальної кількості поколінь")

        # Умова 4 — перевищено час
        if time.time() - start_time > time_limit_sec:
            print("Перевищено ліміт часу")
            break

        # log
        print(f"generation {generation} best_score: {best_score}")

    return best_chromosome, best_score

# Тестування



# population = build_population(adss, 10)
# new_generation = crossbreeding(population, 0.9, 0.1, 100)
# population = selection(population, 10, new_generation, towns)
#
#
# for i in range(len(descendants)):
#     print(f"n: {i}")
#     chromosome = descendants[i]
#     for i in range(18):
#        chromosome[i].print()

adss_final, result = genetic(adss, towns, 20, 0.9, 0.2, 10000, 1000, 500, 600)
print(f"Загальна кількість покритих міст: {result}, КОЦФ: {call_count}")

# візуалізація

x_towns = [t.location[0] for t in towns]
y_towns = [t.location[1] for t in towns]
population_sizes = [t.population for t in towns]

fig, ax = plt.subplots(figsize=(10, 10))
# вивід міст
ax.scatter(x_towns, y_towns, s=[p / 10 for p in population_sizes], alpha=0.6, label="Міста")

# вивід ППО
for ads in adss_final:
    circle = patches.Circle((ads.location[0], ads.location[1]), ads.radius, color="red", alpha=0.2, fill=True)
    ax.add_patch(circle)


ax.set_title("Мапа міст і систем ППО")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.grid(True)
ax.legend()
# plt.axis('equal')  # Щоб кола були кругами, а не еліпсами
plt.show()
