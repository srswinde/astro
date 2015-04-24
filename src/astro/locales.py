from angles import *
from astrolib2 import locale
from astrodate import starDate

class tucson(locale):
	def __init__( self, stardate=False ):
		if stardate:
			
			locale.__init__( self, 'Tucson', lat=Deg10(32.22), lon=Deg10(110.9258), stardate=stardate )
		else:
			locale.__init__( self, 'Tucson', lat=Deg10(32.22), lon=Deg10(110.9258), stardate=starDate() )


class kittpeak(locale):
	def __init__( self, stardate=starDate() ):
		if stardate == False: stardate = starDate()
		locale.__init__(self, 'Kitt Peak', lat=Deg10(31.9583), lon=Deg10(111.5967), stardate=stardate)
		
class mtlemmon(locale):
	def __init__( self, stardate=starDate() ):
		if stardate == False: stardate = starDate()
		locale.__init__( self, "Mount Lemmon", lat=Deg10(32.44313), lon=Deg10(110.78843), stardate=stardate )
		
class mtgraham(locale):
	def __init__( self, stardate=starDate() ):
		if stardate == False: stardate = starDate()
		locale.__init__( self, 'Mount Graham', lat=Deg10(32.701272), lon=Deg10(109.892100), stardate=stardate )

class greenwich( locale ):
	def __init__( self, stardate=starDate() ):
		if stardate == False: stardate = starDate()
		locale.__init__( self, 'Greenwich', lat=Deg10(51.4791), lon=Deg10( 0.000 ), stardate=stardate )
