#!/usr/bin/python

from locales import tucson
from astrodate import starDate
from angles import Hour_angle
import sys

def night():
	mins = 0

	for a in range(60*24):
		alt, az = t.sunhor()
		t.updatetime(60)
	
		if alt.deg10 > 90:
			mins+=1
		
	print mins


def sunset( place ):
	day = False
	alt, az = place.sunhor()
	if alt.deg10 <= 90.0: day = True
	else:day = False
	
	while day:
		
		alt = place.sunhor()[0]
		if alt.deg10 > 90.0:
			return place.stardate
		place.updatetime(60)
		
	while not day:
		
		alt = place.sunhor()[0]
		if alt.deg10 < 90.0:
			return place.stardate
		place.updatetime(-60)
	
	
def planet_at_sunset( planetStr, outfile ):	
	pl = tucson()
	print pl.stardate.date
	for a in range(1, 365, 1):
		pl.updatetime(24*60*60)
		
		date = sunset( pl )
		newDate = starDate( date=date.date, UT=date.UT+Hour_angle( [5,0,0] ) )
		t=tucson( stardate=newDate )
		#t.updatetime(60*60)# an hour after sunset
		thePlanet = t.planetEq(planetStr)
	
		alt, az = t.eq2hor(thePlanet.ra, thePlanet.dec)
	
	
	
	#print ( date.UT - Hour_angle([7,0,0]) ).hours, date.date, jalt, j.ra,j.dec, t.LST.hours
		
		if alt.deg10 < 90:
			dateStr = "{1}/{2}/{0}".format(*t.stardate.date)
			outStr = dateStr+" "+str(alt.deg10) +"\n"
			outfile.write(outStr)
			#print outStr
		


	
if __name__ == "__main__":
	if len( sys.argv ) == 2:
		planet_at_sunset(sys.argv[1])
		
	else:
		for plan in ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Neptune"]:
			planet_file = open("/home/scott/planets/fivehour/"+plan.lower()+".dat", 'w')
			print plan
			planet_at_sunset(plan, planet_file)
			planet_file.close()
			
			
		
		
