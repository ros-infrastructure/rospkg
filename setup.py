#!/usr/bin/env python

import os
import sys

from setuptools import setup

install_requires = ['catkin_pkg', 'PyYAML']

if (
    'SKIP_PYTHON_MODULES' not in os.environ and
    'SKIP_PYTHON_SCRIPTS' not in os.environ
):
    install_requires.append('distro')

kwargs = {
    'name': 'rospkg',
    # same version as in:
    # - src/rospkg/__init__.py
    # - stdeb.cfg
    'version': '1.2.10',
    'packages': ['rospkg'],
    'package_dir': {'': 'src'},
    'entry_points': {
        'console_scripts': ['rosversion=rospkg.rosversion:main'],
    },
    'install_requires': install_requires,
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
    kwargs['install_requires'].remove('catkin_pkg')
if 'SKIP_PYTHON_SCRIPTS' in os.environ:
    kwargs['name'] += '_modules'
    kwargs['install_requires'].remove('catkin_pkg')
    kwargs['scripts'] = []
    kwargs['entry_points']['console_scripts'] = []

setup(**kwargs)
