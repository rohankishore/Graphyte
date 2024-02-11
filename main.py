import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QVBoxLayout, QWidget, QLineEdit
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np


class GeoGebraApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Graphite.")
        self.setGeometry(100, 100, 800, 600)

        # Create the central widget that holds the graphing area and input bar
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout for the central widget
        central_layout = QVBoxLayout()
        self.central_widget.setLayout(central_layout)

        # Create the dock widget for the left panel
        self.dock_widget = QDockWidget("Tools", self)
        self.dock_widget.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)

        # Create a widget for the dock widget
        dock_widget_contents = QWidget()
        dock_layout = QVBoxLayout()
        dock_widget_contents.setLayout(dock_layout)

        # Set the contents of the dock widget
        self.dock_widget.setWidget(dock_widget_contents)

        # Add the dock widget to the main window
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_widget)

        # Create the graphing area on the right
        self.graph_widget = MatplotlibWidget(self)
        central_layout.addWidget(self.graph_widget)

        # Create an input bar below the graphing area
        self.input_bar = QLineEdit()
        self.input_bar.returnPressed.connect(self.update_graph)
        central_layout.addWidget(self.input_bar)

    def update_graph(self):
        function_text = self.input_bar.text()
        self.graph_widget.plot_function(function_text)


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure, self.axis = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Example plot
        self.plot()

    def plot(self):
        # Example plot
        x = [1, 2, 3, 4, 5]
        y = [2, 3, 4, 5, 6]

        self.axis.plot(x, y)
        self.canvas.draw()

    def plot_function(self, function_text):
        self.axis.clear()
        try:
            x = np.linspace(-10, 10, 400)
            y = eval(function_text)
            self.axis.plot(x, y)
            self.canvas.draw()
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeoGebraApp()
    window.show()
    sys.exit(app.exec())
