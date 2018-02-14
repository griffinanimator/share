'''
------------------------------------------

Author: Ryan Griffin
email: ryangrif@gmail.com
------------------------------------------


'''
"""
This is the base I use for creating windows.  You can make them dockable or not.
"""

import os
from maya import OpenMayaUI as OpenMayaUI
import pymel.core as pm
import weakref

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

def dock_window(dialog_class):
    try:
        pm.deleteUI(dialog_class.CONTROL_NAME)
    except:
        pass

    main_control = pm.workspaceControl(dialog_class.CONTROL_NAME, iw=300, ttc=["AttributeEditor", -1], li=False, mw=True, wp='preferred',
                                       label=dialog_class.LABEL_NAME)

    control_widget = OpenMayaUI.MQtUtil.findControl(dialog_class.CONTROL_NAME)

    control_wrap = wrapInstance(long(control_widget), QtWidgets.QWidget)
    control_wrap.setStyleSheet("background-color:#505050;")
    control_wrap.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    win = dialog_class(control_wrap)

    pm.evalDeferred(lambda *args: pm.workspaceControl(main_control, e=True, rs=True))

    return win.run()

def create_window(dialog_class):
    try:
        pm.deleteUI(dialog_class.CONTROL_NAME)
    except:
        pass

    main_control = QtWidgets.QMainWindow()
    main_control.setObjectName(dialog_class.CONTROL_NAME)
    #main_control.setWindowFlags(QtWidgets.QMainWindow)
    main_control.setStyleSheet("background-color:#505050;")
    main_control.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    main_layout = QtWidgets.QVBoxLayout(main_control)

    main_control.setParent(getMainWindow(), QtCore.Qt.Window)

    win = dialog_class(main_control)
    #main_control.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    win.show()
    return win.run()

def getMainWindow():
    mayaMainWindowPtr = OpenMayaUI.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QMainWindow)
    return mayaMainWindow

class SubWindow(QtWidgets.QWidget):
    instances = list()
    CONTROL_NAME="default"
    LABEL_NAME="default"
    DOCK = False
    WINDOW_ICON = os.environ['FXS_FRAMEWORK'] + '/icon/FXS.png'
    pixmap = QtGui.QPixmap(WINDOW_ICON)
    icon_img = QtGui.QIcon(pixmap)
    """
    Helper class for loading Qt .ui files and managing the loaded QWindow.
    """
    def __init__(self, parent=None):
        # let's keep track of our docks so we only have one at a time.
        SubWindow.delete_instances()
        self.__class__.instances.append(weakref.proxy(self))

        self.window_name = self.CONTROL_NAME

        if parent:
            self.ui = parent
            if parent.layout():
                self.main_layout = parent.layout()
                self.main_layout.setContentsMargins(2, 2, 2, 2)

            self.ui.setWindowTitle(self.CONTROL_NAME)
            self.ui.setWindowIcon(self.icon_img)

        else:
            return




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
from core.ui.pywindow import SubWindow, createButton

import rigging.ui.ui_ops as ui_ops

reload(ui_ops)

import os
from functools import partial


class Test_UI(SubWindow):
    instances = list()
    CONTROL_NAME = "RigUI"
    LABEL_NAME = "Rig_UI"
    DOCK = False
    WINDOW_ICON = os.environ['FXS_ICON_PATH'] + '/FXS.png'
    pixmap = QtGui.QPixmap(WINDOW_ICON)
    icon = QtGui.QIcon(pixmap)

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