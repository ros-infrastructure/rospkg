#!/usr/bin/env python

import os
import sys

from setuptools import setup

kwargs = {
    'name': 'rospkg',
    # same version as in:
    # - src/rospkg/__init__.py
    # - stdeb.cfg
    'version': '1.1.4',
    'packages': ['rospkg'],
    'package_dir': {'': 'src'},
    'entry_points': {
        'console_scripts': ['rosversion=rospkg.rosversion:main'],
    },
    'install_requires': ['catkin_pkg', 'PyYAML'],
    'author': 'Ken Conley',
    'author_email': 'kwc@willowgarage.com',
    'url': 'http://wiki.ros.org/rospkg',
    'keywords': ['ROS'],
    'classifiers': [
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License'],
    'description': 'ROS package library',
    'long_description': """\
        Library for retrieving information about ROS packages and stacks.
        """,
    'license': 'BSD'
}

if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    kwargs['install_requires'].append('argparse')

if 'SKIP_PYTHON_MODULES' in os.environ:
    kwargs['packages'] = []
    kwargs['package_dir'] = {}
if 'SKIP_PYTHON_SCRIPTS' in os.environ:
    kwargs['name'] += '_modules'
    kwargs['scripts'] = []

setup(**kwargs)
