
import math

def convert_time_to_fitness(time):
    min_time = 15
    max_time = 35

    # 使用指数的倒数
    # 随着时间减少，适应度会非线性增加
    normalized_time = (time - min_time) / (max_time - min_time)
    fitness = 1.0 / math.exp(normalized_time)

    return fitness

# 测试几个不同的时间值
times = [20, 30, 40,50,60,70,80,90, 100, 180]
fitness_values = [convert_time_to_fitness(time) for time in times]
print(fitness_values)
