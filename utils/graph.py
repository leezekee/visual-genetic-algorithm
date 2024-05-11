import numpy as np


class Graph:
	def __init__(self):
		self.current_node = 0
		self.matrix = []
		self.nodes = []
		self.edges = []

	def add_node(self, x=-1, y=-1):
		self.nodes.append({"x": x, "y": y})
		self.graphify()
		self.current_node += 1

	def add_edge(self, start, end, weight):
		if weight < 0:
			return False
		new_edge_1 = {
			"start": start,
			"end": end,
			"weight": weight
		}
		new_edge_2 = {
			"start": end,
			"end": start,
			"weight": weight
		}
		self.edges.append(new_edge_1)
		self.edges.append(new_edge_2)
		self.matrix[start][end] = weight
		self.matrix[end][start] = weight
		return True

	def remove_edge(self, start, end):
		for edge in self.edges:
			if (edge["start"] == start and edge["end"] == end) or (edge["start"] == end and edge["end"] == start):
				reversed_edge = {
					"start": edge["end"],
					"end": edge["start"],
					"weight": edge["weight"]
				}
				self.edges.remove(edge)
				if reversed_edge in self.edges:
					self.edges.remove(reversed_edge)
				self.matrix[start][end] = np.inf
				self.matrix[end][start] = np.inf

	def remove_node(self, node):
		for edge in self.edges[:]:
			if edge["start"] == node or edge["end"] == node:
				self.edges.remove(edge)
			if edge["start"] > node:
				edge["start"] -= 1
			if edge["end"] > node:
				edge["end"] -= 1
		self.nodes.remove(self.nodes[node])
		self.current_node -= 1
		self.graphify()

	def graphify(self):
		rows = len(self.nodes)
		cols = rows
		self.matrix = np.full((rows, cols), np.inf)
		np.fill_diagonal(self.matrix, 0)
		for edge in self.edges:
			self.matrix[edge["start"]][edge["end"]] = int(edge["weight"])
			self.matrix[edge["end"]][edge["start"]] = int(edge["weight"])

	def load_distance_matrix(self, filename):
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
				matrix[j][i] = dist
		self.matrix = matrix
		self.nodes = max_city + 1

