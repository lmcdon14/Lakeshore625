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
from scipy import optimize

class mainProgram(QtWidgets.QMainWindow, Ui_TapeDriveWindow):
	def __init__(self, simulate=False):
		super().__init__()
		self.setupUi(self)
		self.sim = simulate
		self.params = [0,0,0,0]
		self.params2 = self.params
		self.current = [0,1,2,3,4]
		self.counts = [10,1,20,3,40]
		self.current2 = self.current
		self.counts2 = self.counts
		self.tester = 0
		self.phi = u"\u03A6"

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
		self.fitdata.clicked.connect(self.fit_count_data)
		self.fitdata2.clicked.connect(self.fit_count_data2)
		self.countfile.clicked.connect(self.get_count_file)
		self.countfile2.clicked.connect(self.get_count_file2)
		self.current_est1.editingFinished.connect(self.est1)
		self.current_est2.editingFinished.connect(self.est2)

		self.ps1spinBox.valueChanged.connect(self.on_ps1_box)
		self.ps2spinBox.valueChanged.connect(self.on_ps2_box)
		self.ps1rampspinBox.valueChanged.connect(self.on_ramp_1)
		self.ps2rampspinBox.valueChanged.connect(self.on_ramp_2)
		self.ps1Out.toggled.connect(self.ps1enable)
		self.ps2Out.toggled.connect(self.ps2enable)

		self.psFlip.clicked.connect(self.switcher)
		
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
					print(self.resources)
					self.instruments = [0]*2
					i=0
					self.switch = 0
					for re in self.resources:
						if re[0:4] == 'GPIB':
							self.instruments[i] = self.rm.open_resource(re, read_termination='\r\n', write_termination='\r\n')
							self.instruments[i].write('MODE 1')
							self.id = self.instruments[i].query('*IDN?"')
							print(self.id)
							if (self.id == 'LSCI,MODEL625,LSA23BX,1.4/1.1') and i==0:
								self.switch = 1
							i = i+1
					#print(self.switch)
					if self.switch == 1:
						intermediate = self.instruments[1]
						self.instruments[1] = self.instruments[0]
						self.instruments[0] = intermediate
					if self.instruments[0] != 0:
						self.ps1spinBox.setStyleSheet("color: black;")
						self.ps1rampspinBox.setStyleSheet("color: black;")
						self.ps1readspinBox.setStyleSheet("color: black;")
						self.ps1spinBox.setReadOnly(False)
						self.ps1rampspinBox.setReadOnly(False)
						self.ps1Out.setEnabled(True)
						val = self.instruments[0].query('RDGI?')
						self.instruments[0].write('TRIG ' + str(val))
						self.ps1readspinBox.setProperty("value", float(val))
						self.ps1spinBox.blockSignals(True)
						self.ps1spinBox.setProperty("value", float(val))
						self.ps1spinBox.blockSignals(False)
						self.ps1rampspinBox.blockSignals(True)
						self.ps1rampspinBox.setProperty("value", 0.000)
						self.ps1rampspinBox.blockSignals(False)
						if (abs(float(val)) >= 0.01):
							if self.ps1Out.isChecked() == False:
								self.ps1Out.blockSignals(True)
								self.ps1Out.toggle()
								self.ps1Out.blockSignals(False)
								self.ps1Out.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;") 
					if self.instruments[1] != 0:
						self.ps2spinBox.setStyleSheet("color: black;")
						self.ps2rampspinBox.setStyleSheet("color: black;")
						self.ps2readspinBox.setStyleSheet("color: black;")
						self.ps2spinBox.setReadOnly(False)
						self.ps2rampspinBox.setReadOnly(False)
						self.ps2Out.setEnabled(True)
						val = self.instruments[1].query('RDGI?')
						self.instruments[1].write('TRIG ' + str(val))
						self.ps2readspinBox.setProperty("value", float(val))
						self.ps2spinBox.blockSignals(True)
						self.ps2spinBox.setProperty("value", float(val))
						self.ps2spinBox.blockSignals(False)
						self.ps2rampspinBox.blockSignals(True)
						self.ps2rampspinBox.setProperty("value", 0.000)
						self.ps2rampspinBox.blockSignals(False)
						if (abs(float(val)) >= 0.01):
							if self.ps2Out.isChecked() == False:
								self.ps2Out.blockSignals(True)
								self.ps2Out.toggle()
								self.ps2Out.blockSignals(False)
								self.ps2Out.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;") 
				else:
					print("Simulating device connection.")
			else:
				self.con.setStyleSheet("background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;")
				self.ps1spinBox.setReadOnly(True)
				self.ps2spinBox.setReadOnly(True)
				self.ps1rampspinBox.setReadOnly(True)
				self.ps2rampspinBox.setReadOnly(True)
				self.ps1Out.setEnabled(False)
				self.ps2Out.setEnabled(False)
				self.ps1Out.setStyleSheet("background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;") 
				self.ps2Out.setStyleSheet("background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;") 
				self.ps1spinBox.setStyleSheet("color: lightgrey;")
				self.ps1rampspinBox.setStyleSheet("color: lightgrey;")
				self.ps1readspinBox.setStyleSheet("color: lightgrey;")
				self.ps2spinBox.setStyleSheet("color: lightgrey;")
				self.ps2rampspinBox.setStyleSheet("color: lightgrey;")
				self.ps2readspinBox.setStyleSheet("color: lightgrey;")
				self.con.setText("Connect\nDevices")
				if self.sim == False:
					if len(self.instruments) > 0:
						for ind, inst in enumerate(self.instruments):
							if inst != 0:
								inst.close()
								print("Instrument {:d} closed.".format(ind))
								inst = 0
					else:
						print("No instruments to close.")
				else:
					print("Closing simulated connections.")

	def switcher(self):
		if self.sim == False:
			if self.con.isChecked() and (self.instruments[0] != 0 or self.instruments[1] != 0):
				print("Switching order of power supplies")
				intermediate = self.instruments[1]
				self.instruments[1] = self.instruments[0]
				self.instruments[0] = intermediate

				# switch all widgets to match new instrument order 
				# switch setpoint spinbox (enabled, value, stylesheet)
				# switch ramp setpoint spinbox (enabled, value, stylesheet, stop timers)
				# switch readout spinbox (stylesheet)
				# switch output button (enabled, state, stylesheet)
				# NEED TO ADD SWITCHING FOR PLOTS TOO!

				# directly switch PS1 and PS2 (PS2 to PS1)
				if self.ps1spinBox.isReadOnly():
					if self.ps2spinBox.isReadOnly() == False:
						self.ps1spinBox.setReadOnly(False)
						self.ps1rampspinBox.setReadOnly(False)
						self.ps1spinBox.setStyleSheet("color: black;")
						self.ps1rampspinBox.setStyleSheet("color: black;")
						self.ps1readspinBox.setStyleSheet("color: black;")
						self.ps1spinBox.blockSignals(True)
						self.ps1spinBox.setProperty("value", self.ps2spinBox.value())
						self.ps1spinBox.blockSignals(False)
						self.ps1rampspinBox.blockSignals(True)
						self.ps1rampspinBox.setProperty("value", 0.000)
						self.ps1rampspinBox.blockSignals(False)
						if self.ramp2recurring_timer.isActive():
							self.ramp2recurring_timer.stop()
							print("Stopping current ramp")

						self.ps1Out.setEnabled(True)
						if self.ps2Out.isChecked() == True:
							self.ps1Out.blockSignals(True)
							self.ps1Out.toggle()
							self.ps1Out.blockSignals(False)
							self.ps1Out.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;") 
						self.ps2spinBox.setReadOnly(True)
						self.ps2rampspinBox.setReadOnly(True)
						self.ps2spinBox.blockSignals(True)
						self.ps2spinBox.setProperty("value", 0.00)
						self.ps2readspinBox.setProperty("value", 0.00)
						self.ps2spinBox.blockSignals(False)
						self.ps2rampspinBox.blockSignals(True)
						self.ps2rampspinBox.setProperty("value", 0.000)
						self.ps2rampspinBox.blockSignals(False)
						self.ps2spinBox.setStyleSheet("color: lightgrey;")
						self.ps2rampspinBox.setStyleSheet("color: lightgrey;")
						self.ps2readspinBox.setStyleSheet("color: lightgrey;")
						self.ps2Out.setEnabled(False)
						self.ps2Out.setStyleSheet("background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;")
				# directly switch PS1 and PS2 (PS1 to PS2)
				elif self.ps2spinBox.isReadOnly():
					self.ps2spinBox.setReadOnly(False)
					self.ps2rampspinBox.setReadOnly(False)
					self.ps2spinBox.setStyleSheet("color: black;")
					self.ps2rampspinBox.setStyleSheet("color: black;")
					self.ps2readspinBox.setStyleSheet("color: black;")
					self.ps2spinBox.blockSignals(True)
					self.ps2spinBox.setProperty("value", self.ps1spinBox.value())
					self.ps2spinBox.blockSignals(False)
					self.ps2rampspinBox.blockSignals(True)
					self.ps2rampspinBox.setProperty("value", 0.000)
					self.ps2rampspinBox.blockSignals(False)
					if self.ramp1recurring_timer.isActive():
						self.ramp1recurring_timer.stop()
						print("Stopping current ramp")

					self.ps2Out.setEnabled(True)
					if self.ps1Out.isChecked() == True:
						self.ps2Out.blockSignals(True)
						self.ps2Out.toggle()
						self.ps2Out.blockSignals(False)
						self.ps2Out.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;") 
					self.ps1spinBox.setReadOnly(True)
					self.ps1rampspinBox.setReadOnly(True)
					self.ps1spinBox.blockSignals(True)
					self.ps1spinBox.setProperty("value", 0.00)
					self.ps1readspinBox.setProperty("value", 0.00)
					self.ps1spinBox.blockSignals(False)
					self.ps1rampspinBox.blockSignals(True)
					self.ps1rampspinBox.setProperty("value", 0.000)
					self.ps1rampspinBox.blockSignals(False)
					self.ps1spinBox.setStyleSheet("color: lightgrey;")
					self.ps1rampspinBox.setStyleSheet("color: lightgrey;")
					self.ps1readspinBox.setStyleSheet("color: lightgrey;")
					self.ps1Out.setEnabled(False)
					self.ps1Out.setStyleSheet("background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;")
				# save intermediate values and switch everything
				else:
					if self.ramp1recurring_timer.isActive():
						self.ramp1recurring_timer.stop()
						print("Stopping current ramp 1")
					if self.ramp2recurring_timer.isActive():
						self.ramp2recurring_timer.stop()
						print("Stopping current ramp 2")

					self.ps1rampspinBox.blockSignals(True)
					self.ps1rampspinBox.setProperty("value", 0.000)
					self.ps1rampspinBox.blockSignals(False)
					self.ps2rampspinBox.blockSignals(True)
					self.ps2rampspinBox.setProperty("value", 0.000)
					self.ps2rampspinBox.blockSignals(False)

					val1 = self.ps2spinBox.value()
					self.ps2spinBox.blockSignals(True)
					self.ps2spinBox.setProperty("value", self.ps1spinBox.value())
					self.ps2spinBox.blockSignals(False)
					self.ps1spinBox.blockSignals(True)
					self.ps1spinBox.setProperty("value", val1)
					self.ps1spinBox.blockSignals(False)


					if self.ps1Out.isChecked() != self.ps2Out.isChecked():
						state1 = self.ps2Out.isChecked()

						self.ps2Out.blockSignals(True)
						self.ps2Out.toggle()
						self.ps2Out.blockSignals(False)
						self.ps1Out.blockSignals(True)
						self.ps1Out.toggle()
						self.ps1Out.blockSignals(False)

						if state1 == True:
							self.ps2Out.setStyleSheet("background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;") 
							self.ps1Out.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;") 
						else:
							self.ps1Out.setStyleSheet("background-color: rgba(0,0,0,0.5); color: white; border-radius:4px;") 
							self.ps2Out.setStyleSheet("background-color: lightblue; color: white; border-radius:4px;") 

			
	def get_count_file(self):
		filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,'Open Neutron Count Data', QtCore.QDir.rootPath(), 'Text files (*.txt);;XML files (*.xml)')
		print(filename)
		if filename != '':
			self.current, self.counts = np.loadtxt(filename, delimiter="\t", skiprows = 1, unpack=True)
			self.sc0.axes.cla()  # Clear the canvas.
			self.sc0.axes.set_xlabel('Current(A)')
			self.sc0.axes.set_ylabel('Neutron Counts')
			self.sc0.axes.plot(self.current, self.counts)
			self.sc0.draw()
			self.centralwidget.show()

			self.fitdata.setEnabled(True)

	def get_count_file2(self):
		filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,'Open Neutron Count Data', QtCore.QDir.rootPath(), 'Text files (*.txt);;XML files (*.xml)')
		print(filename)
		if filename != '':
			self.current2, self.counts2 = np.loadtxt(filename, delimiter="\t", skiprows = 1, unpack=True)
			self.sc1.axes.cla()  # Clear the canvas.
			self.sc1.axes.set_xlabel('Current(A)')
			self.sc1.axes.set_ylabel('Neutron Counts')
			self.sc1.axes.plot(self.current2, self.counts2)
			self.sc1.draw()
			self.centralwidget.show()

			self.fitdata2.setEnabled(True)

	def test_func(self, x, a=0, b=0, p=0, c=0):
		return a * np.cos(b * x + p) + c 

	def fit_count_data(self):
		ind_max = np.argmax(self.counts)
		ind_min = np.argmin(self.counts)
		freq = (math.pi)/(abs(self.current[ind_max] - self.current[ind_min]))
		if self.current[ind_min] == 0:
			phase = 0
		else:
			phase = -math.pi/self.current[ind_min]
		
		if self.A1.value() == 0.0:
			p1 = float((max(self.counts)-min(self.counts))/2)
			self.A1.setProperty("value", p1)
		else:
			p1 = self.A1.value()
		if self.b1.value() == 0.0:
			p2 = float(freq)
			self.b1.setProperty("value", p2)
		else:
			p2 = self.b1.value()
		if self.phi1.value() == 0.0:
			p3 = float(phase)
			self.phi1.setProperty("value", p3)
		else:
			p3 = self.phi1.value()
		if self.c1.value() == 0.0:
			p4 = float(max(self.counts)/2)
			self.c1.setProperty("value", p4)
		else:
			p4 = self.c1.value()
		self.params, params_covariance = optimize.curve_fit(self.test_func, self.current, self.counts, p0=[p1, p2, p3, p4])
		print(self.params)

		self.A1read.setProperty("value", float(self.params[0]))
		self.b1read.setProperty("value", float(self.params[1]))
		self.phi1read.setProperty("value", float(self.params[2]))
		self.c1read.setProperty("value", float(self.params[3]))

		#print(params_covariance)
		self.sc0.axes.cla()  # Clear the canvas.
		self.sc0.axes.set_xlabel('Current(A)')
		self.sc0.axes.set_ylabel('Neutron Counts')
		self.sc0.axes.plot(self.current, self.counts, label='Raw Counts')
		self.sc0.axes.plot(self.current, self.test_func(self.current, self.params[0], self.params[1], self.params[2], self.params[3]), label='Acos(bi+' + self.phi + ')+c')
		self.sc0.axes.legend(loc='best')
		self.sc0.draw()
		self.centralwidget.show()

		self.current_est1.setEnabled(True)

	def fit_count_data2(self):
		ind_max = np.argmax(self.counts2)
		ind_min = np.argmin(self.counts2)
		freq = (math.pi)/(abs(self.current2[ind_max] - self.current2[ind_min]))
		if self.current2[ind_min] == 0:
			phase = 0
		else:
			phase = -math.pi/self.current2[ind_min]

		if self.A2.value() == 0.0:
			p1 = float((max(self.counts2)-min(self.counts2))/2)
			self.A2.setProperty("value", p1)
		else:
			p1 = self.A2.value()
		if self.b2.value() == 0.0:
			p2 = float(freq)
			self.b2.setProperty("value", p2)
		else:
			p2 = self.b2.value()
		if self.phi2.value() == 0.0:
			p3 = float(phase)
			self.phi2.setProperty("value", p3)
		else:
			p3 = self.phi2.value()
		if self.c2.value() == 0.0:
			p4 = float(max(self.counts2)/2)
			self.c2.setProperty("value", p4)
		else:
			p4 = self.c2.value()

		self.params2, params_covariance = optimize.curve_fit(self.test_func, self.current2, self.counts2, p0=[p1, p2, p3, p4])
		print(self.params2)
		self.A2read.setProperty("value", float(self.params2[0]))
		self.b2read.setProperty("value", float(self.params2[1]))
		self.phi2read.setProperty("value", float(self.params2[2]))
		self.c2read.setProperty("value", float(self.params2[3]))

		#print(params_covariance)
		self.sc1.axes.cla()  # Clear the canvas.
		self.sc1.axes.set_xlabel('Current(A)')
		self.sc1.axes.set_ylabel('Neutron Counts')
		self.sc1.axes.plot(self.current2, self.counts2, label='Raw Counts')
		self.sc1.axes.plot(self.current2, self.test_func(self.current2, self.params2[0], self.params2[1], self.params2[2], self.params2[3]), label='Acos(bi+' + self.phi+ ')+c')
		self.sc1.axes.legend(loc='best')
		self.sc1.draw()
		self.centralwidget.show()

		self.current_est2.setEnabled(True)

	def est1(self):
		val = self.current_est1.text()
		check = val.find('/')
		if check != -1:
			ind = val.index('/')
			coef = float(val[:ind])/float(val[ind+1:])
		else:
			coef = float(val)
		self.current_est1.setText("{:5.3f}".format(coef))

		if self.params[1] != 0:
			self.i_est = (coef*math.pi-self.params[2]-math.pi)/self.params[1]
		else:
			self.i_est = (coef*math.pi-self.params[2]-math.pi)

		self.count_est = self.test_func(self.i_est, self.params[0], self.params[1], self.params[2], self.params[3])
		
		self.sc0.axes.cla()  # Clear the canvas.
		self.sc0.axes.set_xlabel('Current(A)')
		self.sc0.axes.set_ylabel('Neutron Counts')
		self.sc0.axes.plot(self.current, self.counts, label='Raw Counts')
		self.sc0.axes.plot(self.current, self.test_func(self.current, self.params[0], self.params[1], self.params[2], self.params[3]), label='A*cos(b*i+phi)+c')
		self.sc0.axes.plot(self.i_est, self.count_est, 'r*', markersize=10)
		self.sc0.axes.legend(loc='best')
		self.sc0.draw()
		self.centralwidget.show()

		self.val_est1.setEnabled(True)
		self.val_est1.setText("{:5.3f}".format(self.i_est))

	def est2(self):
		val = self.current_est2.text()
		check = val.find('/')
		if check != -1:
			ind = val.index('/')
			coef = float(val[:ind])/float(val[ind+1:])
		else:
			coef = float(val)
		self.current_est2.setText("{:5.3f}".format(coef))

		if self.params2[1] != 0:
			self.i_est2 = (coef*math.pi-self.params2[2]-math.pi)/self.params2[1]
		else:
			self.i_est2 = (coef*math.pi-self.params2[2]-math.pi)

		self.count_est2 = self.test_func(self.i_est2, self.params2[0], self.params2[1], self.params2[2], self.params2[3])
		
		self.sc1.axes.cla()  # Clear the canvas.
		self.sc1.axes.set_xlabel('Current(A)')
		self.sc1.axes.set_ylabel('Neutron Counts')
		self.sc1.axes.plot(self.current2, self.counts2, label='Raw Counts')
		self.sc1.axes.plot(self.current2, self.test_func(self.current2, self.params2[0], self.params2[1], self.params2[2], self.params2[3]), label='A*cos(b*i+phi)+c')
		self.sc1.axes.plot(self.i_est2, self.count_est2, 'r*', markersize=10)
		self.sc1.axes.legend(loc='best')
		self.sc1.draw()
		self.centralwidget.show()

		self.val_est2.setEnabled(True)
		self.val_est2.setText("{:5.3f}".format(self.i_est2))

	def on_ps1_box(self):
		val = self.ps1spinBox.value()
		if self.sim == False:
			self.instruments[0].write('TRIG ' + str(val))
			if self.ps1Out.isChecked():
				self.instruments[0].write('*TRG')
				print("Supply 1 ramping to {:3.2f}A.".format(val))
			else:
				print("Supply 1 set to {:3.2f}A when triggered.".format(val))
			#print(self.instruments[0].read())
		else:
			print("Supply 1 set to {:3.2f}A when triggered.".format(val))

	def on_ps2_box(self):
		val = self.ps2spinBox.value()
		if self.sim == False:
			self.instruments[1].write('TRIG ' + str(val))
			if self.ps2Out.isChecked():
				self.instruments[1].write('*TRG')
				print("Supply 2 ramping to {:3.2f}A.".format(val))
			else:
				print("Supply 2 set to {:3.2f}A when triggered.".format(val))
			#print(self.instruments[1].read())
		else:
			print("Supply 2 set to {:3.2f}A when triggered.".format(val))

	# Add ramp text box with format: scan [start_current] [end_current] [current_step]
	# Add universal time box for time rates
	def on_ramp_1(self):
		if self.ramp1timer.isActive():
			self.ramptimer.stop()

		self.ramp1timer = QtCore.QTimer()
		self.ramp1timer.setInterval(10000)
		self.ramp1timer.timeout.connect(self.ramp1recurring_timer)
		self.ramp1timer.start()

	def ramp1recurring_timer(self):
		pass
		# do all the ramping logic from MIS Code

	def on_ramp_2(self):
		self.ramp2timer = QtCore.QTimer()
		self.ramp2timer.setInterval(10000)
		self.ramp2timer.timeout.connect(self.ramp2recurring_timer)
		self.ramp2timer.start()

	def ramp2recurring_timer(self):
		pass
		# do all the ramping logic from MIS Code

	def ps1enable(self):
		if self.sim == False:
			if self.instruments[0] != 0:
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
					#print(self.inst.read())
					#inst.write('TRIG 0.00')
					#print(self.inst.read())
					#inst.write('*TRG')       
					inst.write('SETI 0.00')
					print("Supply 1 ramping to 0.00A.")
					inst.write('TRIG ' + str(self.ps1spinBox.value()))

	def ps2enable(self):
		if self.sim == False:
			if self.instruments[1] != 0:
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
					#print(self.inst.read())
					#inst.write('TRIG 0.00')
					#print(self.inst.read())
					#inst.write('*TRG')       
					inst.write('SETI 0.00')
					print("Supply 2 ramping to 0.00A.")
					inst.write('TRIG ' + str(self.ps2spinBox.value()))

	def recurring_timer(self):
		if self.sim==False:
			if self.con.isChecked():
				self.tester += 1 
				#Update power supply readouts
				if len(self.instruments) > 0:
					#print(self.instruments)
					for i,inst in enumerate(self.instruments):
						if inst != 0:
							#print(inst)
							val = inst.query('RDGI?')
							if i==0:
								self.ps1readspinBox.setProperty("value", float(val))
							else:
								self.ps2readspinBox.setProperty("value", float(val))
			
	def closeEvent(self, event):
		print("Closing program.")
		# Disconnect all devices
		if self.con.isChecked():
			self.con.click()
			
		# and afterwards call the closeEvent of the super-class
		super(QtWidgets.QMainWindow, self).closeEvent(event)
		

if __name__ == '__main__':
	import sys
	#QtWidgets.QApplication.setAttribute(QtCore.Qt.
	#QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
	#QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
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