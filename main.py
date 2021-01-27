# Code adapted from Chris Baird's repository on github:
# cdbaird/TL-rotation-control

from PyQt5 import QtCore, QtGui, QtWidgets
from td_gui import Ui_TapeDriveWindow
import pyvisa as visa
import math
import matplotlib.pyplot as plt
import array
import numpy as np

class mainProgram(QtWidgets.QMainWindow, Ui_TapeDriveWindow):
	def __init__(self, simulate=False):
		super().__init__()
		self.setupUi(self)
		self.sim = simulate

		exitAction = QtWidgets.QAction(QtGui.QIcon('pics/exit.png'), '&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit/Terminate application')
		exitAction.triggered.connect(self.close)
		menubar = self.menuBar
		menubar.setNativeMenuBar(False)
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAction)

		#if simulate==False:			
		# Attempt to connect to Lakeshore 625
		self.type = 'gpib'
		self.con.toggled.connect(self.connection)
		self.con.click()

		self.ps1spinBox.valueChanged.connect(self.on_ps1_box)
		#self.ps2spinBox.valueChanged.connect(self.on_ps2_box)
		self.ps1Out.toggled.connect(self.ps1enable)
		#self.ps2Out.toggled.connect(self.ps2enable)
		
		self.timer = QtCore.QTimer()
		self.timer.setInterval(3000)
		self.timer.timeout.connect(self.recurring_timer)
		self.timer.start()

	def connection(self):
		if self.type == 'gpib':
			if self.con.isChecked():
				self.rm = visa.ResourceManager()
				self.resources = self.rm.list_resources()
				i=0
				for re in self.resources:
					if re[0:3] == 'GPIB':
						self.instruments[i] = self.rm.open_resource(re, read_termination='\r\n', write_termination='\r\n')
						self.instruments[i].write('MODE 1')
						print(self.instruments[i].query('*IDN?"'))
						i = i+1
			else:
				for ind, inst in enumerate(self.instruments):
					inst.close()
					print("Instrument {:d} closed.".format(ind))

	def on_ps1_box(self):
		val = self.ps1spinBox.value()
		self.instruments[0].write('SETI ' + str(val))
		print(self.instruments[0].read())
		
		print("Main field set to {:3.2f}A with constant current.".format(val))

	def ps1enable(self):
		inst = self.instruments[0]
		# if button is checked 
		if self.ps1Out.isChecked(): 
			# setting background color to light-blue 
			self.ps1Out.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;") 
			psu.outputs[0].enabled = True
			if psu.outputs[0].enabled == True:
				print("Main field enabled.")
			else:
				print("Main field failed to turn on.")

		# if it is unchecked 
		else:
			# set background color back to light-grey 
			self.ps1Out.setStyleSheet("background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;") 
			psu.outputs[0].enabled = False
			if psu.outputs[0].enabled == False:        
				print("Main field disabled.")
			else:
				print("Main field failed to turn off.")

	def recurring_timer(self):
		if self.sim==False:
			#Update power supply readouts
			for inst in self.instruments:
				self.ps1readspinBox.setProperty("value", inst.query('RDGI?'))
			
	def closeEvent(self, event):
		# Disconnect all devices
		pass

		# and afterwards call the closeEvent of the super-class
		super(QtWidgets.QMainWindow, self).closeEvent(event)
		

if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	app_icon = QtGui.QIcon(r"C:\Users\qlz\Dropbox (ORNL)\Projects\26 - Superconducting Magnet\Lakeshore625\Resources\Lakeshore.png")
	app.setWindowIcon(app_icon)
	
	if len(sys.argv)>1:
		if sys.argv[1] == 'sim':
			tdgui = mainProgram(simulate=True)
		else:
			tdgui = mainProgram()
	else:
		tdgui = mainProgram()
	tdgui.show()
	sys.exit(app.exec_())