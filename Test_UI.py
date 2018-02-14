"""
This is an example ui that inherits from SubWindow
"""

__author__ = 'rgriffin'

try:
    import pysideuic as pysideuic
    from shiboken import wrapInstance
    import shiboken as shiboken
except ImportError:
    import pyside2uic as pysideuic
    from shiboken2 import wrapInstance
    import shiboken2 as shiboken

# Qt is a project by Marcus Ottosson ---> https://github.com/mottosso/Qt.py
from Qt import QtWidgets, QtCore, QtGui, QtCompat
from PysideDockUI import SubWindow

import os
from functools import partial

class Test_UI(SubWindow):
    instances = list()
    CONTROL_NAME = "Test_UI"
    LABEL_NAME = "Test_UI"
    DOCK = False
    WINDOW_ICON = None

    def __init__(self, parent=None):
        super(Test_UI, self).__init__(parent)
        # self.ui is the QMainWindow

        # add a central widget
        self.central_widget = QtWidgets.QWidget()
        self.ui.setCentralWidget(self.central_widget)
        ##0000ff
        self.central_widget.setStyleSheet("background-color:#fa7727;")

        # Menu Bar
        self.menubar = self.ui.menuBar()
        self.populateMenuBar()

        # Tool Bar
        self.toolbar = self.ui.addToolBar('Messages')
        self.toolbar.setWindowTitle('Toolbar')
        self.toolbar_widget = QtWidgets.QWidget()
        self.toolbar_layout = QtWidgets.QVBoxLayout(self.toolbar_widget)
        self.toolbar.addWidget(self.toolbar_widget)

        # Status Bar
        self.status_bar = self.ui.statusBar()
        self.status_bar.showMessage('Hover over an element for tips.')
        self.status_bar.setSizeGripEnabled(0)

        self.toolbar.addWidget(self.status_bar)
        self.inSceneLabel = QtWidgets.QLabel()
        self.inSceneLabel.setText('Testing This')
        self.toolbar_layout.addWidget(self.inSceneLabel)

    def show(self):
        super(Test_UI, self).show()