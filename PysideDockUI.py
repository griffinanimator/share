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

    main_control.setStyleSheet("background-color:#505050;")
    main_control.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    main_layout = QtWidgets.QVBoxLayout(main_control)

    main_control.setParent(getMainWindow(), QtCore.Qt.Window)

    win = dialog_class(main_control)

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
    WINDOW_ICON = None
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

        else:
            return

    @staticmethod
    def delete_instances():
        for ins in SubWindow.instances:
            #logger.info('Delete {}'.format(ins))
            try:
                ins.setParent(None)
                ins.deleteLater()
            except:
                # ignore the fact that the actual parent has already been deleted by Maya...
                pass

            SubWindow.instances.remove(ins)
            del ins

    def run(self):
        return self

    def show(self):
        """
        Show the window.
        """
        if self.ui is not None:
            self.ui.show()

    def hide(self):
        """
        Hide the window.
        """
        if self.ui is not None:
            self.ui.hide()