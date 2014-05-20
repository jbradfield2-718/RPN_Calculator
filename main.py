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
import math, cmath, config
import functions
from decimal import *
from functions import root, pow, exp, rect, polar
import display_gui

global constants, constants_list, history
config.stack = []
history = []
constants_list = [ 'e', 'c', 'pi', 'me', 'phi', 'G', 'g', 'h', 'q']
constants = [ ('e', 2.71828182845904523536, "Euler's number"), ('c', 299792458, "Speed of Light in vacuum m&#47s&#41"),
					('pi', 3.14159265358979323846, 'Pi'), ('me', 9.10938291e-31, 'Electron mass kg'),
					('phi', 1.6180339887498948, 'Golden ratio'),
                    ('G', 6.67428e-11, 'Gravitational constant N*(m/kg)^2'),
					('g', 9.80665, 'Acceleration due to gravity m/s'), ('h', 6.62606957e-34, "Planck's constant J*s"),
					('q', 1.60217657e-19, 'Elementary charge C') ]

def rpn_calc(input, angle_mode = 0):
	global stack
	single_arg_funcs = ['exp','sqrt','sin','asin','cos','acos','tan','atan', 'sinh','asinh','cosh','acosh','tanh',
                        'atanh','!', 'polar']
	
	num, arg, option = parse(input)
	#print(num, arg, option)
	#print('\n')
	
	if arg == None and (num != None or num != 'Error'):
		config.stack.append(num)
		history.append('Entered number: ' + str(num) )
		return config.stack

	

