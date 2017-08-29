# -*- coding: utf-8 -*-

"""SETUP"""

from setuptools import setup, find_packages

setup(
    name='tcc',
    version='0.1.0',
    description='Emerson Demetrio TCC',
    author='Emerson Demetrio',
    author_email='emer.demetrio@gmail.com',
    url='https://gitlab.com/emersondemetrio/tcc',
    packages=find_packages(exclude=('tests', 'docs'))
)
