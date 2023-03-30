from setuptools import setup, find_packages
from distutils.core import setup
from run import start
# import py2exe

setup(scripts=['run.py'])

print(find_packages)
setup(name='TelloBeep',
version='2',
description='Bot for automating instagram spoteds',
url='https://github.com/spottedmi/TelloBeep',
author='RandomGuy90',
author_email='randomguy0090@gmail.com',
license='MIT',
packages=find_packages(),
zip_safe=False)
