from . import locales
import sys


here=locales.tucson()


if sys.argv[1].lower() == 'lst':
	print(here.LST.Format('hours'))



elif sys.argv[1].lower() == 'ut':
	print(here.stardate.UT)
	
elif sys.argv[1].lower() == 'gmst':
	print(here.stardate.GMST.Format('hours'))
	
elif sys.argv[1].lower() == 'jd':
	print(here.stardate.jd)