# Simple arithmatic-----------------------------------------------------------------------	
	if option == None and num != None:
		if arg not in single_arg_funcs:
			last = config.stack.pop()
	
		if arg == '+':
			try:
				result = Decimal(last) + Decimal(num)
				hist = str(last) + '+' + str(num) + '=' + str(result)
			except TypeError:
				result = last + num
				hist = str(last) + '+' + str(num) + '=' + str(result)
				
		if arg == '-':
			try:
				result = Decimal(last) - Decimal(num)
				hist = str(last) + '-' + str(num) + '=' + str(result)
			except TypeError:
				result = last - num
				hist = str(last) + '-' + str(num) + '=' + str(result)
			
		if arg == '*':
			try:
				result = Decimal(last) * Decimal(num)
				hist = str(last) + '*' + str(num) + '=' + str(result)
			except TypeError:
				result = last * num
				hist = str(last) + '*' + str(num) + '=' + str(result)
				
		if arg == '/':
			try:
				result = Decimal(last) / Decimal(num)
				hist = str(last) + '/' + str(num) + '=' + str(result)
			except TypeError:
				result = last / num
				hist = str(last) + '/' + str(num) + '=' + str(result)
				
		if arg == '**':
			try:
				result = pow(Decimal(last), Decimal(num) )
				hist = str(last) + '**' + str(num) + '=' + str(result)
			except TypeError:
				result = last ** num
				hist = str(last) + '**' + str(num) + '=' + str(result)
				
		if arg == 'rt':
			try:
				result = root(Decimal(last), Decimal(num) )
				hist = str(last) + 'raised to 1 over ' + str(num) + '=' + str(result)
			except TypeError:
				result = root(last + num)
				hist = str(last) + 'raised to 1 over ' + str(num) + '=' + str(result)
				
		if arg == '%':
			try:
				result = Decimal(last) % Decimal(num)
				hist = str(last) + '%' + str(num) + '=' + str(result)
			except TypeError:
				result = last % num
				hist = str(last) + '%' + str(num) + '=' + str(result)
		
		if arg == '!':
			try:
				result = Decimal(math.factorial(num))
				hist = str(num) + '!' + '=' + str(result)
			except TypeError:
				result = math.factorial(num)
				hist = str(num) + '!' + '=' + str(result)
				
		if arg == 'exp':
			try:
				result = math.exp(Decimal(num))
				hist = str(num) + 'exp' + '=' + str(result)
			except ValueError:
				result = cmath.exp(Decimal(num))
				hist = str(num) + 'exp' + '=' + str(result)
			except TypeError:
				result = cmath.exp(num)
				hist = str(num) + 'exp' + '=' + str(result)
				
		if arg == 'sqrt':
			try:
				result = math.sqrt(Decimal(num))
				hist = str(num) + 'sqrt' + '=' + str(result)
			except ValueError:
				result = cmath.sqrt(Decimal(num))
				hist = str(num) + 'sqrt' + '=' + str(result)
			except TypeError:
				result = cmath.sqrt(num)
				hist = str(num) + 'sqrt' + '=' + str(result)
				
		if arg == 'log':
			try:
				result = math.log10(Decimal(num))
				hist = str(num) + 'log10' + '=' + str(result)
			except ValueError:
				result = cmath.log10(Decimal(num))
				hist = str(num) + 'log10' + '=' + str(result)
			except TypeError:
				result = cmath.log10(num)
				hist = str(num) + 'log10' + '=' + str(result)
		#=================================
		if arg == 'ln':
			try:
				result = math.log(Decimal(num))
				hist = str(num) + 'ln' + '=' + str(result)
			except ValueError:
				result = cmath.log(Decimal(num))
				hist = str(num) + 'ln' + '=' + str(result)
			except TypeError:
				result = cmath.log(num)
				hist = str(num) + 'ln' + '=' + str(result)
		#--------TRIG--------------------------------
		if arg == 'sin':
			if angle_mode == 1:
				try:
					result = math.sin(Decimal(num))
					hist = 'sin' + str(num) + '=' + str(result)
				except TypeError:
					result = cmath.sin(num)
					hist = 'sin' + str(num) + '=' + str(result)
			elif angle_mode == 0:
				try:
					result = math.sin(math.radians(Decimal(num)))
					hist = 'sin' + str(num) + '=' + str(result)
				except TypeError:
					result = cmath.sin(num)
					hist = 'sin' + str(num) + '=' + str(result)
		
		if arg == 'cos':
			if angle_mode == 1:
				try:
					result = math.cos(Decimal(num))
					hist = 'cos' + str(num) + '=' + str(result)
				except TypeError:
					result = cmath.cos(num)
					hist = 'cos' + str(num) + '=' + str(result)
			elif angle_mode == 0:
				try:
					result = math.cos(math.radians(Decimal(num)))
					hist = 'cos' + str(num) + '=' + str(result)
				except TypeError:
					result = cmath.cos(num)
					hist = 'cos' + str(num) + '=' + str(result)

		if arg == 'tan':
			if angle_mode == 1:
				try:
					result = math.tan(Decimal(num))
					hist = 'tan' + str(num) + '=' + str(result)
				except TypeError:
					result = cmath.tan(num)
					hist = 'tan' + str(num) + '=' + str(result)
			elif angle_mode == 0:
				try:
					result = math.tan(math.radians(Decimal(num)))
					hist = 'tan' + str(num) + '=' + str(result)
				except TypeError:
					result = cmath.tan(num)
					hist = 'tan' + str(num) + '=' + str(result)
			
		if arg == 'asin':
			if angle_mode == 1:
				try:
					result = math.asin(Decimal(num))
					hist = 'asin' + str(num) + '=' + str(result)
				except TypeError:
					result = cmath.asin(num)
					hist = 'asin' + str(num) + '=' + str(result)
			elif angle_mode == 0:
				try:
					result = math.asin(math.radians(Decimal(num)))
					hist = 'asin' + str(num) + '=' + str(result)
				except TypeError:
					result = cmath.asin(num)
					hist = 'asin' + str(num) + '=' + str(result)
		
		if arg == 'acos':
			if angle_mode == 1:
				try:
					result = math.acos(Decimal(num))
					hist = 'acos' + str(num) + '=' + str(result)
				except TypeError:
					result = cmath.acos(num)
					hist = 'acos' + str(num) + '=' + str(result)
			elif angle_mode == 0:
				try:
					result = math.acos(math.radians(Decimal(num)))
					hist = 'acos' + str(num) + '=' + str(result)
				except TypeError:
					result = cmath.acos(num)
					hist = 'acos' + str(num) + '=' + str(result)

		if arg == 'atan':
			if angle_mode == 1:
				try:
					result = math.atan(Decimal(num))
					hist = 'atan' + str(num) + '=' + str(result)
				except TypeError:
					result = cmath.atan(num)
					hist = 'atan' + str(num) + '=' + str(result)
			elif angle_mode == 0:
				try:
					result = math.atan(math.radians(Decimal(num)))
					hist = 'atan' + str(num) + '=' + str(result)
				except TypeError:
					result = cmath.atan(num)
					hist = 'atan' + str(num) + '=' + str(result)
			
		if arg == 'sinh':
			try:
				result = math.sinh(Decimal(num))
				hist = 'sinh' + str(num) + '=' + str(result)
			except TypeError:
				result = cmath.sinh(num)
				hist = 'sinh' + str(num) + '=' + str(result)
		
		if arg == 'cosh':
			try:
				result = math.cosh(Decimal(num))
				hist = 'cosh' + str(num) + '=' + str(result)
			except TypeError:
				result = cmath.cosh(num)
				hist = 'cosh' + str(num) + '=' + str(result)

		if arg == 'tanh':
			try:
				result = math.tanh(Decimal(num))
				hist = 'tanh' + str(num) + '=' + str(result)
			except TypeError:
				result = cmath.tanh(num)
				hist = 'tanh' + str(num) + '=' + str(result)
			
		if arg == 'asinh':
			try:
				result = math.asinh(Decimal(num))
				hist = 'asinh' + str(num) + '=' + str(result)
			except TypeError:
				result = cmath.asinh(num)
				hist = 'asinh' + str(num) + '=' + str(result)
		
		if arg == 'acosh':
			try:
				result = math.acosh(Decimal(num))
				hist = 'acosh' + str(num) + '=' + str(result)
			except TypeError:
				result = cmath.acosh(num)
				hist = 'acosh' + str(num) + '=' + str(result)

		if arg == 'atanh':
			try:
				result = math.atanh(Decimal(num))
				hist = 'atanh' + str(num) + '=' + str(result)
			except TypeError:
				result = cmath.atanh(num)
				hist = 'atanh' + str(num) + '=' + str(result)

		if arg == 'rect': #continue here....
			try:
				result = rect(last, num)
				hist = 'Convert ' + str(last) + ',' + str(num) + ' to rectangular coords.'

			except TypeError:
				result = 'Error'
				hist = 'Error in attempted conversion to rectangular coords.  No result.'

		if arg == 'polar':
			try:
				result = polar(num)
				hist = 'Convert ' + str(num) + ' to polar coords.'
			except TypeError:
				result = 'Error'
				hist = 'Error in attempted conversion to polar coords.  No result.'
		
			
		config.stack.append(result)
		history.append(hist)
		return config.stack
