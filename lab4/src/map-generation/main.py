import random
import matplotlib.pyplot as plt
import csv

class Town:
    def __init__(self, x, y):
        self.location = [x, y]

    def print(self):
        print(f"location: [{self.location[0]},{self.location[1]}]")



X_RANGE = (-5000, 5000)
Y_RANGE = (-5000, 5000)


towns = []

for i in range (5000):
    x = random.randint(*X_RANGE)
    y = random.randint(*Y_RANGE)

    town = Town(x,y)
    towns.append(town)






# візуалізація
x_vals = [t.location[0] for t in towns]
y_vals = [t.location[1] for t in towns]

plt.scatter(x_vals, y_vals, s=1)
plt.title("Генеровані міста")
plt.xlabel("X координата")
plt.ylabel("Y координата")
plt.grid(True)
plt.show()


# Запис до файлу

with open("cities1.csv", mode="w", newline="") as file:
    writer = csv.writer(file, delimiter=';')  
    writer.writerow(["x", "y"])
    for town in towns:
        writer.writerow([town.location[0], town.location[1]])





