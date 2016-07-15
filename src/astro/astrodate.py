from angles import *
import math
import time
import datetime
import pytz
#Class to handle all time considerations
#Arguments:	jd, date, ut
#Description:	Holds Julian Date, Gregorian calendar date, UT
#		and Greenwich Sidereal time for a given epoch
#		With methods to convert between jd and gregorian
#		calendar.
class starDate:
	def __init__(self, jd=False, date=False, UT=False):
		if not UT: self.UT=Angle(0)
		else:self.UT=UT
		if not date:
			 if not jd:
			 	self.date = (time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday)
			 	self.UT = RA_angle([time.gmtime().tm_hour, time.gmtime().tm_min, time.gmtime().tm_sec])
			 	self.jd = self.calcJD()
			 	
			 else:
			 	self.jd = jd
			 	self.date, self.UT=self.calcDate()
		else:
			self.date=date
			self.jd = self.calcJD()
		self.GMST = self.calcGMST()
		self.mjd = self.jd - 2400000.5 
		
		
	#calculate a calendar date from julian date	
	#Astronomical Algorithms 2nd ed. pg 63
	def calcDate( self ):
		jd = self.jd+0.5
		Z = int( jd )
		F = jd - Z #Decimal portion of jd
		A = Z
		if Z > 2299161: 
			alpha = int( (Z-1867216.25)/36524.25 )
			A = Z+1+alpha-int(alpha/4.0)
		
		B = A+1524
		C = int( (B-122.1)/365.25 )
		D = int(365.25*C)
		E = int( (B-D)/30.6001 )
		day = B-D-int(30.6001*E)+F
		if E<14:month = E-1
		elif E==14 or E==15: month=E-13
		
		if month > 2: year = C-4716
		else: year = C-4715
		UT = Angle((day-int(day))*2*math.pi)
		date = (year, month, int(day))
		return (date, UT)
	
	
	#Calculate the Julian date from the gregorian date
	#Astronomical Algorithms second edition
	def calcJD(self):
		year,month,day = self.date
		day = day+self.UT.hourdecimal/24.0 #add time to day
		
		if(month == 2 or month == 1):
			year = year-1
			month = month+12
	
		A = int(year/100)
		B = 2 - A + int(A/4)
		
		return(int(365.25*(year+4716)) + int(30.6001*(month+1)) + day + B - 1524.5)
		
	
	#Greenwich Sidereal Time from jd
	#Astronomical Algorithms 2nd ed.
	def calcGMST(self):
		jd = self.jd
		T = (jd - 2451545.0)/36525 # Julian Centuries since 2000
		theta0 = 280.46061837 + 360.98564736629*(jd-2451545.0) + 0.000387933*T*T - (T*T*T)/38710000
		
		return RA_angle( Deg10( theta0 ) )
		
	def __float__(self):
		return self.jd
		
	def __str__(self):
		outstr = self.datestr()+"\n"
		outstr+= "Julian Date:\t\t%f\n"%self.jd
		outstr+= "Modified Julian Date:\t\t%f\n"%self.mjd
		
		return outstr

	#Add days to JD and update GMST, UT and Gregorian Date
	def addDays(self, days):
		self.jd = self.jd+days
		self.mjd = self.jd - 2400000.5 
		self.date,self.UT = self.calcDate()
		self.GMST = self.calcGMST()
		
	#Add seconds to JD and update GMST, UT and Gregorian Date
	def addSecs(self, secs):
		self.addDays(secs/(24.0*3600))

	def datestr( self ):
		months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		days = [
					'First',
					'Second',
					'Third',
					'Fourth',
					'Fifth',
					'Sixth',
					'Seventh',
					'Eighth',
					'Ninth'
					'Tenth',
					'Eleventh',
					'Twelfth',
					'Thirteenth',
					'Fourteenth',
					'Fifteenth',
					'Sixteenth',
					'Seventeenth',
					'Eighteenth',
					'Nineteenth',
					'Twenthieth',
					'Twenty First',
					'Twenty Second',
					'Twenty Third',
					'Twenty Fourth',
					'Twenty Fifth',
					'Twenty Sixth',
					'Twenty Seventh',
					'Twenty Eighth',
					'Twenty Ninth',
					'Thirtieth',
					'Thirty First'
					]
	
		return "the %s of %s %d" %( days[self.date[2]-1], months[self.date[1]-1], self.date[0] )

		
	def datetime(self):
		self.GMST = self.calcGMST()
		self.mjd = self.jd - 2400000.5 
		year, mon, day = self.date
		hh,mm = self.UT.hours[:2]
		ss = int(self.UT.hours[-1])
		ms = int( (self.UT.hours[-1]-ss)*1e6 )
		return datetime.datetime( year, mon, day, hh, mm, ss, ms, pytz.timezone("Universal") )

		
