#!/usr/bin/python
 
 
import PySide
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication
from PySide.QtGui import QMessageBox
import PySide.QtGui as qt
import os, sys, shutil
import hashlib
import random



class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.resize(800, 600)
        # container and layout
        self.container = QtGui.QWidget(self)
        self.setCentralWidget(self.container)
        self.layout = QtGui.QGridLayout(self.container)
        # labels

        self.create_toolbar()
        self.layout.setMenuBar(self.menu_bar)

    def open_photos(self):
        pass

    def segment(self):
        pass

    def about(self):
        QtGui.QMessageBox.about(self, "Shark Fin Classifier v0.1",
            "Stefan van der Walt\nTessa Marais\nPieter Holtzhausen")

    def create_toolbar(self):
        self.open_action = QtGui.QAction(self.style().standardIcon(
                QtGui.QStyle.SP_DirIcon), 
            "&Open photo", self, shortcut="ctrl+o",
            statusTip="Open new photos",
            triggered=self.open_photos)

        self.segment_action = QtGui.QAction(self.style().standardIcon(
                QtGui.QStyle.SP_ComputerIcon), 
            "&Segment", self, shortcut="",
            statusTip="Segment",
            triggered=self.segment)

        self.about_action = QtGui.QAction("&About", self, shortcut="",
            triggered=self.about)

        self.toolbar = self.addToolBar("Edit")
        self.toolbar.addAction(self.open_action)
        self.toolbar.addAction(self.segment_action)
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.menu_bar = QtGui.QMenuBar()
        self.file_menu = self.menu_bar.addMenu("&File")
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.segment_action)
        self.file_menu.addSeparator()
        self.exit_action = self.file_menu.addAction("E&xit")
        self.exit_action.triggered.connect(sys.exit)
        self.file_menu.addAction(self.exit_action)

        self.about_menu = self.menu_bar.addMenu("&Help")
        self.about_menu.addAction(self.about_action)

# Create the application object
app = QApplication(sys.argv) 
window = Window()
window.showMaximized()
window.setWindowTitle("Shark View")
window.show()
sys.exit(app.exec_())
