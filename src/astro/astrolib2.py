from .angles import *
from .astrodate import starDate
from . import planets
import time
import math
import collections


Epsilon = Angle([23, 27, 0], 'degarc')# obliquity of the ecliptic at J2000



def transits(ra, dec, jd=False, lat=Deg10(32.2217), lon=Deg10(110.9258)):
	if not jd: jd=julian_date(now=True)
	jd = int(jd)+0.5
	ST0 = calcGMST(jd)#Siderial Time  0 hour UT
	
	alt,az = calc_AltandAz(ra, dec,jd=jd)
	H0 = Angle( math.acos((math.sin(-0.5667*math.pi/180 )-math.sin( lat )*math.sin( dec ))/(math.cos( lat )*math.cos( dec ))) )
	
	TRANSIT = (( ra+lon-ST0 ).deg10/( 360.0 ))%1
	RISE = (TRANSIT - H0.deg10/(360.0))%1
	SET = (TRANSIT + H0.deg10/(360.0))%1
		
	return (TRANSIT, RISE, SET)

#Simple class for holding an objects ra and dec
class astroobj:
	def __init__(self, Name, rawra, rawdec, delim=':'):
		self.name = Name
		self.ra = RA_angle(rawra, delim=delim)
		self.dec = Dec_angle(rawdec, delim=delim)
		self.iseq = True

	
	
	def __str__(self):
		return "%s %s %s"%(self.name, self.ra, self.dec)
		
	def __repr__(self):
		return self.name


class astroobj2( collections.MutableMapping ):
	def __init__( self, Name=False, rawra=False, rawdec=False, delim=':', *args, **kwargs ):
		self.store = dict()
		self.update(dict(*args, **kwargs))
		
		if not rawra:
			self.store['ra'] = RA_angle( rawra, delim=delim )
		elif 'ra' in self.store:
			self.store['ra'] = RA_angle( self.store[ra], delim=delim )
		else:
			raise KeyError('ra')
			
		if not rawdec:
			self.store['dec'] = Dec_angle( rawdec, delim=delim )
		elif 'dec' in self.store:
			self.store['dec'] = RA_angle( self.store['dec'], delim=delim )
		else:
			raise KeyError('name')
			
		if not Name:
			self.store['name'] = Name
		elif 'name' not in self.store:
			raise KeyError('name')
			
		self.ra = self.store['ra']
		self.dec = self.store['dec']
		self.name = self.store['name']
		
	def __str__( self ):
		return "{name} {ra} {dec}".format( **self.store )

	def __repr__( self ):
		return self.store[self.__keytransform__('name')]

	def __keytransform__( self, key ):
		return key	
		
	def __getitem__( self, key):
		return self.store[self.__keytransform__(key)]
		
	def __setitem__( self, key, value ):
		self.store[self.__keytransform__(key)] = value
	
	def __delitem__(self, key):
		del self.store[self.__keytransform__(key)]
	
	def __iter__( self ):
		return iter( self.store )
		
	def __len__(self):
		return len(self.store)

#Class to handle all location specific astronomy
#Arguments: name, lat, lon, stardate (astrodate.py)
#Decription: Methods for generating ephemerides for 
#		for extra solar objects and planets
#		will work on ephemerides from 
#		orbital elements.
#		also while be good to include
#		corrections ie epoch, aberation,
#		refraction etc. 

