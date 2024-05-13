import sys

from PyQt6.QtWidgets import QApplication

from view.window import Window




app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())

