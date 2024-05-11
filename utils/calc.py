import random

import numpy as np
from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal


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


def genetic_algorithm(graph, pop_size=100, generations=1000):
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


class CalcThread(QThread):
	"""线程函数"""

	onEpochChanged = pyqtSignal(list)
	onCalcFinished = pyqtSignal([list, int])
	onFinished = pyqtSignal()

	def __init__(self, graph=None):
		"""构造函数"""
		super().__init__()
		self.is_running = True
		self.graph = graph

	def isrun(self, value: bool):
		self.is_running = value

	def run(self):
		for i in range(50):
			self.onEpochChanged.emit([i, i, i])
		self.onFinished.emit()
		print(self.graph.matrix)
		best_path, best_distance = genetic_algorithm(self.graph)
		self.onCalcFinished.emit(best_path, best_distance)


	def stop(self):
		self.is_running = False

