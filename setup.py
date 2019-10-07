# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in restore/__init__.py
from restore import __version__ as version

setup(
	name='restore',
	version=version,
	description='restore',
	author='suraj varade',
	author_email='varade.suraj787@gmail.co',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
