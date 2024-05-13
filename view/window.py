from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QIcon

from utils.ga_calc import GAThread
from view.resultWidget import ResultWidget
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
		self.ga_chart = ChartWidget('GA Analysis Chart', self, self.g)
		self.ga_result = ResultWidget('GA Result', self, self.g)
		self.ga_calc = GAThread(self.g)

		self.graph.onStatusChanged.connect(self.ga_chart.update)
		self.graph.onGraphChanged.connect(self.ga_result.handle_graph_change)
		self.graph.onGraphChanged.connect(self.ga_chart.update)

		self.ga_chart.onCalcStart.connect(self.start_calc)
		self.ga_chart.onGSet.connect(self.ga_calc.set_G)
		self.ga_chart.onWidgetSwitch.connect(self.go_ga_detail)

		self.ga_calc.onEpochChanged.connect(self.ga_chart.sync_data)
		self.ga_calc.onPathChanged.connect(self.ga_result.sync_data)
		self.ga_calc.onFinished.connect(self.ga_chart.calc_finish)
		self.ga_calc.onCalcFinished.connect(self.ga_result.handle_data_change)
		self.ga_calc.onCalcFinished.connect(self.ga_chart.handle_data_change)

		self.onCalcStop.connect(self.stop_calc)

		self.initNavigation()
		self.initWindow()

	def initNavigation(self):
		self.addSubInterface(self.graph, MyIcon.GRAPH, 'Graph Generate')
		self.navigationInterface.addSeparator()
		self.navigationInterface.addItem(
			routeKey='GA',
			icon=MyIcon.GA,
			text='Genetic Algorithm ↓',
			onClick=self.do_nothing,
			selectable=False,
			tooltip='Genetic Algorithm ↓'
		)
		self.addSubInterface(self.ga_chart, MyIcon.CHART, 'Analysis Chart')
		self.addSubInterface(self.ga_result, MyIcon.DATA, 'Data in Process')

		self.navigationInterface.setExpandWidth(200)

	def initWindow(self):
		self.setMinimumSize(1260, 960)
		self.setWindowIcon(QIcon('assets/icon.png'))
		self.setWindowTitle('Genetic Algorithm')
		# 出现在屏幕中央
		x = int((self.screen().size().width() - self.width()) / 2)
		y = int((self.screen().size().height() - self.height()) / 2)
		self.move(x, y)

	def start_calc(self):
		self.ga_calc.start()
		# self.calc.wait()

	def stop_calc(self):
		self.ga_calc.stop()

	def do_nothing(self):
		pass

	def go_ga_detail(self):
		self.switchTo(self.ga_result)
