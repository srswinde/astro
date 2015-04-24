#!/usr/bin/env python

from distutils.core import setup

setup(name='astro',
      version='1.0',
      description='Python Distribution Utilities',
      author='Scott Swindell',
      author_email='scottswindell@email.arizona.edu',
	  packages = ['astro'],
	  package_dir = {'':'src'}
     )
