# coding: utf-8
import os
from setuptools import find_packages, setup

from pfbox import version

# get the dependencies and installs
root = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(root, 'requirements.txt')) as f:
    all_requirements = f.read().split('\n')

setup(
    name='pfbox',
    version=version,
    author='justworld',
    description='python framework box',
    url='https://github.com/justworld/pfbox',
    packages=find_packages(exclude=['tests']),
    package_data={'pfbox': ['README.md']},
    install_requires=all_requirements
)
