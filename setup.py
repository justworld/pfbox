# coding: utf-8
import os
from setuptools import find_packages, setup

from pythonframework import version

# get the dependencies and installs
root = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(root, 'requirements.txt')) as f:
    all_requirements = f.read().split('\n')

setup(
    name='pythonframework',
    version=version,
    author='justworld',
    description='python framework',
    url='https://github.com/justworld/python-framework',
    packages=find_packages(exclude=['examples']),
    package_data={'pythonframework': ['README.md']},
    install_requires=all_requirements
)
