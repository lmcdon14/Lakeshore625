# Code adapted from Chris Baird's repository on github:
# cdbaird/TL-rotation-control


from PyQt5 import QtCore, QtGui, QtWidgets
from td_gui import Ui_TapeDriveWindow
import pyvisa
import math
import matplotlib.pyplot as plt
import array
import numpy as np

class mainProgram(QtWidgets.QMainWindow, Ui_TapeDriveWindow):
	def __init__(self, simulate=False):
		super().__init__()
		self.setupUi(self)
		self.sim = simulate
		self.i=0

		exitAction = QtWidgets.QAction(QtGui.QIcon('pics/exit.png'), '&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit/Terminate application')
		exitAction.triggered.connect(self.close)
		menubar = self.menuBar
		menubar.setNativeMenuBar(False)
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAction)

		if simulate==False:			
			# Attempt to onnect to Lakeshore 625
			pass
		
		self.timer = QtCore.QTimer()
		self.timer.setInterval(3000)
		self.timer.timeout.connect(self.recurring_timer)
		self.timer.start()

	def recurring_timer(self):
		if self.sim==False:
			#Update power supply readouts
			pass
			
	def closeEvent(self, event):
		# Disconnect all devices
		pass

		# and afterwards call the closeEvent of the super-class
		super(QtWidgets.QMainWindow, self).closeEvent(event)
		

if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	
	if len(sys.argv)>1:
		if sys.argv[1] == 'sim':
			tdgui = mainProgram(simulate=True)
		else:
			tdgui = mainProgram()
	else:
		tdgui = mainProgram()
	tdgui.show()
	sys.exit(app.exec_())