#!/usr/bin/env python

from distutils.core import setup
import os

setup(name='astro',
      version='1.0',
      description='Python Distribution Utilities',
      author='Scott Swindell',
      author_email='scottswindell@email.arizona.edu',
	  packages = ['astro'],
	  package_dir = {'':'src'},
	  data_files = [('VSOP_Formated', ["VSOP_Formated/{0}".format(fname) for fname in os.listdir("VSOP_Formated") if fname.endswith('dat')])]
     )
