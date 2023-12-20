import math
import matplotlib.pyplot as plt
import numpy as np
import math

def convert_time_to_fitness(time):
    min_time = 15 # just a hyperparameter
    max_time = 35 # just a hyperparameter
    normalized_time = (time - min_time) / (max_time - min_time)
    fitness = 1.0 / math.exp(normalized_time)

    return fitness

times = np.linspace(5, 200, 200)

fitness_values = [convert_time_to_fitness(time) for time in times]

plt.plot(times, fitness_values)
plt.xlabel('Time')
plt.ylabel('Fitness')
plt.title('Time to Fitness Conversion')
plt.savefig("./figure/fitness_function.png")
plt.show()


