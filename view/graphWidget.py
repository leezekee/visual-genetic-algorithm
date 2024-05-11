from PyQt6.QtWidgets import (QWidget, QSlider, QApplication,
                             QHBoxLayout, QVBoxLayout, QLabel, QPushButton)
from PyQt6.QtCore import QObject, Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QFont, QColor, QPen, QIcon
from qfluentwidgets import SubtitleLabel, setFont, TitleLabel, TransparentToggleToolButton, TransparentPushButton

from view.graphView import GraphView
from view.myIcon import MyIcon
from utils.mode import Mode


class GraphWidget(QWidget):
	onStatusChanged = pyqtSignal()

	def __init__(self, text="", parent=None, g=None):
		super().__init__(parent=parent)
		self.g = g
		self.parent = parent
		self.text = text
		self.mode = Mode.NORMAL
		self.init_ui()

	def init_ui(self):
		self.mainLayout = QVBoxLayout(self)

		self.titleLayout = QHBoxLayout()
		self.title = TitleLabel(self.text, self)
		self.title.setStyleSheet("padding: 0px 0px 0px 10px;")

		self.status = SubtitleLabel(f"Current Mode: " + self.mode.value, self)

		self.titleLayout.addWidget(self.title)
		self.titleLayout.addWidget(self.status)

		self.toolBoxLayout = QHBoxLayout()
		self.normalButton = TransparentPushButton(MyIcon.NORMAL, "Normal")
		self.addNodeButton = TransparentPushButton(MyIcon.ADD_NODE, "Add Node")
		self.addEdgeButton = TransparentPushButton(MyIcon.ADD_EDGE, "Add Edge")
		self.removeNodeButton = TransparentPushButton(MyIcon.REMOVE_NODE, "Remove Node")
		self.removeEdgeButton = TransparentPushButton(MyIcon.REMOVE_EDGE, "Remove Edge")

		self.normalButton.clicked.connect(lambda: self.update_mode(Mode.NORMAL))
		self.addNodeButton.clicked.connect(lambda: self.update_mode(Mode.ADD_NODE))
		self.addEdgeButton.clicked.connect(lambda: self.update_mode(Mode.ADD_EDGE))
		self.removeNodeButton.clicked.connect(lambda: self.update_mode(Mode.REMOVE_NODE))
		self.removeEdgeButton.clicked.connect(lambda: self.update_mode(Mode.REMOVE_EDGE))

		self.toolBoxLayout.addWidget(self.normalButton)
		self.toolBoxLayout.addWidget(self.addNodeButton)
		self.toolBoxLayout.addWidget(self.addEdgeButton)
		self.toolBoxLayout.addWidget(self.removeNodeButton)
		self.toolBoxLayout.addWidget(self.removeEdgeButton)

		self.graphViewLayout = QVBoxLayout()
		self.graphView = GraphView(self.g, self)
		self.graphViewLayout.addWidget(self.graphView)

		self.graphView.onStatusChanged.connect(self.handle_update)

		self.mainLayout.addLayout(self.titleLayout, 0)
		self.mainLayout.addLayout(self.toolBoxLayout, 0)
		self.mainLayout.addLayout(self.graphViewLayout, 1)

		self.setLayout(self.mainLayout)

		self.setObjectName(self.text.replace(' ', '-'))

	def update_mode(self, mode):
		self.mode = mode
		self.status.setText(f"Current Mode: " + self.mode.value)
		self.graphView.update_mode(mode)

	def handle_update(self):
		self.onStatusChanged.emit()

