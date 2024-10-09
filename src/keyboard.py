import sys
import qdarktheme
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QVBoxLayout, QWidget, QLineEdit, QListWidget, \
    QAbstractItemView, QToolBar, QStatusBar, QSizePolicy, QMenu, QHBoxLayout, QPushButton, QDialog
from PyQt6.QtCore import Qt
from GraphWidget import MatplotlibWidget

class Keyboard(QDialog):
    def __init__(self, input_bar):
        super().__init__()

        self.setMinimumSize(600, 400)
