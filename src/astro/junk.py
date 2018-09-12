from .locales import mtgraham
from .angles import Hour_angle

l=mtgraham()


for a in range(0,3600*3,60):
	l.updatetime(60)
	el = l.sunhor()[0]
	print((l.stardate.UT-Hour_angle([7,0,0])).hours, el)
	if el.deg10 < 90:
		break


print(a/3600.0)
