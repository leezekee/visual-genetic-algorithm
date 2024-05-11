import random

import numpy as np
from PyQt6.QtWidgets import (QWidget, QSlider, QApplication,
                             QHBoxLayout, QVBoxLayout, QLabel)
from PyQt6.QtCore import QObject, Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QFont, QColor, QPen, QIcon
from qfluentwidgets import SubtitleLabel, setFont, TitleLabel, StrongBodyLabel


class DataWidget(QWidget):
	onEpochChanged = pyqtSignal(list)
	def __init__(self, text="", parent=None, graph=None):
		super().__init__(parent=parent)
		self.graph = graph
		self.text = text
		self.distance = -1
		self.path = []
		self.init_ui()

	def init_ui(self):
		self.mainLayout = QVBoxLayout(self)

		self.titleLayout = QHBoxLayout()
		self.title = TitleLabel(self.text, self)
		self.title.setStyleSheet("padding: 0px 0px 0px 10px;")

		self.titleLayout.addWidget(self.title)

		self.dataLayout = QVBoxLayout()
		self.dataLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

		self.distanceLabel = StrongBodyLabel(f"Distance: {self.distance}", self)
		self.pathLabel = StrongBodyLabel(f"Path: {self.path}", self)

		self.dataLayout.addWidget(self.distanceLabel)
		self.dataLayout.addWidget(self.pathLabel)

		self.mainLayout.addLayout(self.titleLayout, 0)
		self.mainLayout.addLayout(self.dataLayout, 1)

		self.setLayout(self.mainLayout)

		self.setObjectName(self.text.replace(' ', '-'))

	def handle_data_change(self, best_path, best_distance):
		self.distance = best_distance
		self.path = best_path
		self.distanceLabel.setText(f"Distance: {self.distance}")
		self.pathLabel.setText(f"Path: {self.path}")

