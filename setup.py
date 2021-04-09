from setuptools import setup
from platform import system

curses_name = "curses"
if system() == "Windows": curses_name = "windows-curses"

setup(
   name='asautils',
   version='1.0',
   description='A useful python package',
   author='Asapros',
   packages=['asautils'],
   install_requires=['colorama', curses_name]
)