#=======================================================================================================================
#----Only argument passed-----------------------------------------------------------------------------------------------
#=======================================================================================================================
	elif option == None and num == None:
		last = config.stack.pop()
		if arg not in single_arg_funcs:
			try:
				n_minus1 = config.stack.pop()
			except IndexError:
				try:
					config.stack.append(Decimal(last))
				except TypeError:
					config.stack.append(last)
			except TypeError:
				config.stack.append(last)
			except Exception as e:
				return 'Error'

		if arg == '+':
			try:
				result = Decimal(n_minus1) + Decimal(last)
				hist = str(n_minus1) + '+' + str(last) + '=' + str(result)
			except TypeError:
				result = n_minus1 + last
				hist = str(n_minus1) + '+' + str(last) + '=' + str(result)
				
		if arg == '-':
			try:
				result = Decimal(n_minus1) -  Decimal(last)
				hist = str(n_minus1) + '-' + str(last) + '=' + str(result)
			except TypeError:
				result = n_minus1 - last
				hist = str(n_minus1) + '-' + str(last) + '=' + str(result)
				
		if arg == '*':
			try:
				result = Decimal(n_minus1) * Decimal(last)
				hist = str(n_minus1) + '*' + str(last) + '=' + str(result)
			except TypeError:
				result = n_minus1 * last
				hist = str(n_minus1) + '*' + str(last) + '=' + str(result)
				
		if arg == '/':
			try:
				result = Decimal(n_minus1) / Decimal(last)
				hist = str(n_minus1) + '/' + str(last) + '=' + str(result)
			except TypeError:
				result = n_minus1 / last
				hist = str(n_minus1) + '/' + str(last) + '=' + str(result)
				
		if arg == '!':
			try:
				result = Decimal(math.factorial(last))
				hist = str(last) + '!' '=' + str(result)
			except TypeError:
				result = math.factorial(last)
				hist = str(last) + '!' '=' + str(result)
			except OverflowError:
				config.stack.append(last)
				hist = str('Factorial overflow error, no result.')
				return 'Error'
				
		if arg == '**':
			try:
				result = pow(Decimal(last), Decimal(last))
				hist = str(n_minus1) + '**' + str(last) + '=' + str(result)
			except TypeError:
				result = last ** last
				hist = str(n_minus1) + '**' + str(last) + '=' + str(result)
				
		if arg == 'log':
			try:
				result = math.log10(Decimal(last))
				hist = str(last) +'log10' + '=' + str(result)
			except ValueError:
				result = cmath.log10(Decimal(last))
				hist = str(last) +'log10' + '=' + str(result)
			except TypeError:
				result = cmath.log10(last)
				hist = str(last) +'log10' + '=' + str(result)
		
		if arg == 'ln':
			try:
				result = math.log(Decimal(last))
				hist = str(last) +'ln' + '=' + str(result)
			except ValueError:
				result = cmath.log(Decimal(last))
				hist = str(last) +'ln' + '=' + str(result)
			except TypeError:
				result = cmath.log(last)
				hist = str(last) +'ln' + '=' + str(result)
			
		if arg == 'rt':
			try:
				result = root(Decimal(last), Decimal(n_minus1))
				hist = str(n_minus1) + 'root' + str(last) + '=' + str(result)
			except TypeError:
				result = root(last), (n_minus1)
				hist = str(n_minus1) + 'root' + str(last) + '=' + str(result)
				
		if arg == 'exp':
			try:
				result = math.exp(Decimal(last))
				hist = str(last) +'exp' + '=' + str(result)
			except TypeError:
				result = cmath.exp(last)
				hist = str(last) +'exp' + '=' + str(result)
			
				
		if arg == 'sqrt':
			try:
				result = math.sqrt(Decimal(last))
				hist = 'Square root of ' + str(last) + '=' + str(result)
			except ValueError:
				result = cmath.sqrt(Decimal(last))
				hist = 'Square root of ' + str(last) + '=' + str(result)
			except TypeError:
				result = cmath.sqrt(last)
				hist = 'Square root of ' + str(last) + '=' + str(result)
