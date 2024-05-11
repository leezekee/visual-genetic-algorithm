from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon

from utils.calc import CalcThread
from view.dataWidget import DataWidget
from view.graphWidget import GraphWidget

from qfluentwidgets import FluentWindow

from view.myIcon import MyIcon
from view.chartWidget import ChartWidget
from utils.graph import Graph


class Window(FluentWindow):
	onCalcStop = pyqtSignal()
	def __init__(self):
		super().__init__()
		self.g = Graph()

		# 创建子界面，实际使用时将 Widget 换成自己的子界面
		self.graph = GraphWidget('Graph Generate', self, self.g)
		self.chart = ChartWidget('Real-time Chart', self, self.g)
		self.data = DataWidget('Data in Process', self, self.g)
		self.calc = CalcThread(self.g)

		self.graph.onStatusChanged.connect(self.chart.update)
		self.chart.onCalcStart.connect(self.start_calc)
		self.calc.onEpochChanged.connect(self.chart.sync_data)
		self.calc.onFinished.connect(self.chart.calc_finish)
		self.onCalcStop.connect(self.stop_calc)
		self.calc.onCalcFinished.connect(self.data.handle_data_change)

		self.initNavigation()
		self.initWindow()

	def initNavigation(self):
		self.addSubInterface(self.graph, MyIcon.GRAPH, 'Graph Generate')
		self.addSubInterface(self.chart, MyIcon.CHART, 'Real-time Plot')
		self.addSubInterface(self.data, MyIcon.DATA, 'Data in Process')

	def initWindow(self):
		self.setFixedSize(800, 600)
		self.setWindowIcon(QIcon('assets/icon.png'))
		self.setWindowTitle('Genetic Algorithm')

	def start_calc(self):
		self.calc.start()
		self.calc.wait()

	def stop_calc(self):
		self.calc.stop()
