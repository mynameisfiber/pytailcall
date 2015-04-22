#!/usr/bin/env python

from distutils.core import setup

setup(
    name='pytailcall',
    version='1.0',
    description='Bytecode hacks for tail call optimizations in python',
    author='Micha Gorelick',
    author_email='mynameisfiber@gmail.com',
    url='http://github.com/mynameisfiber/pytailcall/',
    packages=['pytailcall', 'pytailcall.experiments'],
)