#----------Trig----------------------------------------				
		#--------TRIG--------------------------------
		if arg == 'sin':
			if angle_mode == 1:
				try:
					result = math.sin(Decimal(last))
					hist = 'sin' + str(last) + '=' + str(result)
				except TypeError:
					result = cmath.sin(last)
					hist = 'sin' + str(last) + '=' + str(result)
			elif angle_mode == 0:
				try:
					result = math.sin(math.radians(Decimal(last)))
					hist = 'sin' + str(last) + '=' + str(result)
				except TypeError:
					result = cmath.sin(last)
					hist = 'sin' + str(last) + '=' + str(result)
					
		if arg == 'cos':
			if angle_mode == 1:
				try:
					result = math.cos(Decimal(last))
					hist = 'cos' + str(last) + '=' + str(result)
				except TypeError:
					result = cmath.cos(last)
					hist = 'cos' + str(last) + '=' + str(result)
			elif angle_mode == 0:
				try:
					result = math.cos(math.radians(Decimal(last)))
					hist = 'cos' + str(last) + '=' + str(result)
				except TypeError:
					result = cmath.cos(last)
					hist = 'cos' + str(last) + '=' + str(result)
					
		if arg == 'tan':
			if angle_mode == 1:
				try:
					result = math.tan(Decimal(last))
					hist = 'tan' + str(last) + '=' + str(result)
				except TypeError:
					result = cmath.tan(last)
					hist = 'tan' + str(last) + '=' + str(result)
			elif angle_mode == 0:
				try:
					result = math.tan(math.radians(Decimal(last)))
					hist = 'tan' + str(last) + '=' + str(result)
				except TypeError:
					result = cmath.tan(last)
					hist = 'tan' + str(last) + '=' + str(result)
					
		if arg == 'asin':
			if angle_mode == 1:
				try:
					result = math.asin(Decimal(last))
					hist = 'asin' + str(last) + '=' + str(result)
				except TypeError:
					result = cmath.asin(last)
					hist = 'asin' + str(last) + '=' + str(result)
			elif angle_mode == 0:
				try:
					result = math.asin(math.radians(Decimal(last)))
					hist = 'asin' + str(last) + '=' + str(result)
				except TypeError:
					result = cmath.asin(last)
					hist = 'asin' + str(last) + '=' + str(result)
					
		if arg == 'acos':
			if angle_mode == 1:
				try:
					result = math.acos(Decimal(last))
					hist = 'acos' + str(last) + '=' + str(result)
				except TypeError:
					result = cmath.acos(last)
					hist = 'acos' + str(last) + '=' + str(result)
			elif angle_mode == 0:
				try:
					result = math.acos(math.radians(Decimal(last)))
					hist = 'acos' + str(last) + '=' + str(result)
				except TypeError:
					result = cmath.acos(last)
					hist = 'acos' + str(last) + '=' + str(result)

		if arg == 'atan':
			if angle_mode == 1:
				try:
					result = math.atan(Decimal(last))
					hist = 'atan' + str(last) + '=' + str(result)
				except TypeError:
					result = cmath.atan(last)
					hist = 'atan' + str(last) + '=' + str(result)
			elif angle_mode == 0:
				try:
					result = math.atan(math.radians(Decimal(last)))
					hist = 'atan' + str(last) + '=' + str(result)
				except TypeError:
					result = cmath.atan(last)
					hist = 'atan' + str(last) + '=' + str(result)
			
		if arg == 'sinh':
			try:
				result = math.sinh(Decimal(last))
				hist = 'sinh' + str(last) + '=' + str(result)
			except TypeError:
				result = math.sinh(last)
				hist = 'sinh' + str(last) + '=' + str(result)
		
		if arg == 'cosh':
			try:
				result = math.cosh(Decimal(last))
				hist = 'cosh' + str(last) + '=' + str(result)
			except TypeError:
				result = math.cosh(last)
				hist = 'cosh' + str(last) + '=' + str(result)

		if arg == 'tanh':
			try:
				result = math.tanh(Decimal(last))
				hist = 'tanh' + str(last) + '=' + str(result)
			except TypeError:
				result = math.tanh(last)
				hist = 'tanh' + str(last) + '=' + str(result)
			
		if arg == 'asinh':
			try:
				result = math.asinh(Decimal(last))
				hist = 'asinh' + str(last) + '=' + str(result)
			except TypeError:
				result = math.asinh(last)
				hist = 'asinh' + str(last) + '=' + str(result)
		
		if arg == 'acosh':
			try:
				result = math.acosh(Decimal(last))
				hist = 'acosh' + str(last) + '=' + str(result)
			except TypeError:
				result = math.acosh(last)
				hist = 'acosh' + str(last) + '=' + str(result)

		if arg == 'atanh':
			try:
				result = math.atanh(Decimal(last))
				hist = 'atanh' + str(last) + '=' + str(result)
			except TypeError:
				result = math.atanh(last)
				hist = 'atanh' + str(last) + '=' + str(result)
				
		if arg == 'rect': #continue here....
			try:
				result = rect(n_minus1, last)
				hist = 'Convert ' + str(n_minus1) + ',' + str(last) + ' to rectangular coords.'

			except TypeError:
				result = 'Error'
				hist = 'Error in attempted conversion to rectangular coords.  No result.'

		if arg == 'polar':
			try:
				result = polar(last)
				hist = 'Convert complex value ' + str(last) + ' to rectangular coords.'
			except TypeError:
				result = 'Error'
				hist = 'Error in attempted conversion to polar coords.  No result.'

		config.stack.append(result)
		history.append(hist)
		return config.stack
