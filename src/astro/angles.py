import math
import exceptions

__all__ = [
				'Angle',
				'Dec_angle',
				'Hour_angle',
				'RA_angle',
				'Deg10',
				'delimError',
				'parseError'
				]



class Angle():

	"""Class to handle different types of astronomical angles
	args:	rawval, type, delim
	Desc:	Takes rawval and converts it to rotations leaving 
	the direction and number of rotations in tact
	From there it converts it to other units less than 
	one positive rotation. So if direction and number
	of rotations is important use unit Angle.unit .

	'Type' gives the units the angle rawval is given in. Delim is the seperator 
	for things like hours:minutes:seconds if the angle is an hour angle."""
			
	def __init__(self, rawval, Type='radians', delim=':'):
		"""Angle constructor class"""
		raw = rawval
		self.Name = 'Angle'
		if type(rawval) in [str, unicode ]:#Parse angle into list values seperated by delim
		
			if delim not in rawval: raise delimError("No delimiter found in rawval '%s'. Delimiter is '%s'." %(rawval, delim))
			else: 
				vals = rawval.split(delim)
				try: vals.remove('')
				except(ValueError):pass
				
				#rawval = [int(float(i)) for i in vals]
				try:
					rawval = [int( float( vals[0] ) ), int( float( vals[1] ) ), float( vals[2] ) ]
				except( IndexError ):
					raise parseError("Error parsing string %s into angle" %( rawval ))
				
		elif type(rawval) == list:#Parse list
			if rawval[1] > 60 or rawval[2] > 60:
				if Type=='hours': raise Exception("minutes or seconds in rawval exceeds 60.")
				else: Exception("arcminutes or arcseconds in rawval exceeds 60.")
				
		try:#If rawval is an angle instance
			if rawval.ThisIsAnAngle:
				rawval = rawval.val
				Type = 'radians'
				
		except(AttributeError):
			pass
		
		
		#Convert angle to units of one rotation
		#This conserves direction and number of rotations
		#all other angle Types are less than one rotation in 
		#the positive direction. 
		if Type=='deg10':
			self.unit = rawval/360.0
		
		#0 to 360 in degrees arcminustes and arcseconds
		elif Type=='degarc':
			if rawval[0] != 0:sign = rawval[0]/abs(rawval[0])
			else: sign = 0
			self.unit = sign*(abs(rawval[0])/360.0 + rawval[1]/(360*60.0) + rawval[2]/( 360*60*60.0 ) )

			
		#hours:minutes:seconds	
		#good for  hour angle
		elif Type=='hours' or Type=='hour':
			
			if rawval[0] != 0:sign = rawval[0]/abs(rawval[0])
			else: sign = 1
			
			self.unit = sign*(abs(rawval[0])/24.0 + rawval[1]/(24*60.0) + rawval[2]/(24*60*60.0))

		#Good for declination
		#degrees[-180:180]:arcminutes:arcseconds
		elif Type=='degarc180':
			if rawval[0] != 0: 
				sign = rawval[0]/abs( rawval[0] )
			else: 
				sign = 1
			self.unit = sign*( abs( rawval[0] )/360.0 + rawval[1]/( 360*60.0 ) + rawval[2]/( 360*60*60.0 ) )

		elif Type=="dec":
			if type( raw ) in [str, unicode]:
				if '+' in raw:
					sign = 1
				elif '-' in raw:
					sign = -1
				else:
					sign = 1
                
			elif type(raw) == list:
				if abs( raw[0] ) < 1: #ambiguous sign
					sign=1#raise ( signError("sign is ambigous") )
				else:
					sign=rawval[0]/abs( rawval[0] )
			
			
			self.unit = sign*(abs(rawval[0])/360.0 + rawval[1]/(360.0*60.0) + rawval[2]/(360.0*60.0*60.0))
		        

		elif Type=='radians':
			self.unit = rawval/(2*math.pi)
		
		
		elif Type=='hourdecimal':
			self.unit = rawval/24.0
		#End conversion	

		#Now we have an angle in number of rotations and direction (self.unit)
		#Lets convert to every other type of angle
		self.onerot = self.unit%1 # less than one rotation in the positive direction
		
		#The easy stuff
		self.val = self.onerot*2*math.pi#Angle in radians
		self.deg10 = self.onerot*360.0#angle in degrees and decimals
		self.hourdecimal = self.onerot*24.0#Angle in hours and decimals
		
		
		#python list of [hours,minutes,seconds]
		self.hours = [int(self.hourdecimal), int((self.hourdecimal*60)%60), round( ( self.hourdecimal*60*60 )%60, 2 )]
		if self.hours[2] == 60:
			self.hours[2] = 0
			self.hours[1] = (self.hours[1]+1) % 60
		if self.hours[1] == 60:
			self.hours[1] = 0
			self.hours[0] = (self.hours[0]+1) % 24
			
		#Python list of [degrees,arcminutes,arcsedonds]
		self.degarc = [int(self.deg10), int((self.deg10*60)%60), round( ( self.deg10*60*60 )%60, 2 )]
		if self.degarc[2] == 60:
			self.degarc[2] = 0
			self.degarc[1] = (self.degarc[1]+1) % 60
		if self.degarc[1] == 60:
			self.degarc[1] = 0
			self.degarc[0] = (self.degarc[0]+1) % 24
		 
		#max180 => angle in in range [-180, 180]
		if self.onerot > 0.5:	self.max180 = (self.onerot-1)*360
		else:self.max180 = self.deg10
		
		
		#List with angle in [degrees, arcminutes, arcseconds] in range [-180, 180] (mostly for declination) 	
		self.degarc180 = [int(self.max180), int(abs(self.max180*60)%60), round( abs( self.max180*60*60 )%60, 2 )]
		if self.degarc180[2] == 60:
			self.degarc180[2] = 0
			self.degarc180[1] = (self.degarc180[1]+1) % 60
		if self.degarc180[1] == 60:
			self.degarc180[1] = 0
			self.degarc180[0] = (self.degarc180[0]+1) % 24
		
		
		#Seconds
		self.secs = self.hours[0]*60*60 + self.hours[1]*60 + self.hours[2]
		#Arcseconds
		self.arcsecs = self.degarc[0]*60*60 + self.degarc[1]*60 + self.degarc[2]
		
		# My silly way of going around isinstance which is apparently bad form. 
		self.ThisIsAnAngle = True  
	
	
	def __float__(self):#Angle in Radians
		return self.val
			
	def __str__(self):
		return str(round(self.deg10*1000)/1000)+"deg"
	
	def getHours(self):#This seems uneccesary... 
		return str(self.hours)
			
	def getDegarc180(self):#As does this
		return str(self.getDegarc180)
	
	#The idea for the add and subtract
	#magic methods is to allow an Angle
	#type or float type as the `other'
	#angle. float types are assumed to be
	#in radians
	def __radd__(self, other):
		try: 
			other.ThisIsAnAngle
			return Angle(self.val+other.val)
		except( AttributeError ):
			return Angle(self.val+other)
		
	def __add__(self, other):
		try: 
			other.ThisIsAnAngle
			return Angle(self.val+other.val)
		except( AttributeError ):
			return Angle(self.val+other)
	
	def __rsub__(self, other):
		try: 
			other.ThisIsAnAngle
			return Angle(self.val-other.val)
		except( AttributeError ):
			return Angle(self.val-other)
			
	def __sub__(self, other):
		try: 
			other.ThisIsAnAngle
			return Angle(self.val-other.val)
		except( AttributeError ):
			return Angle(self.val-other)
	
	def __rmul__(self, other):
		try: 
			other.ThisIsAnAngle
			return Angle( self.val*other.val )
		except( AttributeError ):
			return Angle( self.val*other )
	
	def __mul__(self, other):
		try: 
			other.ThisIsAnAngle
			return Angle( self.val*other.val )
		except( AttributeError ):
			return Angle( self.val*other )
	
	def __div__( self, other ):
		try: 
			other.ThisIsAnAngle
			return Angle( self.val/other.val )
		except( AttributeError ):
			return Angle( self.val/other )
			
	def __rdiv__( self, other ):
		try: 
			other.ThisIsAnAngle
			return Angle( self.val/other.val )
		except( AttributeError ):
			return Angle( self.val/other )
	
	def __mod__(self, other):
		return Angle(self.val % other.val)
	
	def __repr__(self):
		return self.__str__()
		
	def Format(self, Type='degarc', delim=':', units=False):
                """params
                Type: str 
                    must be degarc (sexagesimal degrees), 
                    degar180 (sexagesimal degrees betwee -180 +180),
                    or hours
                """
                assert Type in ('degarc', 'hours', 'degarc180')
		sign=''
		if Type=='degarc':
			l = self.degarc
			units=['d', 'am', 'as']
			
		elif Type=='hours':
			l=self.hours
			units=['h', 'm', 's']
			
		elif Type=='degarc180':
			l=self.degarc180
			if self.deg10>180:
				sign='-'
			else:
				sign='+'
			units=['d', 'am', 'as']
	
		if units == False:
			units = ['', '', '']
		units = ['', '', '']
		
		if self.Name == 'Hour_angle':# allow some angles to be in range [-180, 180].
			if l[0] < 0:	sign='-'
			else:				sign='+'
			
		return "%s%02d%s%s%02d%s%s%05.2f%s" %(sign, abs(l[0]), units[0], delim, l[1], units[1], delim, l[2],  units[2])
	

		
		
