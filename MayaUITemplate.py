"""
Maya/QT UI template
Maya 2023
"""

import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtUiTools, QtCore, QtGui, QtWidgets
from functools import partial # optional, for passing args during signal function calls
import sys

class MayaUITemplate(QtWidgets.QWidget):
    """
    Create a default tool window.
    """
    window = None
    
    def __init__(self, parent = None):
        """
        Initialize class.
        """
        super(MayaUITemplate, self).__init__(parent = parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.widgetPath = ('P:\\LIBRERIA\\MAYA_SCRIPTS\\PYTHON\\demoWidget.ui')
        self.widget = QtUiTools.QUiLoader().load(self.widgetPath)
        self.widget.setParent(self)
        # set initial window size
        self.resize(400, 100)


        # locate UI widgets
        self.btn_makeGeo = self.widget.findChild(QtWidgets.QPushButton, 'btn_makeGeo')
        self.btn_close = self.widget.findChild(QtWidgets.QPushButton, 'btn_close')
        self.radio_sphere = self.widget.findChild(QtWidgets.QRadioButton, 'radioButton_sphere')
        self.radio_cube = self.widget.findChild(QtWidgets.QRadioButton, 'radioButton_cube')
        self.radio_cylinder = self.widget.findChild(QtWidgets.QRadioButton, 'radioButton_cylinder')
        self.comboBox = self.widget.findChild(QtWidgets.QComboBox, 'comboBox')

        # assign functionality to buttons
        self.btn_makeGeo.clicked.connect(self.makeGeo)
        self.btn_close.clicked.connect(self.closeWindow)
        self.comboBox.currentTextChanged.connect(self.updateSelection)

    """
    Your code goes here
    """
    def updateSelection(self, event):
        selection = self.comboBox.currentText()
        cmds.select(selection, replace = True)

    def makeGeo(self, event):
        if self.radio_sphere.isChecked():
            transform = cmds.polySphere()[0]
            self.comboBox.addItem(transform)
        if self.radio_cube.isChecked():
            transform = cmds.polyCube()[0]
            self.comboBox.addItem(transform)
        if self.radio_cylinder.isChecked():
            transform = cmds.polyCylinder()[0]
            self.comboBox.addItem(transform)

    def resizeEvent(self, event):
        """
        Called on automatically generated resize event
        """
        self.widget.resize(self.width(), self.height())
        
    def closeWindow(self):
        """
        Close window.
        """
        print('closing window')
        self.destroy()
    
def openWindow():
    """
    ID Maya and attach tool window.
    """
    # Maya uses this so it should always return True
    if QtWidgets.QApplication.instance():
        # Id any current instances of tool and destroy
        for win in (QtWidgets.QApplication.allWindows()):
            if 'myToolWindowName' in win.objectName(): # update this name to match name below
                win.destroy()

    #QtWidgets.QApplication(sys.argv)
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QtWidgets.QWidget)
    MayaUITemplate.window = MayaUITemplate(parent = mayaMainWindow)
    MayaUITemplate.window.setObjectName('myToolWindowName') # code above uses this to ID any existing windows
    MayaUITemplate.window.setWindowTitle('Maya UI Template')
    MayaUITemplate.window.show()
    
openWindow()