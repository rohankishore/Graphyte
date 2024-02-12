import re

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import matplotlib.pyplot as plt
import numpy as np

# math functions
from numpy import sin, cos, tan, sqrt, arcsin, arccos, arctan

from mpl_interactions import panhandler, zoom_factory

top = 0.977
bottom = 0.029
left = 0.028
right = 1.0
hspace = 0.2
wspace = 0.2


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure, self.axis = plt.subplots()
        self.figure.patch.set_facecolor('#202124')
        plt.tight_layout()
        plt.subplots_adjust(left=left, right=right, top=top, bottom=bottom, hspace=hspace, wspace=wspace)
        self.canvas = FigureCanvas(self.figure)

        # Set margins and spacing of the layout to 0
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.canvas)

        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        # Add interactive features for panning and zooming
        plt.ioff()  # Turn interactive mode off
        plt.grid()
        self.axis.set_facecolor('#202124')
        self.canvas.mpl_connect("draw_event", panhandler)

        zoom_factory(self.axis, base_scale=1.1)


    def plot_function(self, functions):
        self.axis.clear()
        try:
            x = np.linspace(-1, 1, 100)  # Adjust the number of points for smoother plots
            for function_text in functions:
                # Replace '2x' with '2*x' for multiplication
                function_text = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', function_text)
                # Replace other symbols as needed, for example '^' with '**'
                function_text = function_text.replace('^', '**')
                # Add more replacements as necessary

                if '=' in function_text:
                    variable, expression = function_text.split('=')
                    variable = variable.strip()
                    expression = expression.strip()
                    locals()[variable] = eval(expression)
                else:
                    y = eval(function_text)
                    self.axis.plot(x, y, label=function_text)  # Add a label for each function

            plt.grid()
            self.axis.legend()  # Add legend to the plot
            self.canvas.draw()
            # self.parent.function_list_widget.addItem(function_text)
        except Exception as e:
            print("Error:", e)
