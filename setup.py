#!/usr/bin/env python

import os
import sys

from setuptools import setup

kwargs = {
    'name': 'rospkg',
    # same version as in:
    # - src/rospkg/__init__.py
    # - stdeb.cfg
    'version': '1.2.4',
    'packages': ['rospkg'],
    'package_dir': {'': 'src'},
    'entry_points': {
        'console_scripts': ['rosversion=rospkg.rosversion:main'],
    },
    'install_requires': ['catkin_pkg', 'distro', 'PyYAML'],
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

if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and
        sys.version_info[1] < 8):
    kwargs['install_requires'].remove('distro')

if 'SKIP_PYTHON_MODULES' in os.environ:
    kwargs['packages'] = []
    kwargs['package_dir'] = {}
    kwargs['install_requires'] = [
        p for p in kwargs['install_requires']
        if p not in {'catkin_pkg', 'distro'}]
if 'SKIP_PYTHON_SCRIPTS' in os.environ:
    kwargs['name'] += '_modules'
    kwargs['install_requires'] = [
        p for p in kwargs['install_requires']
        if p not in {'catkin_pkg', 'distro'}]
    kwargs['scripts'] = []
    kwargs['entry_points']['console_scripts'] = []

setup(**kwargs)