class locale:
	def __init__(self, name, lat, lon, stardate, diffUT=False):
		self.name = name
		self.lon = lon
		self.lat = lat
		self.diffUT=diffUT
		self.stardate = stardate
		self.LST = self.stardate.GMST - self.lon		
		
		
	def __str__(self):
		return "%s lattitude:%s longitude:%s at %f" %(self.name, self.lat, self.lon, self.stardate.jd)
		
	def hor2eq(self, alt, az):#Horizontal coordinates to equatorial
		#subtract 180 degrees to azimuth b/c equations assume azimuth measured from the south.
		az = Angle(az.val - math.pi, 'radians')
		#Equations are from astronomical algorithms
		ha = Angle(math.atan2(math.sin(az), (math.cos(az)*math.sin(self.lat) + math.tan(alt)*math.cos(self.lat))), 'radians')
		Dec = Angle(math.asin(math.sin(self.lat)*math.sin(alt) - math.cos(self.lat)*math.cos(alt)*math.cos(az)), 'radians')
		
		RA = self.LST - ha
		return [RA, Dec]
		
		
	def eq2hor(self, ra, dec):#Equatorial to horizontal coordinates
		ha = self.stardate.GMST - self.lon - ra
		alt = Deg10(Angle(math.asin(math.sin(self.lat)*math.sin(dec) + math.cos(self.lat)*math.cos(dec)*math.cos(ha))))
		az = Deg10(Angle(math.pi+math.atan2(math.sin(ha), math.cos(ha)*math.sin(self.lat) - math.tan(dec)*math.cos(self.lat))))# Measured from north 
		
		return [alt, az]
		
	def ra2ha(self, ra):
		return Hour_angle(self.LST-ra)
		
	def ha2ra(self, ha):
		return self.LST-ha
	
	def hor2hadec(self, alt, az):
		ha = Angle( math.atan2( math.sin( alt ), math.cos( alt ) * math.cos( self.lat ) + math.tan( alt ) *  math.cos( self.lat ) ) )
		Dec = Angle( math.asin( math.sin( Lat ) * math.sin( alt ) - math.cos( Lat ) * math.cos( alt ) * math.cos( az ) ) )
		return ha, dec
	

		
	
		
	def suneq(self):#Eq coords of sun
		e=self.earthPos().pos
		
		x=-e.x
		y=-e.y
		z=-e.z
		
		Lambda = Angle(math.atan2(y, x), 'radians')
		Beta = Angle(math.atan2(z,math.sqrt(x*x + y*y)), 'radians')
		
		RAangle = math.atan2((math.sin(Lambda)*math.cos(Epsilon) - math.tan(Beta)*math.sin(Epsilon)),math.cos(Lambda))
		
		Decangle = math.asin(math.sin(Beta)*math.cos(Epsilon) + math.cos(Beta)*math.sin(Epsilon)*math.sin(Lambda))
		
		RA = Angle(RAangle, 'radians')	
		Dec = Angle(Decangle, 'radians')
		
		return [RA, Dec]
		
		
		
	
	
	def sunhor(self):
		ra,dec = self.suneq()
		return self.eq2hor(ra, dec)
		
	def planets(self, name):
		return Planet(name=name, T=self.jd)
		
	#def updatetime(self,t):#t is in seconds
		#self.stardate.jd = self.stardate.jd+t/(24.0*3600.0)
	
	def settingHA(self, ra, dec):
		jd = int(self.stardate.jd)+0.5
		ST0 = starDate(jd=jd, UT=Deg10(0))#sidereal time at 0 hour UT
	
		return Angle(math.acos(-math.tan(self.lat)*math.tan(dec)))
	
	def settingAz(self, ra, dec):
		ha = self.settingHA(ra,dec)
		return Angle(math.atan2(math.sin(ha),math.cos(ha)*math.sin(self.lat)-math.tan(dec)*math.cos(self.lat)))+Angle(math.pi)
	
	def doPlanets(self):
		
		pls = planets.doAll(self.stardate.jd)
		allPlanets = []
		
		for p in pls:
			allPlanets.append(self.planetEq(p))
		
		return allPlanets
	
	def earthPos(self):
		return planets.Earth(self.stardate.jd)
			
	def planetEq(self, planet):
		if type(planet) == str:
			planet = planets.Planet(planet, self.stardate.jd)
		earth = self.earthPos()
		diff = planet.pos - earth.pos
		x,y,z = diff.x,diff.y,diff.z
		
		Lambda = Angle(math.atan2(y, x), 'radians')
		Beta = Angle(math.atan2(z,math.sqrt(x*x + y*y)), 'radians')
		
		RAangle = math.atan2((math.sin(Lambda)*math.cos(Epsilon) - math.tan(Beta)*math.sin(Epsilon)),math.cos(Lambda))
		
		Decangle = math.asin(math.sin(Beta)*math.cos(Epsilon) + math.cos(Beta)*math.sin(Epsilon)*math.sin(Lambda))
		
		RA = RA_angle(Angle(RAangle, 'radians'))
		
		Dec = Dec_angle(Angle(Decangle, 'radians'))
		return astroobj(planet.name, RA, Dec)
		
	#add t in seconds to locale time
	def updatetime(self, t):
		self.stardate.addSecs(t)
		self.LST = self.stardate.GMST-self.lon	


def precess(jd_i=2451545.0, jd_f=False, calendar='J', ra=False, dec=False, obj=False):
	"""Add precession to coords from Astronomical Algorithms pg 134"""
	
	if obj != False:
		ra = obj.ra
		dec = obj.dec
		
	jd_2000 = 2451545.0
	
	if not jd_f:
		jd_f = starDate().jd
		
	T = (jd_i - jd_2000)/36525
	
	t = (jd_f - jd_i)/36525
	
	#these coeffs are in arcseconds and then converted to Angle class
	zeta = Deg10( ( (2306.2181 + 1.39656*T - 0.000139*T**2)*t +  (0.30188 - 0.000344*T)*t**2 + 0.017998*t**3 )/3600 )
	z = Deg10( ( (2306.2181 + 1.39656*T - 0.000139*T**2)*t + (1.09468 + 0.000066*T)*t**2 + 0.018203*t**3 )/3600 )
	theta = Deg10( ( (2004.3109 - 0.85330*T - 0.000217*T**2)*t - (0.42665 + 0.000217*T)*t**2 - 0.041833*t**3)/3600 )
	
	A = math.cos(dec)*math.sin(ra + zeta )
	B = math.cos(theta)*math.cos(dec)*math.cos(ra + zeta) - math.sin(theta)*math.sin(dec)
	C = math.sin(theta)*math.cos(dec)*math.cos(ra + zeta) + math.cos(theta)*math.sin(dec)
	
	print(T, t)
	print("Coeffs are ",A,B,C)
	ra_p = Angle( math.atan2(A, B) ) + z
	if (90-dec.deg10) > 5:
		dec_p = Angle( math.asin(C) )
	else:
		dec_p = Angle( math.acos(math.sqrt( A*A + B*B ) ) )
	
	return RA_angle(ra_p), Dec_angle( dec_p )
	
	
	

