#!/usr/bin/env python3
from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))


with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hfilesize',
    version='0.1.0',
    license='MIT',
    description='Human Readable File Sizes',
    long_description=long_description,
    url='https://github.com/simonzack/hfilesize',

    author='simonzack',
    author_email='simonzack@gmail.com',

    packages=find_packages(),

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License,
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
