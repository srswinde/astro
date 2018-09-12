#!/usr/bin/python
from .locales import tucson;t=tucson()
from .angles import Hour_angle

for a in range(90*24):
	jup = t.doPlanets()[2]
	
	el,az =t.eq2hor( jup.ra, jup.dec )
	if el.deg10 < 90:
		print(t.stardate.date, ( t.stardate.UT+Hour_angle ( [12,0,0] ) ).hours)
	t.updatetime(60*24)
	
	
