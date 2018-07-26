from .astrolib2 import starDate, locale
from .angles import *
import math
from .planets import *
from . import locales

d = starDate()

Tucson = locale('tucson', Deg10(32.2217), Deg10(110.9258), starDate())

f = open("catalogue/First_Mag.cat", 'r')

class astroobj:
	def __init__(self, Name, rawra, rawdec, delim=':'):
		self.name = Name
		self.ra = RA_angle(rawra, delim=delim)
		self.dec = Dec_angle(rawdec, delim=delim)
		self.iseq = True


def doeq2hor():	
	for line in f:
		name,ra,dec = [i for i in line.replace('\n', '').split("\t") if i != '' and i != "\n"][0:3]
		o=astroobj(name,ra,dec)
		alt,az = Tucson.eq2hor(o.ra,o.dec)
		print(name, alt, az)

def testPlanets():
	e=Earth(d.jd)
	
	
	s = Tucson.doPlanets()
	for a in s:
		alt, az = Tucson.eq2hor(a.ra, a.dec)
		print(a.name , alt, az)
	print() 
	Tucson.updatetime(60)
	s = Tucson.doPlanets()
	for a in s:
		alt, az = Tucson.eq2hor(a.ra, a.dec)
		print(a.name , alt, az)
	
def testrise_set(p):
	p = place
	m = p.planetEq('Mars')
	return p.settingAz(m.ra, m.dec)
	
	
place = locales.mtgraham()
jd0 = place.stardate.jd
for a in range(2*365):
	place.updatetime(24*3600)
	az = testrise_set(place).deg10
	if az<287 and az>285:
		print(place.stardate.date)
	#print place.stardate.jd-jd0,testrise_set(place).deg10
	
