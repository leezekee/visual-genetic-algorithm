import numpy as np
import pyqtgraph as pg

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from qfluentwidgets import StrongBodyLabel


class ChartView(QWidget):

	def __init__(self, title, parent=None):
		super().__init__(parent=parent)
		self.pw = pg
		self.pw = pg.PlotWidget()
		self.pw.setContentsMargins(10, 10, 10, 10)
		self.pw.setLabel('left', 'y')
		self.pw.setLabel('bottom', 'x')
		# 设置图像内部背景色
		self.pw.setBackground('#f9f9f9')

		# 修改坐标轴颜色
		self.pw.getAxis('bottom').setPen(pg.mkPen(color='#009eab'))
		self.pw.getAxis('left').setPen(pg.mkPen(color='#009eab'))
		self.pw.getAxis('bottom').setTextPen(pg.mkPen(color='#009eab'))
		self.pw.getAxis('left').setTextPen(pg.mkPen(color='#009eab'))
		self.curve = self.pw.plot(pen=pg.mkPen(color='#ffb573'))

		self.title = title
		self.current = 0
		self.data_list = []
		self.mainLayout = QVBoxLayout()
		self.mainLayout.addWidget(StrongBodyLabel(self.title), alignment=Qt.AlignmentFlag.AlignCenter)
		self.mainLayout.addWidget(self.pw)
		self.setLayout(self.mainLayout)

	def paintEvent(self, a0):
		pass

	def set_data(self, data):
		series_x = np.arange(1, len(data) + 1)
		series_y = np.array(data[:])
		self.curve.clear()
		self.curve.setData(series_x, series_y)
		self.repaint()

	def set_current(self, current):
		if current < 1:
			return
		self.current = current
		self.set_data(self.data_list[current - 1])
		self.repaint()

	def add_data(self, data):
		# 取上一次的数据
		new_data = self.data_list[-1][:] if len(self.data_list) > 0 else []
		new_data.append(data)
		self.data_list.append(new_data)
		self.repaint()

	def clear_data(self):
		self.data_list = []
		self.curve.clear()
		self.curve.setData([], [])
		self.current = 0
		self.data_list = []
		self.repaint()

