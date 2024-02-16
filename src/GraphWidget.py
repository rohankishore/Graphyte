import re

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import matplotlib.pyplot as plt
import numpy as np
# math functions
# from numpy import sin, cos, tan, sqrt, arcsin, arccos, arctan

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

        self.functions = {}  # Store the plotted functions and their expressions
        self.intersection_points = []  # Store intersection points

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
        self.functions.clear()  # Clear the stored functions
        try:
            x = np.linspace(-1, 1, 100)  # Adjust the number of points for smoother plots
            for function_text in functions:
                if '=' in function_text:
                    variable, expression = function_text.split('=')
                    variable = variable.strip()
                    plt.grid()
                    expression = expression.strip()
                    self.functions[variable] = expression  # Store the function expression
                    locals()[variable] = eval(expression)
                    self.axis.plot(x, eval(expression), label=function_text)
                else:
                    plt.grid(True)
                    try:
                        function_text = function_text.replace(function_text, ('np.'+function_text))
                        y = eval(function_text)
                        self.axis.plot(x, y, label=function_text)
                    except Exception as e:
                        msgBox = QMessageBox()
                        msgBox.setIcon(QMessageBox.Icon.Warning)
                        msgBox.setText(str(e))
                        msgBox.setWindowTitle("Uh-Oh!")
                        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                        msgBox.setDefaultButton(QMessageBox.StandardButton.Ok)
                        msgBox.exec()

            plt.grid(True)
            self.axis.legend()
            self.canvas.draw()
        except Exception as e:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setText(str(e))
            msgBox.setWindowTitle("Uh-Oh!")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            msgBox.setDefaultButton(QMessageBox.StandardButton.Ok)
            msgBox.exec()

    def find_intersections(self, selected_functions):
        if len(selected_functions) < 2:
            print("Please select at least two functions to find intersections.")
            return

        x_values = np.linspace(-10, 10, 1000)
        intersection_points = []

        for i in range(len(selected_functions)):
            for j in range(i + 1, len(selected_functions)):
                func1_text = selected_functions[i]
                func2_text = selected_functions[j]

                # Check if '=' exists in func1_text before splitting
                if '=' in func1_text:
                    func1_name, func1_expr = func1_text.split('=')
                    func1_expr = func1_expr.strip()
                else:
                    # If '=' is missing, use the entire text as the expression
                    func1_name = ''
                    func1_expr = func1_text.strip()

                # Check if '=' exists in func2_text before splitting
                if '=' in func2_text:
                    func2_name, func2_expr = func2_text.split('=')
                    func2_expr = func2_expr.strip()
                else:
                    # If '=' is missing, use the entire text as the expression
                    func2_name = ''
                    func2_expr = func2_text.strip()

                try:
                    func1_values = eval(func1_expr, {'np': np, 'x': x_values})
                    func2_values = eval(func2_expr, {'np': np, 'x': x_values})

                    intersection_indices = np.where(np.isclose(func1_values, func2_values, atol=0.01))[0]
                    for index in intersection_indices:
                        intersection_points.append((x_values[index], func1_values[index]))
                except Exception as e:
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Icon.Warning)
                    msgBox.setText(str(e))
                    msgBox.setWindowTitle("Uh-Oh!")
                    msgBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                    msgBox.setDefaultButton(QMessageBox.StandardButton.Ok)
                    msgBox.exec()

        if intersection_points:
            print("Intersection points:", intersection_points)
            self.plot_intersections(intersection_points)

    def plot_intersections(self, intersection_points):
        x_vals = [point[0] for point in intersection_points]
        y_vals = [point[1] for point in intersection_points]

        # Plot intersection points
        self.axis.scatter(x_vals, y_vals, color='red', label='Intersections')
        self.canvas.draw()
