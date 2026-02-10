import random
import csv

class ADS:
    def __init__(self, x, y, radius):
        self.location = [x, y]
        self.radius = radius

    def print(self):
        print(f"location: [{self.location[0], self.location[1]}], radius: {self.radius}")


amount = random.randint(8,20)

ADSs = []

for i in range(amount):
    x = 0
    y = 0
    radius = random.uniform(10, 100)
    print(f"system {i} radius: {radius}")
    ADSs.append((x, y, radius))

# Зберігаємо набір систем у файл
with open("ADSs.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["x", "y", "radius"])
    for ads in ADSs:
        writer.writerow(ads)