import random
import matplotlib.pyplot as plt
import csv

class Town:
    def __init__(self, x, y, population):
        self.location = [x, y]
        self.population = population

    def print(self):
        print(f"location: [{self.location[0]},{self.location[1]}], population: {self.population}")


# Генерація набору даних
# Діапазон координат
X_RANGE = (-1000, 1000)
Y_RANGE = (-1000, 1000)


# Кількість кластерів кожного типу
clusters = {
    "big_dense": 2,
    "small_dense": 3,
    "big_sparse": 3,
    "small_sparse": 2,
}


towns = []


for cluster_type, count in clusters.items():

    for _ in range(count):

        # визначаємо точку на мапі, яка стане центром кластера
        center_x = random.uniform(*X_RANGE)
        center_y = random.uniform(*Y_RANGE)

        if "big" in cluster_type:
            num_towns = random.randint(200, 300)
        else:
            num_towns = random.randint(30, 70)

        for _ in range(num_towns):

            if "dense" in cluster_type:
                spread = random.randint(20, 50)
            else:
                spread = random.randint(250, 300)


            x = random.gauss(center_x, spread)
            y = random.gauss(center_y, spread)


            if "dense" in cluster_type:
                population = random.randint(500, 1000)
            else:
                population = random.randint(10, 300)

            towns.append((x, y, population))


print(f"amount of towns: {len(towns)}")



# візуалізація
x_vals = [t[0] for t in towns]
y_vals = [t[1] for t in towns]
population_sizes = [t[2] for t in towns]


plt.figure(figsize=(10, 10))
plt.scatter(x_vals, y_vals, s=[p / 10 for p in population_sizes], alpha=0.6)
plt.title("Генерація міст")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.show()


#Запис до файлу
with open("towns1.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["x", "y", "population"])
    for town in towns:
        writer.writerow(town)


