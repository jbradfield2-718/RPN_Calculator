''' 
	Copyright 2014 J. Bradfield
	This file is part of TrueRPN.

	TrueRPN is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	TrueRPN is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with TrueRPN.  If not, see <http://www.gnu.org/licenses/>.
'''
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rpn_calc_rev0.ui'
#
# Created: Sat Apr 19 16:45:02 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtWebKit import QWebView
from display_gui import display_start, functions, show_constants, manual, about
import main, dialog, csv, cmath, config
from main import history

global prev_commands, cmd_cnt
prev_commands = []
cmd_cnt = 0

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

global angle_mode_flag, entry_mode_flag, result_format_flag, load_stack_flag		# 0 == degrees, 1 == radians
entry_mode_flag = 0																		# 0 == rpn, 1 == algebraic
angle_mode_flag = 0
fixed_digits_flag = 3
results_format_flag = 1													# 1 == general, 3 == sci, 2 == fixed, 4 == eng
load_stack_flag = 1
																						

class Popup(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)
		#self.centralwidget = QtGui.QWidget
		#self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
		self.QWebView = QWebView(self)
		self.QWebView.resize(350,400)
		self.resize(350, 400)

class Window(QtGui.QMainWindow):
	def __init__(self):
		super(Window, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
	def closeEvent(self, event):
		try:
			msgbox.close()
		except:
			pass

		try:
			self.ui.save_stack()
		except:
			pass
			
		#self.closing.emit()

		super(MainWindow, self).closeEvent(event)

#===========================================================
	#Implements keypress history for calculator.  Up/down arrow cycles back/forth in
	#command history.
#============================================================
	def keyPressEvent(self, ev):
		global prev_commands, cmd_cnt, results_format_flag, fixed_digits_flag
		
		if ev.key() == 0x01000013:							# hex code for up arrow.

			try:
				if cmd_cnt > 0:
					cmd_cnt -= 1
					self.ui.qLineEdit.setText( prev_commands[cmd_cnt] )
			except IndexError:
				pass
				
		if ev.key() == 0x01000015:
			try:
				if cmd_cnt < len(prev_commands) -1:
					cmd_cnt += 1
					self.ui.qLineEdit.setText( prev_commands[cmd_cnt] )
			except IndexError:
				pass
				
		if ev.key() == QtCore.Qt.Key_Escape:
			try:
				config.stack.pop()
				self.ui.refresh_display()		# This simple line of code took approx 1 hr to figure out.  Love OOP!
				
			except:
				pass
				
			
				
class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		global load_stack_flag

		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(431, 489)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
		self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.verticalLayout_2 = QtGui.QVBoxLayout()
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		
	#---RPN RADIO BUTTON----------------------------------------------------------------------------------------------
		self.radioButton_rpn = QtGui.QRadioButton(self.centralwidget)
		self.radioButton_rpn.setChecked(True)
		self.radioButton_rpn.setObjectName(_fromUtf8("radioButton_rpn"))
		self.buttonGroup = QtGui.QButtonGroup(MainWindow)
		self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
		self.buttonGroup.addButton(self.radioButton_rpn)
		self.verticalLayout_2.addWidget(self.radioButton_rpn)
	#---ALGEBRAIC RADIO BUTTON---------------------------------------------------------------------------------------
		self.radioButton_algebraic = QtGui.QRadioButton(self.centralwidget)
		self.radioButton_algebraic.setObjectName(_fromUtf8("radioButton_algebraic"))
		self.buttonGroup.addButton(self.radioButton_algebraic)
		self.verticalLayout_2.addWidget(self.radioButton_algebraic)
		
		self.horizontalLayout.addLayout(self.verticalLayout_2)
		self.line = QtGui.QFrame(self.centralwidget)
		self.line.setFrameShape(QtGui.QFrame.VLine)
		self.line.setFrameShadow(QtGui.QFrame.Sunken)
		self.line.setObjectName(_fromUtf8("line"))
		self.horizontalLayout.addWidget(self.line)
		self.verticalLayout_3 = QtGui.QVBoxLayout()
		self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
		
	#---DEGREES RADIO BUTTON----------------------------------------------------------------------------------------------
		self.radioButton_degrees = QtGui.QRadioButton(self.centralwidget)
		self.radioButton_degrees.setChecked(True)
		self.radioButton_degrees.setObjectName(_fromUtf8("radioButton_degrees"))
		self.buttonGroup_2 = QtGui.QButtonGroup(MainWindow)
		self.buttonGroup_2.setObjectName(_fromUtf8("buttonGroup_2"))
		self.buttonGroup_2.addButton(self.radioButton_degrees)
		self.verticalLayout_3.addWidget(self.radioButton_degrees)
			
	#---RPN RADIANS BUTTON----------------------------------------------------------------------------------------------
		self.radioButton_radians = QtGui.QRadioButton(self.centralwidget)
		self.radioButton_radians.setObjectName(_fromUtf8("radioButton_radians"))
		self.buttonGroup_2.addButton(self.radioButton_radians)
		self.verticalLayout_3.addWidget(self.radioButton_radians)
		self.horizontalLayout.addLayout(self.verticalLayout_3)
		self.verticalLayout_4.addLayout(self.horizontalLayout)
		self.verticalLayout = QtGui.QVBoxLayout()
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
	
	#---QWebView------------------------------------------------------------------------------------------------------
		self.QWebView = QWebView(self.centralwidget)
		self.QWebView.setObjectName(_fromUtf8("QWebView"))
		self.verticalLayout.addWidget(self.QWebView)
		
		
	#---QLINEEDIT------------------------------------------------------------------------------------------------------
		self.qLineEdit = QtGui.QLineEdit(self.centralwidget)
		self.qLineEdit.setMaximumSize(QtCore.QSize(16777215, 30))
		self.qLineEdit.setObjectName(_fromUtf8("qLineEdit"))
		self.verticalLayout.addWidget(self.qLineEdit)
		self.verticalLayout_4.addLayout(self.verticalLayout)
		MainWindow.setCentralWidget(self.centralwidget)
		
		
		
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 431, 21))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		
		self.menuFile = QtGui.QMenu(self.menubar)
		self.menuFile.setObjectName(_fromUtf8("menuFile"))
		
		self.menuDisplay = QtGui.QMenu(self.menubar)
		self.menuDisplay.setObjectName(_fromUtf8("menuDisplay"))
		
		self.menuFormat = QtGui.QMenu(self.menubar)
		self.menuFormat.setObjectName(_fromUtf8("menuFormat"))
		
		self.menuHelp = QtGui.QMenu(self.menubar)
		self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
		
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)

		#=====File Dropdown List============================================
		self.actionSave_Ctrl_S = QtGui.QAction(MainWindow)
		self.actionSave_Ctrl_S.setObjectName(_fromUtf8("actionSave_Ctrl_S"))
		self.actionSave_Ctrl_S.setShortcut('Ctrl+S')
		self.actionSave_Ctrl_S.setStatusTip('Save Calculation History')
		self.actionSave_Ctrl_S.triggered.connect(self.save_history)
	
		self.actionLoad_Ctrl_L = QtGui.QAction(MainWindow)
		self.actionLoad_Ctrl_L.setObjectName(_fromUtf8("actionLoad_Ctrl_L"))
		self.actionLoad_Ctrl_L.setShortcut('Ctrl+L')
		self.actionLoad_Ctrl_L.setStatusTip('Load Previous Calcs')
		self.actionLoad_Ctrl_L.triggered.connect(self.load_history)
		
		#=====Display Dropdown List============================================
		self.actionFunctions = QtGui.QAction(MainWindow)
		self.actionFunctions.setObjectName(_fromUtf8("actionFunctions"))
		self.actionFunctions.setStatusTip('Show available functions')
		self.actionFunctions.triggered.connect(self.display_functions)
		
		self.actionConstants = QtGui.QAction(MainWindow)
		self.actionConstants.setObjectName(_fromUtf8("actionConstants"))
		self.actionConstants.setStatusTip('Shows currently available constants')
		self.actionConstants.triggered.connect(self.display_constants)
		
		self.actionclear_stack_Ctrl_N = QtGui.QAction(MainWindow)
		self.actionclear_stack_Ctrl_N.setObjectName(_fromUtf8("actionclear_stack_Ctrl_N"))
		self.actionclear_stack_Ctrl_N.setShortcut('Ctrl+N')
		self.actionclear_stack_Ctrl_N.setStatusTip('Clear Current config.stack')
		self.actionclear_stack_Ctrl_N.triggered.connect(self.clear_stack)
		
		#=====Format Dropdown List==========================================
		self.actionFixed = QtGui.QAction(MainWindow)
		self.actionFixed.setObjectName(_fromUtf8("actionFixed"))
		self.actionFixed.setCheckable(True)
		self.actionFixed.setChecked(False)
		self.actionFixed.setShortcut('Ctrl+2')
		self.actionFixed.setStatusTip('Results displayed with fixed number of digits past decimal')
		self.actionFixed.triggered.connect(self.set_fixed)
		
		self.actionScientific = QtGui.QAction(MainWindow)
		self.actionScientific.setObjectName(_fromUtf8("actionScientific"))
		self.actionScientific.setCheckable(True)
		self.actionScientific.setChecked(False)
		self.actionScientific.setShortcut('Ctrl+3')
		self.actionScientific.setStatusTip('Results displayed in scientific notation')
		self.actionScientific.triggered.connect(self.set_scientific)
		
		self.actionGeneral = QtGui.QAction(MainWindow)
		self.actionGeneral.setObjectName(_fromUtf8("actionGeneral"))
		self.actionGeneral.setCheckable(True)
		self.actionGeneral.setChecked(True)
		self.actionGeneral.setShortcut('Ctrl+1')
		self.actionGeneral.setStatusTip('No specific result formatting')
		self.actionGeneral.triggered.connect(self.set_general)
		
		self.actionEngineering = QtGui.QAction(MainWindow)
		self.actionEngineering.setObjectName(_fromUtf8("actionEngineering"))
		self.actionEngineering.setCheckable(True)
		self.actionEngineering.setChecked(False)
		self.actionEngineering.setShortcut('Ctrl+4')
		self.actionEngineering.setStatusTip('Results displayed in Engineering format')
		self.actionEngineering.triggered.connect(self.set_engineering)
		
		#=====Help Dropdown List============================================
		self.actionManual = QtGui.QAction(MainWindow)
		self.actionManual.setObjectName(_fromUtf8("actionManual"))
		self.actionManual.triggered.connect(self.display_manual)
		
		self.actionAbout = QtGui.QAction(MainWindow)
		self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
		self.actionAbout.triggered.connect(self.display_about)
		#==============================================================
		
		self.menuFile.addAction(self.actionSave_Ctrl_S)
		self.menuFile.addAction(self.actionLoad_Ctrl_L)
		
		self.menuDisplay.addAction(self.actionclear_stack_Ctrl_N)
		self.menuDisplay.addAction(self.actionFunctions)
		self.menuDisplay.addAction(self.actionConstants)
		
		self.menuFormat.addAction(self.actionGeneral)
		self.menuFormat.addAction(self.actionFixed)
		self.menuFormat.addAction(self.actionScientific)
		self.menuFormat.addAction(self.actionEngineering)
		
		self.menuHelp.addAction(self.actionManual)
		self.menuHelp.addAction(self.actionAbout)
		
		self.menubar.addAction(self.menuFile.menuAction())
		self.menubar.addAction(self.menuDisplay.menuAction())
		self.menubar.addAction(self.menuFormat.menuAction())
		self.menubar.addAction(self.menuHelp.menuAction())

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		MainWindow.setTabOrder(self.qLineEdit, self.QWebView)
		MainWindow.setTabOrder(self.QWebView, self.radioButton_rpn)
		MainWindow.setTabOrder(self.radioButton_rpn, self.radioButton_algebraic)
		MainWindow.setTabOrder(self.radioButton_algebraic, self.radioButton_degrees)
		MainWindow.setTabOrder(self.radioButton_degrees, self.radioButton_radians)
		

		self.qLineEdit.returnPressed.connect( self.calculate_input )
		self.radioButton_radians.toggled.connect( self.set_angle_mode )
		self.radioButton_rpn.toggled.connect( self.set_entry_mode )

		if load_stack_flag == 1:
			try:
				load_stack_flag = 0
				self.load_stack()
			except:
				pass

		self.refresh_display()

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "TrueRPN", None))
		self.radioButton_rpn.setText(_translate("MainWindow", "RPN", None))
		self.radioButton_algebraic.setText(_translate("MainWindow", "ALGEBRAIC", None))
		self.radioButton_degrees.setText(_translate("MainWindow", "DEGREES", None))
		self.radioButton_radians.setText(_translate("MainWindow", "RADIANS", None))
		self.menuFile.setTitle(_translate("MainWindow", "File", None))
		self.menuDisplay.setTitle(_translate("MainWindow", "Display", None))
		self.menuFormat.setTitle(_translate("MainWindow", "Format", None))
		self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
		self.actionSave_Ctrl_S.setText(_translate("MainWindow", "Save", None))
		self.actionLoad_Ctrl_L.setText(_translate("MainWindow", "Load", None))
		self.actionFunctions.setText(_translate("MainWindow", "Functions", None))
		self.actionConstants.setText(_translate("MainWindow", "Constants", None))
		self.actionclear_stack_Ctrl_N.setText(_translate("MainWindow", "Clear config.stack	  Ctrl + N", None))
		self.actionGeneral.setText(_translate("MainWindow", "General Results", None))
		self.actionFixed.setText(_translate("MainWindow", "Fixed", None))
		self.actionScientific.setText(_translate("MainWindow", "Scientific", None))
		self.actionEngineering.setText(_translate("MainWindow", "Engineering", None))
		
		self.actionManual.setText(_translate("MainWindow", "Manual", None))
		self.actionAbout.setText(_translate("MainWindow", "About", None))
		
	def refresh_display(self):
		global results_format_flag, entry_mode_flag
		print(config.stack)
		display_start(self, config.stack, results_format_flag, fixed_digits_flag)
	
	def calculate_input(self):
		global cmd_cnt, results_format_flag, entry_mode_flag
		text = self.qLineEdit.text()
		cmd_cnt += 1													# increments command count
		prev_commands.append(text)							# add command to history
		self.qLineEdit.clear()
		
		#------RPN ENTRY MODE----------------------------------------------------------------------------------------
		if entry_mode_flag == 0:
			config.stack = main.rpn_calc( text, angle_mode_flag )
			if config.stack == 'Error':
				self.qLineEdit.setText(config.stack)
			else:
				self.refresh_display()				# Sends config.stack and formatting flag to be displayed
		
		#------ALGEBRAIC ENTRY MODE----------------------------------------------------------------------------------
		if entry_mode_flag == 1:
			self.qLineEdit.setText('Currently no support for algebraic mode!  To be added in next release!')
			
		#self.QWebView.setScrollBarPolicy(QWebView.End)
		return
		
	def set_angle_mode(self):
		global angle_mode_flag

		if angle_mode_flag == 1:
			angle_mode_flag = 0
			return
		else:
			angle_mode_flag = 1
			return
			
	def set_entry_mode(self):
		global entry_mode_flag

		if entry_mode_flag == 1:
			entry_mode_flag = 0
			return
		else:
			entry_mode_flag = 1
			self.qLineEdit.setText('Currently no support for algebraic mode!  To be added in next release!')
			return
