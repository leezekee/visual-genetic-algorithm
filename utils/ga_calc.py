import random

import numpy as np
from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal


def calculate_path_length(D, f):
	"""计算种群中每个个体的路径长度"""
	NP, N = f.shape
	l = np.zeros(NP)
	for i in range(NP):
		l[i] = D[f[i, -1], f[i, 0]]
		for j in range(N - 1):
			l[i] += D[f[i, j], f[i, j + 1]]
	return l


def selection(fitness, f):
	"""根据适应度值进行选择操作"""
	NP, _ = f.shape
	F = []
	for i in range(NP):
		if fitness[i] >= random.random():
			F.append(f[i].copy())
	return np.array(F)


def crossover_and_mutation(F, NP, N, D):
	"""交叉和变异操作"""
	while len(F) < NP:
		nnper = np.random.permutation(len(F))
		A = F[nnper[0]].copy()
		B = F[nnper[1]].copy()

		# 交叉操作
		W = int(np.ceil(N / 10))
		p = np.random.randint(0, N - W + 1)
		for i in range(W):
			x = np.where(A == B[p + i])[0][0]
			y = np.where(B == A[p + i])[0][0]
			temp = A[p + i]
			A[p + i] = B[p + i]
			B[p + i] = temp
			temp = A[x]
			A[x] = B[y]
			B[y] = temp

		# 变异操作
		p1 = np.random.randint(0, N)
		p2 = np.random.randint(0, N)
		while p1 == p2:
			p1 = np.random.randint(0, N)
			p2 = np.random.randint(0, N)
		A[p1], A[p2] = A[p2], A[p1]
		B[p1], B[p2] = B[p2], B[p1]

		F = np.append(F, [A, B], axis=0)

	if len(F) > NP:
		F = F[:NP]

	return F


class GAThread(QThread):
	"""线程函数"""

	onEpochChanged = pyqtSignal(list)
	onPathChanged = pyqtSignal(list, float)
	onCalcFinished = pyqtSignal(float)
	onFinished = pyqtSignal()

	def __init__(self, graph=None):
		"""构造函数"""
		super().__init__()
		self.is_running = True
		self.graph = graph
		self.G = 200

	def isrun(self, value: bool):
		self.is_running = value

	def genetic_algorithm(self, C, NP=200, G=200):
		"""遗传算法解决 TSP 问题"""
		N = len(C)
		D = np.zeros((N, N))

		# 计算距离矩阵
		for i in range(N):
			for j in range(N):
				D[i, j] = np.sqrt((C[i, 0] - C[j, 0]) ** 2 + (C[i, 1] - C[j, 1]) ** 2)

		# 初始化种群
		f = np.array([np.random.permutation(N) for _ in range(NP)])
		R = None
		Rlength = []

		for gen in range(G):
			# 计算路径长度
			l = calculate_path_length(D, f)

			maxlen = np.max(l)
			minlen = np.min(l)

			# 更新最短路径
			rr = np.where(l == minlen)[0]
			R = f[rr[0]].copy()

			# 计算归一化适应值
			fitness = 1 - ((l - minlen) / (maxlen - minlen + 0.001))

			# 选择操作
			F = selection(fitness, f)

			# 交叉和变异操作
			F = crossover_and_mutation(F, NP, N, D)

			f = F.copy()
			f[0] = R
			Rlength.append(minlen)

			v_on = self.online_judge(fitness, gen + 1)
			v_off = self.offline_judge(Rlength, gen + 1)
			self.onEpochChanged.emit([minlen, v_on, v_off])
			path = []
			for r_ in R:
				path.append([self.graph.nodes[r_]["x"], self.graph.nodes[r_]["y"]])
			self.onPathChanged.emit(path, minlen.round(2))

		return R, Rlength[-1].round(2)

	def run(self):
		best_path, best_distance = self.genetic_algorithm(self.graph.get_nodes(), G=self.G)
		# best_path, best_distance = self.tsp_genetic_algorithm(self.graph.get_nodes(), G=self.G)
		self.onCalcFinished.emit(best_distance)
		# self.onEpochChanged.emit([best_distance, best_distance, best_distance])
		self.onFinished.emit()

	def stop(self):
		self.is_running = False

	def set_G(self, G):
		self.G = G

	def online_judge(self, f, T):
		v = 0
		for i in range(0, T - 1):
			v += f[i]
		return v / T

	def offline_judge(self, f_, T):
		v = 0
		for i in range(0, T - 1):
			v += f_[i]
		return v / T