#Angle Subclasses for simplicity
class Dec_angle(Angle):
	def __init__(self, raw, delim=':'):
		Angle.__init__(self, raw, 'dec', delim=delim)
		self.Name = 'Dec_angle'
		#if abs(self.degarc180[0]) > 90: raise Exception("Declination angle is greater than 90 or less than -90 degrees!")
		
	def __str__(self):
		return Angle.Format(self, 'degarc180')
		
	def __getitem__(self, i):
		return self.degarc180[i]
		
		
class RA_angle(Angle):
	def __init__(self, raw, delim=':'):
			Angle.__init__(self, raw, 'hours', delim=delim)
			self.Name = 'RA_angle'
	def __str__(self):
		return Angle.Format(self, 'hours')
		
	def __getitem__(self, i):
		return self.hours[i]
		
		
class Hour_angle(Angle):
	def __init__(self, raw, delim=':'):
		Angle.__init__(self, raw, 'hours', delim=delim)
		self.Name = 'Hour_angle'
		if self.degarc180[0] < 0:
			self.hours = [self.hours[0]-24, abs(self.hours[1]-60)%60, abs(self.hours[2] - 60)%60]
		
	def __str__(self):
		return self.Format('hours')

class Deg10(Angle):
	def __init__(self, raw, Type='deg10', delim=':'):
		if type(raw) == str:
			raw = float(raw)
		Angle.__init__(self, raw, Type, delim=delim)
		self.Name = 'Deg10_angle'
		
	def __str__(self):
		return ("%.2f" %self.deg10)


#Add error handling
class delimError( exceptions.Exception ):
	def __init__( self, message ):
		Exception.__init__(self, message)

class parseError( exceptions.Exception ):
	def __init__( self, message ):
		Exception.__init__(self, message)
		
class signError( exceptions.Exception ):
	def __init__( self, message ):
		Exception.__init__(self, message)
	
if __name__ == '__main__':
	s=Dec_angle("-00:09:29.15")
	print s.Format("degarc180")
	
