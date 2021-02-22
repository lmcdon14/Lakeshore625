# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'td_gui.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib
matplotlib.use('Qt5Agg')
import sys
import re
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MyButton(QtWidgets.QPushButton):
    def __init__(self, widget, font2, dims, text):
        super().__init__(widget)
        font3 = font2
        font3.setPointSize(10)
        self.setGeometry(dims)
        self.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:5px;}")
        self.setFont(font3)
        self.setText(text)
        self.setObjectName("fitdata")
        self.co_get = 0
        self.co_set = 0

    def _set_color(self, col):
        palette = self.palette()
        palette.setColor(self.foregroundRole(), col)
        self.setPalette(palette)

    def parseStyleSheet(self):
        ss = self.styleSheet()
        sts = [s.strip() for s in ss.split(';') if len(s.strip())]
        return sts

    def getBackColor(self):
        self.co_get += 1
        # print(fuin(), self.co_get)
        return self.palette().color(self.pal_ele)

    def setBackColor(self, color):
        self.co_set += 1
        sss = self.parseStyleSheet()
        if color.alpha() == 0:
            alph = 0.5
        else:
            alph = color.alpha()
        bg_new = 'background-color: rgba(%2.1f,%2.1f,%2.1f,%2.1f)' % (color.red(), color.green(), color.blue(), alph)

        for k, sty in enumerate(sss):
            if re.search('background-color:', sty):
                sss[k] = bg_new
                break
        else:
            sss.append(bg_new)

        self.setStyleSheet('QPushButton {' + '; '.join(sss))
        #print('QPushButton {' + '; '.join(sss))

    pal_ele = QtGui.QPalette.Window
    zcolor = QtCore.pyqtProperty(QtGui.QColor, getBackColor, setBackColor)

    color = QtCore.pyqtProperty(QtGui.QColor, fset=_set_color)

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(6, 1, (1, 5), xlabel='Current(A)', ylabel='Neutron Counts')
        #fig.text(0.5, 0.02, 'Current (A)', ha='center')
        #fig.text(0.02, 0.5, 'Neutron Counts', va='center', rotation='vertical')
        super(MplCanvas, self).__init__(self.fig)

