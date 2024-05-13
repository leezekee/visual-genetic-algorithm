import math

from PyQt6.QtWidgets import (QWidget, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QFont, QColor, QPen

from utils.mode import Mode


class GraphView(QWidget):
	onStatusChanged = pyqtSignal()
	onGraphChanged = pyqtSignal()

	def __init__(self, graph, parent=None):
		super().__init__(parent=parent)
		if graph is None:
			raise ValueError("Graph cannot be None")
		self.graph = graph
		self.parent = parent
		self.node_radius = 15
		self.font_size = 10
		self.mode = Mode.NORMAL
		self.selected_node = -1

	def paintEvent(self, e):
		size = self.size()
		w = size.width()
		h = size.height()
		painter = QPainter()
		painter.begin(self)
		# 边框
		painter.setPen(QPen(QColor(229, 229, 229), 2, Qt.PenStyle.SolidLine))
		painter.drawRoundedRect(0, 0, w, h, 10, 10)
		# 点状背景
		painter.setPen(QPen(QColor(227, 227, 227)))
		painter.setBrush(QColor(227, 227, 227))
		cur_h = -5
		cur_w = -5
		while cur_h < h:
			cur_h += 10
			while cur_w < w:
				cur_w += 10
				painter.drawEllipse(cur_w, cur_h, 2, 2)
			cur_w = -7

		self.draw_board(painter)
		painter.end()

	def draw_board(self, painter):
		self.draw_nodes(painter)
		self.draw_edges(painter)

	def draw_nodes(self, painter):
		nodes = self.graph.nodes
		for node in nodes:
			x = node["x"]
			y = node["y"]
			node_id = nodes.index(node)
			self.draw_node(painter, x, y, node_id)

	def draw_node(self, painter, x, y, node_id):
		if self.selected_node == node_id:
			painter.setPen(QPen(QColor(255, 181, 115), 2, Qt.PenStyle.SolidLine))
			painter.setBrush(QColor(255, 181, 115))
		else:
			painter.setPen(QPen(QColor(0, 158, 171), 2, Qt.PenStyle.SolidLine))
			painter.setBrush(QColor(0, 158, 171))
		painter.setFont(QFont('Arial', self.font_size))
		painter.drawEllipse(int(x - self.node_radius), int(y - self.node_radius), int(2 * self.node_radius),
		                    int(2 * self.node_radius))
		id_l = len(str(node_id))
		offset_x = 3 * id_l
		offset_y = int(self.font_size / 2)
		if self.selected_node == node_id:
			painter.setPen(QColor(255, 255, 255))
		else:
			painter.setPen(QColor(255, 181, 115))
		painter.drawText(int(x - offset_x), int(y + offset_y), str(node_id))

	def draw_edges(self, painter):
		edges = self.graph.edges
		drawed_edges = []
		for edge in edges:
			start = edge["start"]
			end = edge["end"]
			weight = edge["weight"]
			converse_edge = {
				"start": end,
				"end": start,
				"weight": weight
			}
			if edge in drawed_edges or converse_edge in drawed_edges:
				continue
			self.draw_edge(painter, start, end, weight)
			drawed_edges.append(edge)

	def draw_edge(self, painter, start, end, weight):
		s_node = self.graph.nodes[start]
		e_node = self.graph.nodes[end]
		s_x = s_node["x"]
		s_y = s_node["y"]
		e_x = e_node["x"]
		e_y = e_node["y"]
		d = math.sqrt((s_x - e_x) ** 2 + (s_y - e_y) ** 2)

		if s_x == e_x:
			start_offset_x = 0
			end_offset_x = 0
			if s_y < e_y:
				start_offset_y = self.node_radius
				end_offset_y = -self.node_radius
			else:
				start_offset_y = -self.node_radius
				end_offset_y = self.node_radius
		elif s_y == e_y:
			start_offset_y = 0
			end_offset_y = 0
			if s_x < e_x:
				start_offset_x = self.node_radius
				end_offset_x = -self.node_radius
			else:
				start_offset_x = -self.node_radius
				end_offset_x = self.node_radius
		else:
			start_offset_x = int((self.node_radius / d) * (e_x - s_x))
			start_offset_y = int((self.node_radius / d) * (e_y - s_y))
			end_offset_x = int((self.node_radius / d) * (s_x - e_x))
			end_offset_y = int((self.node_radius / d) * (s_y - e_y))

		line_start_x = s_x + start_offset_x
		line_start_y = s_y + start_offset_y
		line_end_x = e_x + end_offset_x
		line_end_y = e_y + end_offset_y

		line_start_x = int(line_start_x)
		line_start_y = int(line_start_y)
		line_end_x = int(line_end_x)
		line_end_y = int(line_end_y)

		painter.setPen(QPen(QColor(0, 158, 171, 100), 2, Qt.PenStyle.SolidLine))
		painter.drawLine(line_start_x, line_start_y, line_end_x, line_end_y)

		text_x = int((line_start_x + line_end_x) / 2)
		text_y = int((line_start_y + line_end_y) / 2)
		painter.setFont(QFont('Arial', self.font_size))
		painter.setPen(QColor(0, 158, 171, 200))
		painter.drawText(text_x, text_y, str(weight))

	def update_mode(self, mode):
		self.mode = mode

	def add_edge(self, start, end):
		self.graph.graphify()

	def get_clicked_node(self, x, y):
		nodes = self.graph.nodes
		for node in nodes:
			n_x = node["x"]
			n_y = node["y"]
			if math.sqrt((n_x - x) ** 2 + (n_y - y) ** 2) <= self.node_radius:
				return nodes.index(node)
		return -1

	def mousePressEvent(self, a0):
		x = a0.position().x()
		y = a0.position().y()

		node_id = self.get_clicked_node(x, y)

		if self.mode == Mode.ADD_NODE:
			self.graph.add_node(x, y)
		elif self.mode == Mode.REMOVE_NODE:
			if node_id != -1:
				self.graph.remove_node(node_id)
		self.update()
		self.onStatusChanged.emit()

	def save(self):
		file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Graph files (*.graph)")
		if file_path:
			with open(file_path, "w") as f:
				f.write(f"Nodes {len(self.graph.nodes)}\n")
				for node in self.graph.nodes:
					f.write(f"{int(node['x'])} {int(node['y'])}\n")
		self.update()

	def load(self):
		file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Graph files (*.graph)")
		if file_path:
			with open(file_path, "r") as f:
				self.graph.clear()
				nodes = int(f.readline().split()[1])
				for _ in range(nodes):
					x, y = map(int, f.readline().split())
					self.graph.add_node(int(x), int(y))
			self.graph.graphify()
		self.update()

	def update(self):
		self.repaint()
		self.onGraphChanged.emit()

	def clear(self):
		self.graph.clear()
		self.update()
