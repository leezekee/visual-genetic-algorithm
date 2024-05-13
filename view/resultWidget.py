import numpy as np
from PyQt6.QtWidgets import (QWidget,
                             QHBoxLayout, QVBoxLayout,)
from PyQt6.QtCore import Qt, pyqtSignal
from qfluentwidgets import TitleLabel, StrongBodyLabel, Slider

from utils.graph import Graph
from view.graphView import GraphView


def calculate_distance(s_x, s_y, e_x, e_y):
	distance = np.sqrt((s_x - e_x) ** 2 + (s_y - e_y) ** 2)
	return distance.round(2)


class ResultWidget(QWidget):
	onEpochChanged = pyqtSignal(list)

	def __init__(self, text="", parent=None, graph=None):
		super().__init__(parent=parent)
		self.graph = graph
		self.text = text
		self.distance = -1
		self.distance_list = []
		self.path_list = []
		self.path = []
		self.current = 0
		self.total = 0
		self.res_graph = Graph()
		self.init_ui()

	def init_ui(self):
		self.mainLayout = QVBoxLayout(self)

		self.titleLayout = QHBoxLayout()
		self.title = TitleLabel(self.text, self)
		self.title.setStyleSheet("padding: 0px 0px 0px 10px;")

		self.titleLayout.addWidget(self.title)

		self.resultDistanceLayout = QHBoxLayout()
		self.distanceLabel = StrongBodyLabel(f"Distance: Not Calculate", self)
		self.resultDistanceLayout.addWidget(self.distanceLabel)

		self.graphViewLayout = QVBoxLayout()
		self.graphView = GraphView(self.res_graph)
		self.graphViewLayout.addWidget(self.graphView)

		self.sliderLayout = QVBoxLayout()
		self.sliderLabel = StrongBodyLabel("Epoch: -/-", self)
		self.slider = Slider(Qt.Orientation.Horizontal, self)
		self.slider.setRange(1, 1)

		self.slider.valueChanged.connect(self.set_current)

		self.sliderLayout.addWidget(self.sliderLabel, alignment=Qt.AlignmentFlag.AlignCenter)
		self.sliderLayout.addWidget(self.slider)

		self.mainLayout.addLayout(self.titleLayout, 0)
		self.mainLayout.addLayout(self.resultDistanceLayout, 0)
		self.mainLayout.addLayout(self.graphViewLayout, 1)
		self.mainLayout.addLayout(self.sliderLayout, 0)

		self.setLayout(self.mainLayout)

		self.setObjectName(self.text.replace(' ', '-'))

	def handle_data_change(self, best_distance):
		self.distance = best_distance
		# self.path = best_path
		self.distanceLabel.setText(f"Distance: {self.distance}")

	def sync_data(self, path, distance):
		self.path_list.append(path)
		self.distance_list.append(distance)
		self.current += 1
		self.total += 1
		self.set_current(self.current)
		self.slider.setRange(1, self.total)
		self.slider.setValue(self.current)
		self.sliderLabel.setText(f"Epoch: {self.current}/{self.total}")

	def set_current(self, current):
		if current < 1:
			return
		elif current > self.total:
			return
		self.current = current
		self.path = self.path_list[current - 1]
		last_node = None
		self.res_graph.clear()
		for i in range(len(self.path)):
			node = self.path[i]
			self.res_graph.add_node_without_edges(node[0], node[1])
			if last_node is not None:
				self.res_graph.matrix[i - 1][i] = calculate_distance(last_node[0], last_node[1], node[0], node[1])
				self.res_graph.matrix[i][i - 1] = self.res_graph.matrix[i - 1][i]
				self.res_graph.edges.append({
					"start": i - 1,
					"end": i,
					"weight": self.res_graph.matrix[i - 1][i]
				})
			if i == len(self.path) - 1:
				self.res_graph.matrix[i][0] = calculate_distance(node[0], node[1], self.path[0][0], self.path[0][1])
				self.res_graph.matrix[0][i] = self.res_graph.matrix[i][0]
				self.res_graph.edges.append({
					"start": 0,
					"end": i,
					"weight": self.res_graph.matrix[i][0]
				})
			last_node = node
		self.graphView.graph = self.res_graph
		self.graphView.update()
		self.sliderLabel.setText(f"Epoch: {self.current}/{self.total}")
		self.distanceLabel.setText(f"Distance: {self.distance_list[current - 1]}")
		self.repaint()

	def handle_graph_change(self):
		pass

	def keyPressEvent(self, a0):
		if a0.key() == Qt.Key.Key_Left:
			self.set_current(self.current - 1)
		elif a0.key() == Qt.Key.Key_Right:
			self.set_current(self.current + 1)
