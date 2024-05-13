from enum import Enum

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from qfluentwidgets import SubtitleLabel, TitleLabel,CaptionLabel, TransparentPushButton, \
	PrimaryPushButton, SpinBox

from view.myIcon import MyIcon
from view.chartView import ChartView


class Status(Enum):
	NOT_READY = "Not Ready"
	READY = "Ready"
	EXECUTING = "Executing"
	DONE = "Done"


class ChartWidget(QWidget):
	onCalcStart = pyqtSignal()
	onCalcStop = pyqtSignal()
	onGSet = pyqtSignal(int)
	onWidgetSwitch = pyqtSignal()
	def __init__(self, text="", parent=None, graph=None):
		super().__init__(parent=parent)
		self.graph = graph
		self.text = text
		self.status = Status.NOT_READY
		self.current_epoch = 0
		self.total_epoch = 0
		self.has_data = False
		self.distance = -1
		self.init_ui()
		self.check_status()

	def init_ui(self):
		self.mainLayout = QVBoxLayout(self)

		self.titleLayout = QHBoxLayout()
		self.title = TitleLabel(self.text, self)
		self.title.setStyleSheet("padding: 0px 0px 0px 10px;")
		self.statusLabel = SubtitleLabel(f"Status: {self.status.value}", self)
		self.statusLabel.setStyleSheet("color: red;")

		self.titleLayout.addWidget(self.title)
		self.titleLayout.addWidget(self.statusLabel)

		self.settingLayout = QHBoxLayout()
		self.settingLabel = CaptionLabel("Enter the number of cycles (integer):", self)
		# lineEdit = LineEdit()
		self.spinBox = SpinBox()
		self.spinBox.setRange(100, 2000)
		self.spinBox.setValue(200)
		self.spinBox.setSingleStep(50)

		self.spinBox.valueChanged.connect(lambda: self.onGSet.emit(self.spinBox.value()))

		self.settingLayout.addWidget(self.settingLabel, 0)
		self.settingLayout.addWidget(self.spinBox, 1)

		self.toolBoxLayout = QHBoxLayout()
		self.startButton = TransparentPushButton(MyIcon.START, "Start")
		self.clearButton = TransparentPushButton(MyIcon.CLEAR, "Clear")

		self.startButton.setEnabled(False)
		self.startButton.setCursor(Qt.CursorShape.ForbiddenCursor)
		self.clearButton.setEnabled(False)
		self.clearButton.setCursor(Qt.CursorShape.ForbiddenCursor)

		self.startButton.clicked.connect(self.start)
		self.clearButton.clicked.connect(self.clear_data)

		self.toolBoxLayout.addWidget(self.startButton)
		self.toolBoxLayout.addWidget(self.clearButton)

		self.chartsLayout = QGridLayout()

		self.chart1 = ChartView("Current best", self)
		self.chart2 = ChartView("Online comparison", self)
		self.chart3 = ChartView("Offline comparison", self)


		self.dataDetailLayout = QVBoxLayout()
		self.distanceLabel = SubtitleLabel(f"Distance: Not Calculated", self)
		self.swtichButton = PrimaryPushButton(MyIcon.GO, 'Go To Detail')
		self.swtichButton.clicked.connect(lambda: self.onWidgetSwitch.emit())
		self.swtichButton.setEnabled(False)
		self.swtichButton.setCursor(Qt.CursorShape.ForbiddenCursor)

		self.dataDetailLayout.addWidget(self.distanceLabel)
		self.dataDetailLayout.addWidget(self.swtichButton)

		self.dataDetailFrame = QFrame()
		self.dataDetailFrame.setLayout(self.dataDetailLayout)
		self.dataDetailFrame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
		self.dataDetailFrame.setMidLineWidth(0)
		self.dataDetailFrame.setStyleSheet("padding: 60px 80px 60px 60px; margin: 0 10px 0 50px")


		self.chartsLayout.addWidget(self.chart1, 0, 0)
		self.chartsLayout.addWidget(self.chart2, 0, 1)
		self.chartsLayout.addWidget(self.chart3, 1, 0)
		self.chartsLayout.addWidget(self.dataDetailFrame, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

		self.mainLayout.addLayout(self.titleLayout, 0)
		self.mainLayout.addLayout(self.settingLayout, 0)
		self.mainLayout.addLayout(self.toolBoxLayout, 0)
		self.mainLayout.addLayout(self.chartsLayout, 1)

		self.setLayout(self.mainLayout)

		self.setObjectName(self.text.replace(' ', '-'))

	def check_status(self):
		if self.graph is not None and len(self.graph.matrix) > 2 and len(self.graph.matrix[0]) > 2 and len(
				self.graph.nodes) > 2 and len(self.graph.edges) > 2:
			self.status = Status.READY
			self.statusLabel.setText(f"Status: {self.status.value}")
			self.statusLabel.setStyleSheet("color: green;")
			self.startButton.setEnabled(True)
			self.startButton.setCursor(Qt.CursorShape.PointingHandCursor)
		else:
			self.status = Status.NOT_READY
			self.statusLabel.setText(f"Status: {self.status.value}")
			self.statusLabel.setStyleSheet("color: red;")
			self.startButton.setEnabled(False)
			self.startButton.setCursor(Qt.CursorShape.ForbiddenCursor)

	def update(self):
		self.check_status()
		self.repaint()

	def start(self):
		if self.status == Status.READY:
			self.status = Status.EXECUTING
			self.startButton.setText("Stop")
			self.startButton.setIcon(MyIcon.STOP)
			self.statusLabel.setText(f"Status: {self.status.value}")
			self.statusLabel.setStyleSheet("color: blue;")
			self.onCalcStart.emit()
		elif self.status == Status.EXECUTING:
			self.status = Status.DONE
			self.startButton.setText("Start")
			self.startButton.setIcon(MyIcon.START)
			self.statusLabel.setText(f"Status: {self.status.value}")
			self.statusLabel.setStyleSheet("color: color;")
			self.onCalcStop.emit()
		self.startButton.setEnabled(False)
		self.repaint()

	def sync_data(self, datas):
		if not self.has_data:
			self.has_data = True
			self.clearButton.setEnabled(True)
			self.clearButton.setCursor(Qt.CursorShape.PointingHandCursor)
		self.chart1.add_data(datas[0])
		self.chart2.add_data(datas[1])
		self.chart3.add_data(datas[2])
		self.repaint()

	def clear_data(self):
		self.chart1.clear_data()
		self.chart2.clear_data()
		self.chart3.clear_data()
		self.has_data = False
		self.clearButton.setEnabled(False)
		self.clearButton.setCursor(Qt.CursorShape.ForbiddenCursor)
		self.startButton.setEnabled(True)
		self.startButton.setCursor(Qt.CursorShape.PointingHandCursor)
		self.status = Status.READY
		self.swtichButton.setEnabled(False)
		self.swtichButton.setCursor(Qt.CursorShape.ForbiddenCursor)
		self.repaint()

	def calc_finish(self):
		self.status = Status.DONE
		self.startButton.setText("Start")
		self.startButton.setIcon(MyIcon.START)
		self.statusLabel.setText(f"Status: {self.status.value}")
		self.statusLabel.setStyleSheet("color: green;")
		self.startButton.setEnabled(False)
		self.repaint()

	def handle_data_change(self, best_distance):
		self.distance = best_distance
		self.distanceLabel.setText(f"Distance: {self.distance}")
		self.swtichButton.setEnabled(True)
		self.swtichButton.setCursor(Qt.CursorShape.PointingHandCursor)
		self.repaint()

