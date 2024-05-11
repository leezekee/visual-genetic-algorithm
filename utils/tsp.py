import numpy as np
import random

from utils.graph import Graph

def load_distance_matrix(filename):
    # 首先，我们需要读取文件来确定城市数量
    city_set = set()
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            city_set.update(parts[:2])

    # 创建一个足够大的矩阵
    max_city = max(map(int, city_set))
    matrix = np.full((max_city + 1, max_city + 1), np.inf)
    np.fill_diagonal(matrix, 0)  # 将对角线上的值设置为0，因为城市到自己的距离为0

    # 再次读取文件来填充距离矩阵
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            i, j, dist = map(int, parts)
            matrix[i][j] = dist
            matrix[j][i] = dist  # 保证矩阵是对称的

    return matrix


def calculate_distance(path, distance_matrix):
    total_distance = 0
    for i in range(len(path)):
        total_distance += distance_matrix[path[i - 1]][path[i]]
    return total_distance


def fitness(path, distance_matrix):
    return 1 / calculate_distance(path, distance_matrix)


def select(population, scores, k=3):
    selection_probs = scores / scores.sum()
    selected_indices = np.random.choice(len(population), size=k, replace=False, p=selection_probs)
    return [population[i] for i in selected_indices]


def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [None] * len(parent1)
    child[start:end] = parent1[start:end]
    for i in range(start, end):
        if parent2[i] not in child:
            j = i
            while child[j] is not None:
                j = parent2.index(parent1[j])
            child[j] = parent2[i]
    for i in range(len(parent1)):
        if child[i] is None:
            child[i] = parent2[i]
    return child


def mutate(path, mutation_rate=0.1):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(path)), 2)
        path[i], path[j] = path[j], path[i]
    return path


def genetic_algorithm(filename, pop_size=100, generations=1000):
    # distance_matrix = load_distance_matrix(filename)
    graph = Graph()
    graph.load_distance_matrix(filename)
    distance_matrix = graph.matrix
    cities = distance_matrix.shape[0]
    population = [random.sample(range(1, cities), cities - 1) for _ in range(pop_size)]
    scores = np.array([fitness(p, distance_matrix) for p in population])

    for _ in range(generations):
        selected = select(population, scores)
        offspring = [mutate(crossover(selected[i % len(selected)], selected[(i + 1) % len(selected)])) for i in
                     range(pop_size)]
        population = offspring
        scores = np.array([fitness(p, distance_matrix) for p in population])

    best_idx = np.argmax(scores)
    return population[best_idx], 1 / scores[best_idx]


# 运行遗传算法
filename = 'data.txt'
best_path, best_distance = genetic_algorithm(filename)
print("Best path:", best_path)
print("Minimum distance:", best_distance)

