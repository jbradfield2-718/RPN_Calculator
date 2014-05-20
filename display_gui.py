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

from PyQt4 import QtCore, QtGui
from decimal import Decimal
import decimal, config

def display(stack, format_flag, fixed_digits_flag):
	'''print(config.stack)
	print(format_flag)
	print(fixed_digits_flag)
	print('\n')'''
# 1 == general, 3 == sci, 2 == fixed, 4 == eng format flag info

	head = '''
<!DOCTYPE html>
<head>
<style type="text/css">

body {
    font-family: sans-serif;
    font-size: medium;
}
.container {
    width: 100%;
}
.left {
    display: block;
    float:left;
	width: 100%;
}
.right {
	display: block;
	float: right;
	word-wrap: break-word;
	width: 100%;
}
</style>
</head>
<body>'''

	tail = '</body>'
	i = len(stack)
		
	for num in stack:
	#------GENERAL OUTPUT-------------------------------------------------------------------------------------------
		if format_flag == 1:
			output = str(num)
	#------FIXED OUTPUT---------------------------------------------------------------------------------------------		
		if format_flag == 2:
			fixed_string = '{:0.' + str(fixed_digits_flag) + 'f}'
			try:
				output = str(fixed_string.format(num))
			except Exception as e:
				output = str(num)
	#------SCIENTIFIC OUTPUT----------------------------------------------------------------------------------------
		if format_flag == 3:
			fixed_string = '{:0.' + str(fixed_digits_flag) + 'e}'
			try:
				output = str(fixed_string.format(num))
			except Exception as e:
				output = str(num)
	#------ENG. OUTPUT---------------------------------------------------------------------------------------------
		if format_flag == 4:
			try:
				output = str(decimal.Decimal(num).normalize().to_eng_string())
			except Exception as e:
				output = str(num)
					
		if i % 2 == 0:
			line = 	'<div class = "container"; style = "background-color:#a0c4de";><b>' + \
						'<div class = "left"; style = "background-color:#a0c4de"; dir = "ltr">' + str(i) + \
                        ':</div></b>' +	'<div class = "right"; style = "background-color:#a0c4de"; dir = "rtl">' + \
                        output +'</div></div>'
		else:
			line = 	'<div class = "container"><b>' + str(i) +':</b>' + \
					'<div class = "right"; dir  = "rtl">' + output +'</div></div>'

		head += line
		i -= 1	
	
	#print(head + tail)
	return head + tail

#=====================================================================================================
# Displays the Program startup screen
#=====================================================================================================
def display_start(self, stack, format_flag, fixed_digits_flag = 3):
	
	a = display(stack, format_flag, fixed_digits_flag)
	self.QWebView.setHtml(a)
	return
#-------------------------------------------------------------------------------------------------------------------
	
def functions():
	functions = 	[ ['+','addition'], ['-', 'subtraction'], ['*', 'multiplication'], ['/', 'division'] ,
			['!', 'factorial'], ['sqrt', 'square root'], ['**', 'exponent'], ['%','modulus'],
			['exp','exponential function'], ['rt', 'root: base, 1/exponent'],
			['asinh','anti-hyperbolic sine'], ['asin','arcsine'], ['sinh','hyperbolic sine'],
			['sin','sine'], ['acosh','anti-hyperbolic cosine'], ['acos','arccosine'],
			['cosh','hyperbolic cosine'], ['cos','cosine'], ['atanh', 'anti-hyperbolic tangent'],
			['atan','arctangent'], ['tanh', 'hyperbolic tangent'], ['tan','tangent'], 
			['log', 'base-10 logarithm'], ['ln', 'natural logarithm'], ['rect', 'convert polar to rect'],
			['polar','convert rect to polar'] ]
		
	head = '''

<!DOCTYPE html>
<head>
<style type="text/css">

body {
    font-family: sans-serif;
    font-size: medium;
}
.container {
    width: 100%;
}
.left {
    display: block;
    float:left;
	width: 100%;
}
.right {
	display: block;
	float: right;
	width: 100%;
}
</style>
</head>
<body>'''

	tail = '</body>'

	i = 0
	for arg in functions:

		if i % 2 == 0:
			line = 	'<div class = "container"; style = "background-color:#a0c4de";><b>'  \
					'<div class = "left"; style = "background-color:#a0c4de"; dir = "ltr">' + arg[0] + \
                    ':</b></div><br>' + '<div class = "right"; style = "background-color:#a0c4de"; dir = "rtl">' + \
                    arg[1] +'</div></div><br>'
						
		else:
			line = 	'<div class = "container"><b>' + arg[0] +':</b><br>' + \
					'<div class = "right"; dir  = "rtl">' + arg[1] +'</div><br></div>'
							
		i += 1
		head += line
	
	return head + tail
	
