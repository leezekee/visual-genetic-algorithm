import numpy as np


def calculate_distance(s_node, e_node):
	distance = np.sqrt((s_node["x"] - e_node["x"]) ** 2 + (s_node["y"] - e_node["y"]) ** 2)
	return distance.round(2)


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

	def add_node_without_edges(self, x=-1, y=-1):
		self.nodes.append({"x": x, "y": y})
		self.graphify(False)
		self.current_node += 1


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

	def generate_edges(self):
		# 将每两个节点之间的距离作为边的权重
		self.edges = []
		for i in range(len(self.nodes)):
			for j in range(len(self.nodes)):
				if i == j:
					continue
				self.edges.append({
					"start": i,
					"end": j,
					"weight": calculate_distance(self.nodes[i], self.nodes[j])
				})

	def graphify(self, gen=True):
		if gen:
			self.generate_edges()
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

	def clear(self):
		self.current_node = 0
		self.matrix = []
		self.nodes = []
		self.edges = []

	def get_nodes(self):
		res = []
		for node in self.nodes:
			res.append([node["x"], node["y"]])
		res = np.array(res)
		return res
