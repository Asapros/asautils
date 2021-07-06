from setuptools import setup
from platform import system

needed_packages = ['colorama', 'leb128']


if system() == "Windows":
    needed_packages.append("windows-curses")

setup(
   name='asautils',
   version='1.0',
   description='A useful python package',
   author='Asapros',
   packages=['asautils'],
   install_requires=needed_packages
)