class Ui_TapeDriveWindow(object):
    def setupUi(self, TapeDriveWindow):
        # Setup window
        TapeDriveWindow.setObjectName("TapeDriveWindow")
        TapeDriveWindow.resize(640, 950)
        TapeDriveWindow.setMinimumSize(QtCore.QSize(640, 950))
        TapeDriveWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        TapeDriveWindow.setStyleSheet("TapeDriveWindow {qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255))}")
        self.centralwidget = QtWidgets.QWidget(TapeDriveWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Setup plots for neutron counts vs. current
        self.sc0 = MplCanvas(self, width=5, height=4, dpi=100)
        # Arbitrary plot values
        self.sc0.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        toolbar = NavigationToolbar(self.sc0, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc0)
        widget = QtWidgets.QWidget(self.centralwidget)
        widget.setLayout(layout)
        widget.setGeometry(QtCore.QRect(70, 215, 500, 350))
        self.centralwidget.show()

        # Setup plots for neutron counts vs. current
        self.sc1 = MplCanvas(self, width=5, height=1, dpi=100)
        # Arbitrary plot values
        self.sc1.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        toolbar = NavigationToolbar(self.sc1, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc1)
        widget = QtWidgets.QWidget(self.centralwidget)
        widget.setLayout(layout)
        widget.setGeometry(QtCore.QRect(70, 545, 500, 350))
        self.centralwidget.show()

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resources/bw3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Resources/fw3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        xmov = 50

        # PS Label
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 25, 621, 41))
        self.label_5.setStyleSheet("QLabel {font-size: 24px; background-color: rgba(0,0,0,0.5); color: white; border-radius: 5px;}")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        # Main Field Setpoint Label
        self.label_ms = QtWidgets.QLabel(self.centralwidget)
        self.label_ms.setGeometry(QtCore.QRect(110+35+xmov, 85, 100, 40))
        self.label_ms.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_ms.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ms.setObjectName("label_ms")
        # Main Field Setpoint Label
        self.label_mr = QtWidgets.QLabel(self.centralwidget)
        self.label_mr.setGeometry(QtCore.QRect(210+35+xmov, 85, 100, 40))
        self.label_mr.setStyleSheet("QLabel {font-size: 12px; color: black; border-radius: 5px;}")
        self.label_mr.setAlignment(QtCore.Qt.AlignCenter)
        self.label_mr.setObjectName("label_mr")
        # PS1 Label
        self.label_ps1 = QtWidgets.QLabel(self.centralwidget)
        self.label_ps1.setGeometry(QtCore.QRect(50+xmov, 130, 100, 40))
        self.label_ps1.setStyleSheet("QLabel {font-size: 20px; color: black; border-radius: 5px;}")
        self.label_ps1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ps1.setObjectName("label_ps1")
        # PS2 Label
        self.label_ps2 = QtWidgets.QLabel(self.centralwidget)
        self.label_ps2.setGeometry(QtCore.QRect(50+xmov, 180, 100, 40))
        self.label_ps2.setStyleSheet("QLabel {font-size: 20px; color: black; border-radius: 5px;}")
        self.label_ps2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ps2.setObjectName("label_ps2")
        
        # Power Supply Control 1
        self.ps1spinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ps1spinBox.setGeometry(QtCore.QRect(110+35+xmov, 130, 100, 40))
        self.ps1spinBox.setFont(font)
        self.ps1spinBox.setReadOnly(True)
        self.ps1spinBox.setDecimals(3)
        self.ps1spinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.ps1spinBox.setStyleSheet("color: lightgrey;")
        self.ps1spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.ps1spinBox.setKeyboardTracking(False)
        self.ps1spinBox.setMinimum(-20.0)
        self.ps1spinBox.setMaximum(20.0)
        self.ps1spinBox.setProperty("value", 0.0)
        self.ps1spinBox.setObjectName("ps1spinBox")
        # Power Supply Readout 1
        self.ps1readspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ps1readspinBox.setGeometry(QtCore.QRect(210+35+xmov, 130, 100, 40))
        self.ps1readspinBox.setFont(font)
        self.ps1readspinBox.setReadOnly(True)
        self.ps1readspinBox.setDecimals(3)
        self.ps1readspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.ps1readspinBox.setStyleSheet("color: lightgrey;")
        self.ps1readspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.ps1readspinBox.setMinimum(-20.0)
        self.ps1readspinBox.setMaximum(20.0)
        self.ps1readspinBox.setProperty("value", 0.0)
        self.ps1readspinBox.setObjectName("ps1readspinBox")
        # Power Supply Control 2
        self.ps2spinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ps2spinBox.setGeometry(QtCore.QRect(110+35+xmov, 180, 100, 40))
        self.ps2spinBox.setFont(font)
        self.ps2spinBox.setReadOnly(True)
        self.ps2spinBox.setDecimals(3)
        self.ps2spinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.ps2spinBox.setStyleSheet("color: lightgrey;")
        self.ps2spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.ps2spinBox.setKeyboardTracking(False)
        self.ps2spinBox.setMinimum(-20.0)
        self.ps2spinBox.setMaximum(20.0)
        self.ps2spinBox.setProperty("value", 0.0)
        self.ps2spinBox.setObjectName("ps1spinBox")
        # Power Supply Readout 2
        self.ps2readspinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ps2readspinBox.setGeometry(QtCore.QRect(210+35+xmov, 180, 100, 40))
        self.ps2readspinBox.setFont(font)
        self.ps2readspinBox.setReadOnly(True)
        self.ps2readspinBox.setDecimals(3)
        self.ps2readspinBox.setAlignment(QtCore.Qt.AlignHCenter)
        self.ps2readspinBox.setStyleSheet("color: lightgrey;")
        self.ps2readspinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.ps2readspinBox.setMinimum(-20.0)
        self.ps2readspinBox.setMaximum(20.0)
        self.ps2readspinBox.setProperty("value", 0.0)
        self.ps2readspinBox.setObjectName("ps2readspinBox")

        # PS1 Output Enable
        self.ps1Out = QtWidgets.QPushButton(self.centralwidget)
        self.ps1Out.setGeometry(QtCore.QRect(320+35+xmov, 130, 140, 40))
        self.ps1Out.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;}")
        font2 = font
        font2.setPointSize(11)
        font2.setBold(False)
        self.ps1Out.setFont(font2)
        self.ps1Out.setCheckable(True)
        self.ps1Out.setText("Output Enable")
        self.ps1Out.setObjectName("ps1Out")
        # PS2 Output Enable
        self.ps2Out = QtWidgets.QPushButton(self.centralwidget)
        self.ps2Out.setGeometry(QtCore.QRect(320+35+xmov, 180, 140, 40))
        self.ps2Out.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;}")
        self.ps2Out.setFont(font2)
        self.ps2Out.setCheckable(True)
        self.ps2Out.setText("Output Enable")
        self.ps2Out.setObjectName("ps2Out")

        # PS Connection
        self.con = QtWidgets.QPushButton(self.centralwidget)
        self.con.setGeometry(QtCore.QRect(10, 175-28, 80, 55))
        self.con.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;}")
        font3 = font
        font3.setPointSize(9)
        font3.setBold(False)
        self.con.setFont(font3)
        self.con.setCheckable(True)
        self.con.setText("Connect\nDevices")
        self.con.setObjectName("con")

        # Neutron Count Data File
        self.countfile = QtWidgets.QPushButton(self.centralwidget)
        self.countfile.setGeometry(QtCore.QRect(10, 280, 50, 50))
        self.countfile.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;}")
        self.countfile.setFont(font3)
        self.countfile.setCheckable(False)
        self.countfile.setText("Load\nData")
        self.countfile.setObjectName("countfile")

        # Fit Neutron Count Data
        self.fitdata = MyButton(self.centralwidget, font2, QtCore.QRect(10, 335, 50, 50),"Fit\nData")
        self.fitdata.setEnabled(False)
        self.animfit = QtCore.QPropertyAnimation(self.fitdata, b"zcolor")
        self.animfit.setDuration(750)
        self.animfit.setLoopCount(1)
        self.animfit.setStartValue(QtGui.QColor(0,0,0,0.5))
        self.animfit.setKeyValueAt(0.1, QtGui.QColor("lightblue"))
        self.animfit.setKeyValueAt(0.9, QtGui.QColor("lightblue"))
        self.animfit.setEndValue(QtGui.QColor(0,0,0,0.5))

        # Neutron Count Data File 2
        self.countfile2 = QtWidgets.QPushButton(self.centralwidget)
        self.countfile2.setGeometry(QtCore.QRect(10, 610, 50, 50))
        self.countfile2.setStyleSheet("QPushButton {background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;}")
        self.countfile2.setFont(font3)
        self.countfile2.setCheckable(False)
        self.countfile2.setText("Load\nData")
        self.countfile2.setObjectName("countfile2")

        # Fit Neutron Count Data 2
        self.fitdata2 = MyButton(self.centralwidget, font2, QtCore.QRect(10, 665, 50, 50),"Fit\nData")
        self.fitdata2.setEnabled(False)
        self.animfit2 = QtCore.QPropertyAnimation(self.fitdata, b"zcolor")
        self.animfit2.setDuration(750)
        self.animfit2.setLoopCount(1)
        self.animfit2.setStartValue(QtGui.QColor(0,0,0,0.5))
        self.animfit2.setKeyValueAt(0.1, QtGui.QColor("lightblue"))
        self.animfit2.setKeyValueAt(0.9, QtGui.QColor("lightblue"))
        self.animfit2.setEndValue(QtGui.QColor(0,0,0,0.5))

        # Current Estimator 1
        self.current_est1 = QtWidgets.QLineEdit(self.centralwidget)
        self.current_est1.setGeometry(QtCore.QRect(380, 512, 60, 40))
        self.current_est1.setFont(font)
        self.current_est1.setAlignment(QtCore.Qt.AlignHCenter)
        self.current_est1.setStyleSheet("color: black;")
        self.current_est1.setObjectName("current_est1")
        self.current_est1.setEnabled(False)

        # Current Value Estimator 1
        self.val_est1 = QtWidgets.QLineEdit(self.centralwidget)
        self.val_est1.setGeometry(QtCore.QRect(460, 512, 60, 40))
        self.val_est1.setFont(font)
        self.val_est1.setAlignment(QtCore.Qt.AlignHCenter)
        self.val_est1.setStyleSheet("color: black;")
        self.val_est1.setObjectName("val_est1")
        self.val_est1.setEnabled(False)
        self.val_est1.setReadOnly(True)

        # Current Estimator 2
        self.current_est2 = QtWidgets.QLineEdit(self.centralwidget)
        self.current_est2.setGeometry(QtCore.QRect(380, 842, 60, 40))
        self.current_est2.setFont(font)
        self.current_est2.setAlignment(QtCore.Qt.AlignHCenter)
        self.current_est2.setStyleSheet("color: black;")
        self.current_est2.setObjectName("current_est2")
        self.current_est2.setEnabled(False)

        # Current Value Estimator 2
        self.val_est2 = QtWidgets.QLineEdit(self.centralwidget)
        self.val_est2.setGeometry(QtCore.QRect(460, 842, 60, 40))
        self.val_est2.setFont(font)
        self.val_est2.setAlignment(QtCore.Qt.AlignHCenter)
        self.val_est2.setStyleSheet("color: black;")
        self.val_est2.setObjectName("val_est1")
        self.val_est2.setEnabled(False)
        self.val_est2.setReadOnly(True)

        TapeDriveWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(TapeDriveWindow)
        self.statusbar.setObjectName("statusbar")
        TapeDriveWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(TapeDriveWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menuBar.setObjectName("menuBar")
        TapeDriveWindow.setMenuBar(self.menuBar)
        self.actionQuit = QtWidgets.QAction(TapeDriveWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionNothingHere = QtWidgets.QAction(TapeDriveWindow)
        self.actionNothingHere.setObjectName("actionNothingHere")

        self.retranslateUi(TapeDriveWindow)
        QtCore.QMetaObject.connectSlotsByName(TapeDriveWindow)

    def retranslateUi(self, TapeDriveWindow):
        # degree_sign = u"\N{DEGREE SIGN}"
        _translate = QtCore.QCoreApplication.translate
        TapeDriveWindow.setWindowTitle(_translate("TapeDriveWindow", "Lakeshore 625 Control"))
        self.label_5.setText(_translate("TapeDriveWindow", "Lakeshore 625"))
        self.label_ms.setText(_translate("TapeDriveWindow", "Current\nSetpoint (A)"))
        self.label_mr.setText(_translate("TapeDriveWindow", "Current\nReadout (A)"))
        self.label_ps1.setText(_translate("TapeDriveWindow", "Supply 1"))
        self.label_ps2.setText(_translate("TapeDriveWindow", "Supply 2"))
        self.actionQuit.setText(_translate("TapeDriveWindow", "Exit"))
        self.actionQuit.setShortcut(_translate("TapeDriveWindow", "Meta+Q"))
        self.actionNothingHere.setText(_translate("TapeDriveWindow", "NothingHere"))

import resources_rc