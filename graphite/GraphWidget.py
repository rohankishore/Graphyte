from PyQt6.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, tan
from mpl_interactions import panhandler, zoom_factory


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure, self.axis = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        self.parent = parent
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        # Add interactive features for panning and zooming
        plt.ioff()  # Turn interactive mode off
        self.canvas.mpl_connect("draw_event", panhandler)
        zoom_factory(self.axis, base_scale=1.1)

    def plot_function(self, functions):
        self.axis.clear()
        try:
            x = np.linspace(-20, 20, 400)
            for function_text in functions:
                y = eval(function_text)
                self.axis.plot(x, y, label=function_text)  # Add a label for each function
            plt.grid()
            self.axis.legend()  # Add legend to the plot
            self.canvas.draw()
            self.parent.function_list_widget.addItem(function_text)
        except Exception as e:
            print("Error:", e)
