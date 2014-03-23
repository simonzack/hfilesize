#!/usr/bin/env python3

import re
from setuptools import setup, find_packages

try:
	import pypandoc

	with open('README.md') as file:
		long_description = pypandoc.convert(file.read(), 'rst', format='md')
		#pandoc bug workaround
		long_description = re.sub(r'(:alt:\s*(.+)\s*\r?\n)\s*\r?\n\s*\2', r'\1', long_description)

except ImportError:
	long_description = ''

setup(
	name='hfilesize',
	version='0.1.0',
	license='GPLv3',
	description='Human Readable File Sizes',
	long_description=long_description,
	url='https://github.com/simonzack/hfilesize',

	author='simonzack',
	author_email='simonzack@gmail.com',

	packages=find_packages(),

	classifiers = [
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Programming Language :: Python :: 3',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
)
