import random
import matplotlib.pyplot as plt
import numpy as np
import csv
import os
from pathlib import Path

class x_y_cost_stats:
    def __init__(self):
        self.max_x = None
        self.min_x = None
        self.sum_x = 0

        self.max_y = None
        self.min_y = None
        self.sum_y = 0

        self.max_cost = None
        self.min_cost = None
        self.sum_cost = 0

        self.i = 0

    def add_x_y_cost(self, x, y, cost):
        self.sum_x += x

        if self.max_x == None or x > self.max_x:
            self.max_x = x
        
        if self.min_x == None or x < self.min_x:
            self.min_x = x

        self.sum_y += y

        if self.max_y == None or y > self.max_y:
            self.max_y = y
        
        if self.min_y == None or y < self.min_y:
            self.min_y = y

        self.sum_cost += cost

        if self.max_cost == None or cost > self.max_cost:
            self.max_cost = cost

        if self.min_cost == None or cost < self.min_cost:
            self.min_cost = cost

        self.i += 1

    def get_avg_x(self):
        return self.sum_x / self.i

    def get_avg_y(self):
        return self.sum_y / self.i

    def get_avg_cost(self):
        return self.sum_cost / self.i

class SimulatedAnnealing:
    def __init__(self, temp, cooling_rate, iterations, local_searches, multiplier, function_name,
                 lower_bound_x, upper_bound_x,lower_bound_y, upper_bound_y):
        self.temperature_0 = temp
        self.temperature = temp
        self.cooling_rate = cooling_rate
        self.iterations = iterations
        self.local_searches = local_searches
        self.multiplier = multiplier
        self.function_name = function_name
        self.lower_bound_x = lower_bound_x
        self.upper_bound_x = upper_bound_x
        self.lower_bound_y = lower_bound_y
        self.upper_bound_y = upper_bound_y
        self.history = []
        self.acceptance_probability_history = []

    def starting_point(self):
        x = random.uniform(self.lower_bound_x, self.upper_bound_x)
        y = random.uniform(self.lower_bound_y, self.upper_bound_y)
        return x, y

    def neighbour(self, x, y, multiplier=1.0):
        if multiplier == 1.0:
            return (x + random.uniform(-1, 1) * self.temperature / self.temperature_0,
                    y + random.uniform(-1, 1) * self.temperature / self.temperature_0)
        return x + random.uniform(-1, 1) * multiplier, y + random.uniform(-1, 1) * multiplier

    def himmelblau_function(self, x, y):
        return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2

    def ackley_function(self, x, y):
        return (-20 * np.exp(-0.2 * np.sqrt(0.5 * (x ** 2 + y ** 2))) -
                np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)))) + np.e + 20

    def beale_function(self, x, y):
        return ((1.5 - x + x * y) ** 2 + (2.25 - x + x * y ** 2) ** 2 + (2.625 - x + x * y ** 3) ** 2)

    def levi_function_13(self, x, y):
        return np.sin(3 * np.pi * x) ** 2 + (x - 1) ** 2 * (1 + np.sin(3 * np.pi * y) ** 2) + (y - 1) ** 2 * (1 + np.sin(2 * np.pi * y) ** 2)

    def choose_function(self, function_name, x, y):
        match function_name:
            case 'himmelblau':
                return self.himmelblau_function(x, y)
            case 'ackley':
                return self.ackley_function(x, y)
            case 'beale':
                return self.beale_function(x, y)
            case 'levi':
                return self.levi_function_13(x, y)
            case _:
                return self.himmelblau_function(x, y)

    def acceptance_probability(self, old_cost, new_cost):
        np.seterr(divide="ignore")
        if new_cost < old_cost:
            return 1.0
        else:
            prob = 0.5
            try:
                prob = 1 / (1 + np.exp((new_cost - old_cost) / self.temperature))
            except:
                pass
            return prob

    def optimize(self):
        x, y = self.starting_point()
        current_cost = self.choose_function(self.function_name, x, y)
        self.history.append((x, y))

        # while self.temperature > 1:
        for iteration in range(self.iterations):
            new_x, new_y = self.neighbour(x, y, self.multiplier[0])
            new_cost = self.choose_function(self.function_name, new_x, new_y)
            acc_prob = self.acceptance_probability(current_cost, new_cost)
            if acc_prob > random.random():
                x, y = new_x, new_y
                current_cost = new_cost
                self.acceptance_probability_history.append(acc_prob)
                self.history.append((x, y))

            for neighbour in range(self.local_searches):
                new_x, new_y = self.neighbour(x, y, self.multiplier[1])
                new_cost = self.choose_function(self.function_name, new_x, new_y)
                acc_prob = self.acceptance_probability(current_cost, new_cost)
                if acc_prob > random.random():
                    x, y = new_x, new_y
                    current_cost = new_cost
                    self.acceptance_probability_history.append(acc_prob)
                    self.history.append((x, y))

            self.temperature *= self.cooling_rate

        return x, y, current_cost

    def plot(self):
        x = np.linspace(-6, 6, 400)
        y = np.linspace(-6, 6, 400)
        x, y = np.meshgrid(x, y)
        z = self.choose_function(self.function_name, x, y)

        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(1, 2, 1, projection='3d')
        ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')

        hx, hy = zip(*self.history)
        hz = [self.choose_function(self.function_name, x, y) for x, y in self.history]
        ax.plot(hx, hy, hz, color='r', marker='.', markersize=5, linestyle='-', linewidth=1)

        final_x, final_y = self.history[-1]
        final_z = self.choose_function(self.function_name, final_x, final_y)
        ax.text2D(0.2, -0.05, f"Optimum: x= {final_x:.4f}, y= {final_y:.4f}, f(x, y)= {final_z:.4f}",
                   transform=ax.transAxes)

        ax2 = fig.add_subplot(2, 2, 2)
        ax2.plot(self.acceptance_probability_history, color='r', marker='.', linestyle='-', linewidth=1)
        ax2.set_title('Acceptance Probability Evolution')
        ax2.set_xlabel('Iteration')
        ax2.set_ylabel('Acceptance Probability')

        ax3 = fig.add_subplot(2, 2, 4)
        ax3.plot(hz, color='g', marker='.', linestyle='-', linewidth=1)
        ax3.set_title('Solution History')
        ax3.set_xlabel('Iteration')
        ax3.set_ylabel('Function value')

        plt.tight_layout()

        plt.show()
        plt.close()

