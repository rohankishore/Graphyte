import sys
import qdarktheme
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QVBoxLayout, QWidget, QLineEdit, QListWidget, \
    QAbstractItemView, QHBoxLayout, QToolBar
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, tan
from mpl_interactions import panhandler, zoom_factory


class Graphite(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Graphite.")
        self.setGeometry(100, 100, 800, 600)

        self.toolbox = QToolBar(self)
        self.toolbox.setFixedHeight(40)
        #self.addToolBar(self.toolbox)

        move = QAction("Move", self)
        move.triggered.connect(self._move)
        move.setIcon(QIcon("resources/icons/move.png"))
        save = QAction("Save", self)
        save.triggered.connect(self._save)
        save.setIcon(QIcon("resources/icons/save.png"))

        # Connect actions to their respective functions
       # action1.triggered.connect(self.on_button1_click)
        #action2.triggered.connect(self.on_button2_click)

        # Add actions to the toolbar
        self.toolbox.addAction(move)
        self.toolbox.addAction(save)

        # Create the central widget that holds the graphing area and input bar
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout for the central widget
        central_layout = QVBoxLayout()
        self.central_widget.setLayout(central_layout)

        # Create the dock widget for the left panel
        self.dock_widget = QDockWidget("Functions", self)

        # Create a widget for the dock widget
        dock_widget_contents = QWidget()
        dock_layout = QVBoxLayout()
        dock_widget_contents.setLayout(dock_layout)

        # Create a QListWidget to display function names
        self.function_list_widget = QListWidget()
        self.function_list_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.function_list_widget.itemSelectionChanged.connect(
            self.listboxActions)  # Connect to remove function
        dock_layout.addWidget(self.function_list_widget)

        # Set the contents of the dock widget
        self.dock_widget.setWidget(dock_widget_contents)

        # Add the dock widget to the main window
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_widget)

        # Create the graphing area on the right
        self.graph_widget = MatplotlibWidget(self)
        central_layout.addWidget(self.toolbox)
        central_layout.addWidget(self.graph_widget)

        # Create an input bar below the graphing area
        self.input_bar = QLineEdit()
        self.input_bar.returnPressed.connect(self.update_graph)
        central_layout.addWidget(self.input_bar)

        # List to hold user-entered functions
        self.functions = []

    def listboxActions(self):
        delete_action = QAction("Delete", self)
        delete_action.setShortcut(Qt.Key.Key_Delete)
        delete_action.triggered.connect(self.remove_selected_function)
        self.addAction(delete_action)  # Add action to main window

    def update_graph(self):
        function_text = self.input_bar.text()
        self.functions.append(function_text)
        self.graph_widget.plot_function(self.functions)

    def _move(self):
        self.graph_widget.toolbar.pan(True)

    def _save(self):
        self.graph_widget.toolbar.save_figure()

    def remove_selected_function(self):
        selected_items = self.function_list_widget.selectedItems()
        if selected_items:
            selected_item_text = selected_items[0].text()
            row = self.function_list_widget.row(selected_items[0])
            self.function_list_widget.takeItem(row)
            self.functions.remove(selected_item_text)
            self.graph_widget.plot_function(self.functions)


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Graphite()
    qdarktheme.setup_theme("dark")
    window.show()
    sys.exit(app.exec())