# 
		
#=================================================================	
''' Parse function accepts the string and returns 3 variables--
	User entered number, whether float or int
	Argument/function to apply to last entry in config.stack
	optional additional arg associated with Argument 2 '''
#=================================================================
def parse(input):
	args = ['+','**','*','/','!','sqrt','-','%','exp','rt',
			'asinh','asin','sinh','sin','acosh','acos','cosh','cos',
			'atanh','atan','tanh','tan','log','ln', 'rect', 'polar']
			
	global constants, constants_list
	
	# Adds constant to lists
	if '=' in input:
		const = add_constant(input)
		return const, None, None
	
	input = input.split(' ')
		
	if len(input) == 1:
		inputg = input[0]
#------Returns single char arguments only----------------------------------------------------		
		if len(inputg) == 1 and inputg in args:
			return None, inputg, None
#-------Try to return number only--------------------------------------------------------------
		try:
			return int(inputg), None, None
		except ValueError:
			try:
				return Decimal(inputg), None, None
			except Exception as e:
				if inputg in constants_list:
					return find_constant(inputg), None, None
				pass						
#-------try to return number and arg----------------------------------------------------------		
		try:
			return int(inputg[:-1]), inputg[-1], None

		except ValueError:
			try:
				return Decimal(inputg[:-1]), inputg[-1], None
			except Exception as e:
					pass
