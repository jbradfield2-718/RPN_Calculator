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
import math
import cmath
import config

def pow(n2, n1):
	return n2 ** n1

def root(num, pow):
	return num ** (1/pow)
	
def exp(pow):
	return exp(pow)
	
def rect(mag, angle):
	return cmath.rect(mag, angle)
	
def polar(num):
	return cmath.polar(num)