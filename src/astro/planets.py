from .angles import *

import math
import time

PATH = "/usr/local/VSOP_Formated"

data_files = {'Mercury'  : 		'{0}/VSOP87B_merc.dat'.format(PATH),
					'Venus'  : 	'{0}/VSOP87B_ven.dat'.format(PATH), 
					'Earth'  : 	'{0}/VSOP87B_earth.dat'.format(PATH), 
					'Mars'   : 	'{0}/VSOP87B_mars.dat'.format(PATH), 
					'Jupiter': 	'{0}/VSOP87B_jupiter.dat'.format(PATH),
					'Saturn' : 	'{0}/VSOP87B_saturn.dat'.format(PATH),
					'Neptune':	'{0}/VSOP87B_neptune.dat'.format(PATH),
					}
					
class vector:
	def __init__(self, x,y,z):
		self.x=x
		self.y=y
		self.z=z
		
		self.mag = math.sqrt(x*x+y*y+z*z)
		self.unit = (x/self.mag, y/self.mag, z/self.mag)
	
	def __sub__(self, other):
		return vector(self.x-other.x, self.y-other.y, self.z-other.z)
	
	
	def __str__(self):
		return ("%s %s %s" %(self.x, self.y, self.z))

class Planet:
	def __init__(self, name, jd):
		
		self.name=name
		data_file = data_files[name]
		self.pos = self.calcVSOP87A(data_file, jd)
		
	def calcVSOP87A(self, data_file, T):
		t=(T-2451545.0)/365250
		
		if type(data_file) == str:
			data_file = open(data_file, 'r')
		
		series_num = 0
		
		var_num = 0
		SUM = 0
		first_line=True
		X,Y,Z = 0,0,0
		
		
		for line in data_file:
			
			
			arr = line.split()
			if len(arr) == 0: pass
			else:
				
				if arr[0] == "VSOP87" and not first_line:
					
					Vars[coords[var_num]]+=SUM*t**series_num
					
					series_num = int(arr[7][-1])
					var_num = int(arr[5])-1
					
					
					
					SUM = 0
					
				elif not first_line:
					A = float(arr[0])
					B = float(arr[1])
					C = float(arr[2])
					
					SUM+= float(A*math.cos(B + C*t))
					
				if first_line:	
					coords = arr[6][1:4]
					Vars = {coords[0]:0 ,coords[1]:0, coords[2]:0}
					
			first_line = False
		if coords == 'LBR':#Convert angles to positive radians less than 2*
			if abs(Vars['L']) >  2*math.pi:
				Vars['L'] = ((Vars['L']/(2*math.pi))-int(Vars['L']/(2*math.pi)))*2*math.pi
			if Vars['L'] < 0:
				Vars['L'] = 2*math.pi + Vars['L']
			
			if abs(Vars['B']) >  2*math.pi:
				Vars['B'] = ((Vars['B']/(2*math.pi))-int(Vars['B']/(2*math.pi)))*2*math.pi
			if Vars['B'] < 0:
				Vars['B'] = 2*math.pi + Vars['B']	
			
			Vars['X'] = Vars['R']*math.cos(Vars['B'])*math.cos(Vars['L'])
			Vars['Y'] = Vars['R']*math.cos(Vars['B'])*math.sin(Vars['L'])
			Vars['Z'] = Vars['R']*math.sin(Vars['B'])
			
			
		return vector(Vars['X'], Vars['Y'], Vars['Z'])
	
	def __str__(self):
		return self.name

class Mercury(Planet):
	def __init__(self, jd):
		Planet.__init__(self, 'Mercury', jd)

class Venus(Planet):
	def __init__(self, jd):
		Planet.__init__(self, 'Venus', jd)
	
class Earth(Planet):
	def __init__(self, jd):
		Planet.__init__(self, 'Earth', jd)

class Mars(Planet):
	def __init__(self, jd):
		Planet.__init__(self, 'Mars', jd)
		
class Jupiter(Planet):
	def __init__(self, jd):
		Planet.__init__(self, 'Jupiter', jd)
		
class Saturn(Planet):
	def __init__(self, jd):
		Planet.__init__(self, 'Saturn', jd)
		
class Neptune(Planet):
	def __init__(self, jd):
		Planet.__init__(self, 'Neptune', jd)

def doAll(jd):
	return [Mercury(jd), Venus(jd), Mars(jd), Jupiter(jd), Saturn(jd), Neptune(jd)]
	
	
				
		