#=======================================================================================================================
#   FILE DROPDOWN MENU FUNCTIONS
#=======================================================================================================================
	def save_history(self):
		global history
		print (history)
		
	def load_history(self):
		pass
#=======================================================================================================================
#   DISPLAY DROPDOWN MENU FUNCTIONS
#=======================================================================================================================
	def display_constants(self):
		#msgbox = dialog.Dialog()
		msgbox = Popup()
		constants = main.return_constants()
		msgbox.QWebView.setContent( show_constants(constants) )
		msgbox.show()
		msgbox.app.exec_()
#-------------------------------------------------------------------------------------------------------------------
	def display_functions(self):
		msgbox = Popup()
		constants = main.return_constants()
		msgbox.QWebView.setHtml( functions() )
		msgbox.show()
		msgbox.app.exec_()
#-------------------------------------------------------------------------------------------------------------------
	def clear_stack(self):
		config.stack = main.clear_stack()
		print(config.stack)
		self.refresh_display()
		return
#=======================================================================================================================
#   FORMAT DROPDOWN MENU FUNCTIONS
#=======================================================================================================================
	def set_fixed(self):
	# 1 == general, 3 == sci, 2 == fixed, 4 == eng
		global results_format_flag, fixed_digits_flag
		results_format_flag = 2
		self.actionScientific.setChecked(False)
		self.actionGeneral.setChecked(False)
		self.actionEngineering.setChecked(False)

		msgbox = QtGui.QInputDialog()
		input = QtGui.QInputDialog.getText(msgbox, 'Fixed Mode', 'Enter number of digits after decimal:')
		#input.exec_()
		
		if input:
			while True:
				try:
					fixed_digits = int(input[0])
					break
				except Exception as e:
					input = QtGui.QInputDialog.getText(msgbox, 'Fixed Mode', 'Enter number of digits after decimal:')
		
		fixed_digits_flag = input	[0]
		self.refresh_display()
		#self.QWebView.setScrollBarPolicy(QWebView.End)
		
		return
