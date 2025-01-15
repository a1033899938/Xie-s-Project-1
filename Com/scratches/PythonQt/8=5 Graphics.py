import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)

        self.plot()

    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        ax.set_title('示例图表')
        self.canvas.draw()


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matplotlib 与 PySide6 集成示例")
        self.setGeometry(100, 100, 800, 600)

        self.matplotlib_widget = MatplotlibWidget(self)
        self.setCentralWidget(self.matplotlib_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = App()
    main.show()
    sys.exit(app.exec())