#-------try to return number and arg if concatenated or multi-char args-----------------------				
		for arg in args:
			if arg in inputg:

				if inputg.find(arg) == 0:
					index = inputg.find(arg) + len(arg)
					num = inputg[index:]
					argument = inputg[:index]
					break
				else:
					index = inputg.find(arg)
					num = inputg[:index]
					argument = inputg[index:]
					break

		#print(index, num, argument)
				
		if num == '':
			return None, argument, None		# User entered an argument that has >1 char
		else:
			try:
				return int(num), argument, None		# Try to return both number and arg
			except ValueError:
				try:
					return float(num), argument, None
				except Exception as e:
					return 'Error', 'Error', 'Error'
					
#--------Parse to see if we have argument with multiple char or arg+num concatenated
#--------e.g. user enters rt3 to calc the square root of 3-------------------------------------------------				

		
	# User entered a number and argument	separated by a space
	elif len(input) == 2:
		number = Decimal(input[0])
		arg = input[1]
		opt = None
		return number, arg, opt
	
	# User entered a number, argument and optional argument all separated by space
	elif len(input) == 3:
		number = Decimal(input[0])
		arg = input[1]
		opt = input[2]
		return number, arg, opt
		
	else:
		
		return 'Error', 'Error', 'Error'
	
def clear_stack():
	config.stack = []
	print(config.stack)
	return config.stack
	
def find_constant(inputg):
	#[ 'e', 'c', 'pi', 'me', 'phi', 'G', 'g', 'h', 'q']
	for const in constants:
		if inputg == const[0]:
			return Decimal(const[1])		
	return
		
def set_precision(num_decimal):
	pass
		
def add_constant(inputg):
	global constants_list, constants
		
	const = inputg.replace(' ', '')
	const = const.split('=')
	try:
		var = const[0]
		num = int(const[1])
	except TypeError:
		try:
			var = const[0]
			num = float(const[1])
		except Exception as e:
			return 'Error'
					
	constants_list.append(var)
	tuple = (var, num, '')
	constants.append(tuple)

	return num
		
def return_constants():
	global constants
	return constants