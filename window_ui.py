# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created: Sat Dec 30 15:58:01 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtGui.QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.scrollArea.setObjectName("scrollArea")
        self.canvas = QtGui.QWidget()
        self.canvas.setGeometry(QtCore.QRect(0, 0, 782, 518))
        self.canvas.setObjectName("canvas")
        self.scrollArea.setWidget(self.canvas)
        self.horizontalLayout_4.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionZoomIn = QtGui.QAction(MainWindow)
        self.actionZoomIn.setObjectName("actionZoomIn")
        self.actionZoomOut = QtGui.QAction(MainWindow)
        self.actionZoomOut.setObjectName("actionZoomOut")
        self.actionPoints = QtGui.QAction(MainWindow)
        self.actionPoints.setObjectName("actionPoints")
        self.actionPointPoint = QtGui.QAction(MainWindow)
        self.actionPointPoint.setObjectName("actionPointPoint")
        self.actionLineLine = QtGui.QAction(MainWindow)
        self.actionLineLine.setObjectName("actionLineLine")
        self.actionLinePoint = QtGui.QAction(MainWindow)
        self.actionLinePoint.setObjectName("actionLinePoint")
        self.actionLinePointLine = QtGui.QAction(MainWindow)
        self.actionLinePointLine.setObjectName("actionLinePointLine")
        self.toolBar.addAction(self.actionZoomIn)
        self.toolBar.addAction(self.actionZoomOut)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPoints)
        self.toolBar.addAction(self.actionPointPoint)
        self.toolBar.addAction(self.actionLineLine)
        self.toolBar.addAction(self.actionLinePoint)
        self.toolBar.addAction(self.actionLinePointLine)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoomIn.setText(QtGui.QApplication.translate("MainWindow", "Zoom In", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoomOut.setText(QtGui.QApplication.translate("MainWindow", "Zoom Out", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPoints.setText(QtGui.QApplication.translate("MainWindow", "Points", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPointPoint.setText(QtGui.QApplication.translate("MainWindow", "Point-Point", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLineLine.setText(QtGui.QApplication.translate("MainWindow", "Line-Line", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLinePoint.setText(QtGui.QApplication.translate("MainWindow", "Line Point", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLinePointLine.setText(QtGui.QApplication.translate("MainWindow", "Line Point-Line", None, QtGui.QApplication.UnicodeUTF8))

