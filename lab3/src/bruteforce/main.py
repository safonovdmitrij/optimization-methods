import matplotlib.pyplot as plt
import matplotlib.patches as patches
import csv
import random

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
    covered = set() # місто може покриватися декількома системами, тому set (важливо враховувати 1 раз)

    for i, ads in enumerate(adss):
        for j, town in enumerate(towns):
            dx = ads.location[0] - town.location[0]
            dy = ads.location[1] - town.location[1]
            distance = (dx**2 + dy**2)**(1/2)
            if distance <= ads.radius:
                covered.add(j)

    return len(covered)

# Брутфорс

def evaluate_ads_coverage(ads, towns, already_covered):
    global call_count
    call_count += 1

    new_covered = set()


    for i, town in enumerate(towns):
        if i in already_covered:
            continue  # це місто вже покрите іншою системою

        dx = ads.location[0] - town.location[0]
        dy = ads.location[1] - town.location[1]
        distance = (dx**2 + dy**2)**0.5

        if distance <= ads.radius:
            new_covered.add(i)

    return new_covered  # повертаємо набір індексів міст, які покриває ця система


def brutforce(adss, towns):
    already_covered = set()

    for ads in adss:
        best_location = None
        best_covered = set()

        for _ in range(100):

            x = random.uniform(-1750, 1500)
            y = random.uniform(-1500, 1500)

            ads.location[0] = x
            ads.location[1] = y

            new_covered = evaluate_ads_coverage(ads, towns, already_covered)

            if(len(new_covered) > len(best_covered)):
                best_covered = new_covered
                best_location = (x, y)

        if(best_location):
            ads.location[0] = best_location[0]
            ads.location[1] = best_location[1]
            already_covered.update(best_covered)

    return adss

# Тестування

adss_final = brutforce(adss, towns)
result = optimality_lvl_1(adss_final, towns)
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
    circle = patches.Circle((ads.location[0], ads.location[1]), ads.radius, color = "red", alpha = 0.2, fill = True)
    ax.add_patch(circle)


ax.set_title("Мапа міст і систем ППО")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.grid(True)
ax.legend()
# plt.axis('equal')  # Щоб кола були кругами, а не еліпсами
plt.show()


