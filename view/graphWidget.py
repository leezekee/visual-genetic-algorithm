from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from qfluentwidgets import SubtitleLabel, TitleLabel, TransparentPushButton

from view.graphView import GraphView
from view.myIcon import MyIcon
from utils.mode import Mode


class GraphWidget(QWidget):
	onStatusChanged = pyqtSignal()
	onGraphChanged = pyqtSignal()

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
		self.removeNodeButton = TransparentPushButton(MyIcon.REMOVE_NODE, "Remove Node")
		self.clearButton = TransparentPushButton(MyIcon.CLEAR, "Clear")

		self.normalButton.clicked.connect(lambda: self.update_mode(Mode.NORMAL))
		self.addNodeButton.clicked.connect(lambda: self.update_mode(Mode.ADD_NODE))
		self.removeNodeButton.clicked.connect(lambda: self.update_mode(Mode.REMOVE_NODE))

		self.toolBoxLayout.addWidget(self.normalButton)
		self.toolBoxLayout.addWidget(self.addNodeButton)
		self.toolBoxLayout.addWidget(self.removeNodeButton)
		self.toolBoxLayout.addWidget(self.clearButton)

		self.graphViewLayout = QVBoxLayout()
		self.graphView = GraphView(self.g, self)
		self.graphViewLayout.addWidget(self.graphView)

		self.graphView.onStatusChanged.connect(self.handle_update)
		self.graphView.onGraphChanged.connect(self.handle_graph_change)

		self.clearButton.clicked.connect(self.graphView.clear)

		self.graphToolLayout = QHBoxLayout()
		self.saveButton = TransparentPushButton(MyIcon.SAVE, "Save")
		self.loadButton = TransparentPushButton(MyIcon.LOAD, "Load")
		self.saveButton.clicked.connect(self.graphView.save)
		self.loadButton.clicked.connect(self.graphView.load)

		self.graphToolLayout.addWidget(self.loadButton)
		self.graphToolLayout.addWidget(self.saveButton)

		self.mainLayout.addLayout(self.titleLayout, 0)
		self.mainLayout.addLayout(self.toolBoxLayout, 0)
		self.mainLayout.addLayout(self.graphViewLayout, 1)
		self.mainLayout.addLayout(self.graphToolLayout, 0)

		self.setLayout(self.mainLayout)

		self.setObjectName(self.text.replace(' ', '-'))

	def update_mode(self, mode):
		self.mode = mode
		self.status.setText(f"Current Mode: " + self.mode.value)
		self.graphView.update_mode(mode)

	def handle_update(self):
		self.onStatusChanged.emit()

	def handle_graph_change(self):
		self.onGraphChanged.emit()