#-------------------------------------------------------------------------------------------------------------------
	def set_scientific(self):
	# 1 == general, 3 == sci, 2 == fixed, 4 == eng
		global results_format_flag
		results_format_flag = 3
		self.actionFixed.setChecked(False)
		self.actionGeneral.setChecked(False)
		self.actionEngineering.setChecked(False)
		
		msgbox = QtGui.QInputDialog()
		input = QtGui.QInputDialog.getText(msgbox, 'Scientific Mode', 'Enter number of digits after decimal:')
		#input.exec_()
		
		if input:
			while True:
				try:
					fixed_digits = int(input[0])
					break
				except Exception as e:
					input = QtGui.QInputDialog.getText(msgbox, 'Scientific Mode',
													   'Enter number of digits after decimal:')
		
		fixed_digits_flag = input	[0]
		self.refresh_display()
		
		return
#-------------------------------------------------------------------------------------------------------------------
	def set_general(self):
	# 1 == general, 3 == sci, 2 == fixed, 4 == eng
		global results_format_flag
		results_format_flag = 1
		self.actionScientific.setChecked(False)
		self.actionFixed.setChecked(False)
		self.actionEngineering.setChecked(False)
		self.refresh_display()

		return
#-------------------------------------------------------------------------------------------------------------------
	def set_engineering(self):
	# 1 == general, 3 == sci, 2 == fixed, 4 == eng
		global results_format_flag
		results_format_flag = 4
		self.actionScientific.setChecked(False)
		self.actionGeneral.setChecked(False)
		self.actionFixed.setChecked(False)
		self.refresh_display()

		return

#=======================================================================================================================
#   HELP DROPDOWN MENU FUNCTIONS
#=======================================================================================================================
	def display_about(self):
		msgbox = Popup()
		msgbox.QWebView.setHtml( about()  )
		msgbox.show()
		msgbox.app.exec_()

	def display_manual(self):
		msgbox = Popup()
		msgbox.QWebView.setHtml( manual()  )
		msgbox.show()
		msgbox.app.exec_()

	def save_stack(self):

		if sys.version_info >= (3,0,0):
			f = open('stack.csv', 'w', newline='')
		else:
			f = open('stack.csv', 'wb')
		writer = csv.writer(f)
		writer.writerow(config.stack)

	def load_stack(self):
		print('herer')
		with open('stack.csv', 'rt') as f:
			reader = csv.reader(f)
			for row in reader:
				saved = row
			for i in saved:
				try:
					config.stack.append(int(i))
				except TypeError:
					try:
						config.stack.append(float(i))
					except TypeError:
						try:
							config.stack.append((complex(i)))
						except:
							config.stack.append(i)
		

if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	'''MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)'''
	MainWindow = Window()
	MainWindow.show()
	MainWindow.raise_()
	sys.exit(app.exec_())