if __name__ == '__main__':
    levi_params = {
        'temp': 1000,
        'cooling_rate': 0.95,
        'iterations': 400,
        'local_searches': 25,
        'multiplier': [0.5, 0.1],
        'function_name': 'levi',
        'lower_bound_x': -10,
        'upper_bound_x': 10,
        'lower_bound_y': -10,
        'upper_bound_y': 10
    }

    p = levi_params

    # Parametri x, y

    all_x = []
    all_max_x = []
    all_min_x = []

    all_y = []
    all_max_y = []
    all_min_y = []

    all_cost = []
    all_max_cost = []
    all_min_cost = []

    val = []

    for i in range(100, 1001, 50):
        stats = x_y_cost_stats()
        val.append(i)

        for j in range(1000):
            sa = SimulatedAnnealing(
                i, p['cooling_rate'], p['iterations'], p['local_searches'],
                p['multiplier'], p['function_name'],
                p['lower_bound_x'], p['upper_bound_x'],
                p['lower_bound_y'], p['upper_bound_y']
                )
            
            x, y, cost = sa.optimize()

            stats.add_x_y_cost(x, y, cost)
        
        all_x.append(stats.get_avg_x())
        all_max_x.append(stats.max_x)
        all_min_x.append(stats.min_x)

        all_y.append(stats.get_avg_y())
        all_max_y.append(stats.max_y)
        all_min_y.append(stats.min_y)

        all_cost.append(stats.get_avg_cost())
        all_max_cost.append(stats.max_cost)
        all_min_cost.append(stats.min_cost)
    
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    ax1.set_title("Y")
    ax1.plot(val, all_x, marker = '.')
    ax1.plot(val, all_max_x, color = 'g', linestyle = '--', marker = '.')
    ax1.plot(val, all_min_x, color = 'r', linestyle = '--', marker = '.')
    ax1.set_xticks(val)

    ax2.set_title("X")
    ax2.plot(val, all_y, marker = '.')
    ax2.plot(val, all_max_y, color = 'g', linestyle = '--', marker = '.')
    ax2.plot(val, all_min_y, color = 'r', linestyle = '--', marker = '.')
    ax2.set_xticks(val)

    ax3.set_title("Cost")
    ax3.plot(val, all_cost, marker = '.')
    ax3.plot(val, all_max_cost, color = 'g', linestyle = '--', marker = '.')
    ax3.set_xticks(val)

    print(f"Val: {val}")
    print(f"X: {all_x}")
    print(f"X: {all_max_x}")
    print(f"X: {all_min_x}")
    print(f"Y: {all_y}")
    print(f"Y: {all_max_y}")
    print(f"Y: {all_min_y}")
    print(f"Cost: {all_cost}")
    print(f"Cost: {all_max_cost}")

    with open(Path(os.path.dirname(os.path.realpath(__file__)), 'temp_val.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        field = [''] + val

        writer.writerow(field)
        writer.writerow(['Avg X'] + all_x)
        writer.writerow(['Max X'] + all_max_x)
        writer.writerow(['Min X'] + all_min_x)
        writer.writerow([''])
        writer.writerow(['Avg Y'] + all_y)
        writer.writerow(['Max Y'] + all_max_y)
        writer.writerow(['Min Y'] + all_min_y)
        writer.writerow([''])
        writer.writerow(['Avg Cost'] + all_cost)
        writer.writerow(['Max Cost'] + all_max_cost)

    plt.show()
