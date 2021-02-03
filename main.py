# Code adapted from Chris Baird's repository on github:
# cdbaird/TL-rotation-control

from PyQt5 import QtCore, QtGui, QtWidgets
from td_gui import Ui_TapeDriveWindow
import pyvisa as visa
import math
import matplotlib.pyplot as plt
import array
import numpy as np
import re

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

		self.countfile.clicked.connect(self.get_count_file)

		self.ps1spinBox.valueChanged.connect(self.on_ps1_box)
		self.ps2spinBox.valueChanged.connect(self.on_ps2_box)
		self.ps1Out.toggled.connect(self.ps1enable)
		self.ps2Out.toggled.connect(self.ps2enable)
		
		self.timer = QtCore.QTimer()
		self.timer.setInterval(3000)
		self.timer.timeout.connect(self.recurring_timer)
		self.timer.start()

	def connection(self):
		if self.type == 'gpib':
			if self.con.isChecked():
				self.con.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;")
				self.con.setText("Disconnect\nDevices")
				if self.sim == False:
					print("Connecting devices.")
					self.rm = visa.ResourceManager()
					self.resources = self.rm.list_resources()
					self.instruments = []
					i=0
					for re in self.resources:
						if re[0:3] == 'GPIB':
							self.instruments[i] = self.rm.open_resource(re, read_termination='\r\n', write_termination='\r\n')
							self.instruments[i].write('MODE 1')
							print(self.instruments[i].query('*IDN?"'))
							i = i+1
					if i > 0:
						self.ps1spinBox.setStyleSheet("color: black;")
						self.ps1readspinBox.setStyleSheet("color: black;")
						self.ps1spinBox.setReadOnly(False)
					if i > 1:
						self.ps2spinBox.setStyleSheet("color: black;")
						self.ps2readspinBox.setStyleSheet("color: black;")
						self.ps2spinBox.setReadOnly(False)
				else:
					print("Simulating device connection.")
			else:
				self.con.setStyleSheet("background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;")
				self.ps1spinBox.setReadOnly(True)
				self.ps2spinBox.setReadOnly(True)
				self.con.setText("Connect\nDevices")
				if self.sim == False:
					if len(self.instruments) > 0:
						for ind, inst in enumerate(self.instruments):
							inst.close()
							print("Instrument {:d} closed.".format(ind))
					else:
						print("No instruments to close.")
				else:
					print("Closing simulated connections.")
			
	def get_count_file(self):
		filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,'Open Neutron Count Data', QtCore.QDir.rootPath(), 'Text files (*.txt);;XML files (*.xml)')
		
		current, counts = np.loadtxt(filename, delimiter="\t", skiprows = 1, unpack=True)
		self.sc.axes.cla()  # Clear the canvas.
		self.sc.axes.plot(current, counts)
		self.sc.draw()
		self.centralwidget.show()

	def on_ps1_box(self):
		val = self.ps1spinBox.value()
		if self.sim == False:
			self.instruments[0].write('TRIG ' + str(val))
			print(self.instruments[0].read())
			
		print("Supply 1 set to {:3.2f}A when triggered.".format(val))

	def on_ps2_box(self):
		val = self.ps2spinBox.value()
		if self.sim == False:
			self.instruments[1].write('TRIG ' + str(val))
			print(self.instruments[1].read())
		
		print("Supply 2 set to {:3.2f}A when triggered.".format(val))

	def ps1enable(self):
		if self.sim == False:
			if len(self.instruments) > 0:
				inst = self.instruments[0]
				# if button is checked 
				if self.ps1Out.isChecked(): 
					# setting background color to light-blue 
					self.ps1Out.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;") 
					inst.write('*TRG')
					print("Supply 1 ramping to {:3.2f}A.".format(self.ps1spinBox.value()))
					
				# if it is unchecked 
				else:
					# set background color back to light-grey 
					self.ps1Out.setStyleSheet("background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;") 
					inst.write('STOP')
					print(self.inst.read())
					inst.write('TRIG 0.00')
					print(self.inst.read())
					inst.write('*TRG')       
					print("Supply 1 ramping to 0.00A.")

	def ps2enable(self):
		if self.sim == False:
			if len(self.instruments) > 1:
				inst = self.instruments[1]
				# if button is checked 
				if self.ps2Out.isChecked(): 
					# setting background color to light-blue 
					self.ps2Out.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;") 
					inst.write('*TRG')
					print("Supply 2 ramping to {:3.2f}A.".format(self.ps2spinBox.value()))
					
				# if it is unchecked 
				else:
					# set background color back to light-grey 
					self.ps2Out.setStyleSheet("background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;") 
					inst.write('STOP')
					print(self.inst.read())
					inst.write('TRIG 0.00')
					print(self.inst.read())
					inst.write('*TRG')       
					print("Supply 2 ramping to 0.00A.")

	def recurring_timer(self):
		if self.sim==False:
			#Update power supply readouts
			if len(self.instruments) > 0:
				for inst in self.instruments:
					self.ps1readspinBox.setProperty("value", inst.query('RDGI?'))
			
	def closeEvent(self, event):
		print("Closing program.")
		# Disconnect all devices
		if self.con.isChecked():
			self.con.click()
			
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