def show_constants(constants):
	head = '''
<!DOCTYPE html>
<head>
<style type="text/css">

body {
    font-family: sans-serif;
    font-size: medium;
}
.container {
    bottom:0;
    width: 100%;
}
.left {
    display: block;
    float:left;
}
.right {
	display: block;
	float: right;
	width: 100%;
}
</style>
</head>
<body>'''

	tail = '</body>'

	i = 0
	for const in constants:
		
		if i % 2 == 0:
			line = 	'<div class = "container"; style = "background-color:#a0c4de";><b>'  \
					'<div class = "left"; dir = "ltr">' + const[0] +':</div></b><br>'   \
					'<div class = "right"; style = "background-color:#a0c4de"; dir = "rtl">' + \
                    str(const[1]) +'</div><br><b>' + \
                    '<div class = "right"; style = "background-color:#a0c4de"; dir = "rtl">' + \
                    const[2] +'</div></b></div><br>'
		else:
			line = 	'<div class = "container"><b>' + const[0] +':</b><br>' \
					'<div class = "right"; dir  = "rtl">' + str(const[1]) +'</div><br>' \
					'<b><div class = "right"; dir  = "rtl">' + const[2] +'</div></b></div><br>'
		
		i += 1
		head += line
	
	return head + tail
	
	
def manual():
	string = '''
<!DOCTYPE html>
<head>
<style type="text/css">

body {
    font-family: sans-serif;
    font-size: medium;
}
.container {
    bottom:0;
    width: 100%;
}
.left {
    display: block;
    float:left;
}
.right {
	display: block;
	float: right;
	width: 100%;
}
</style>
</head>
<body>
<h1> TrueRPN</h1>
The following program performs as a fully functional rpn and algebraic mode calculator.
<h2>RPN Mode</h2>
<div>The program allows reverse polish notation entry of values.  Note that entry of number
along with the operator is supported.  All entries must be made using the enter key.
For instance, if you'd like to enter the number 8 to the stack, hit the 8 key, and then
Enter on the keyboard.  If you'd like to multiply 8 (on the stack) with the number 2,
type 2* on the keyboard, then press enter.</div>
<div>In a similar fashion it's possible to enter more complex arguments in the same way.
Try the following:  type 2sqrt then enter, to get the square root of two!</div>
<h2>Algebraic Entry Mode</h2>
<div>Not yet supported.  Check back during next release!</div>
<h2>Functions</h2>
<div>The standard scientific calculator functions are supported. Note that some of the
 functions may not work with complex number values.</div>
<h2>Constants</h2>
<div>A variety of engineering constants are available.  Further, the user can enter
their own defined constants by tying a string value followed by the equal sign:<br>
var_x = 25<br>
All the currently defined constants can be displayed by selecting the 'Constants'
option from the Display dropdown menu.</div>
<h2>Complex Math</h2>
The program supports complex math calculations.  
</body>'''
	return string
	
def about():
	string = '''
<!DOCTYPE html>
<head>
<style type="text/css">

body {
    font-family: sans-serif;
    font-size: small;
}
.container {
    bottom:0;
    width: 100%;
}
.left {
    display: block;
    float:left;
}
.right {
	display: block;
	float: right;
	width: 100%;
}
</style>
</head>
<body>
<b>TrueRPN was developed by Justin Bradfield.</b><br>

	<div>Copyright 2014, Justin Bradfield<br><br>

    <div>TrueRPN is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.</div><br>

    <div>TrueRPN is distributed in the hope that it will be useful,
    but <b>WITHOUT ANY WARRANTY;</b> without even the implied warranty of
    <b>MERCHANTABILITY</b> or <b>FITNESS FOR A PARTICULAR PURPOSE.</b>  See the
    GNU General Public License for more details.</div><br>

    <div>You should have received a copy of the GNU General Public License
    along with TrueRPN.  If not, see <a href="http://www.gnu.org/licenses/">http://www.gnu.org/licenses/.</a><div>
</body>
'''
	return string
	