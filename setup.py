#!/usr/bin/env python

import os

from setuptools import setup

install_requires = ['catkin_pkg', 'PyYAML']

if (
    'SKIP_PYTHON_MODULES' not in os.environ and
    'SKIP_PYTHON_SCRIPTS' not in os.environ
):
    install_requires.append("distro >= 1.4.0; python_version >= '3.8'")

kwargs = {
    'name': 'rospkg',
    # same version as in:
    # - src/rospkg/__init__.py
    # - stdeb.cfg
    'version': '1.6.1',
    'packages': ['rospkg'],
    'package_dir': {'': 'src'},
    'entry_points': {
        'console_scripts': ['rosversion=rospkg.rosversion:main'],
    },
    'install_requires': install_requires,
    'extras_require': {
        'test': [
            'pytest',
        ]},
    'author': 'Ken Conley',
    'author_email': 'kwc@willowgarage.com',
    'maintainer': 'ROS Infrastructure Team',
    'project_urls': {
        'Source code':
        'https://github.com/ros-infrastructure/rospkg',
        'Issue tracker':
        'https://github.com/ros-infrastructure/rospkg/issues',
    },
    'url': 'http://wiki.ros.org/rospkg',
    'keywords': ['ROS'],
    'classifiers': [
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License'],
    'python_requires': '>=3.6',
    'description': 'ROS package library',
    'long_description': """\
        Library for retrieving information about ROS packages and stacks.
        """,
    'license': 'BSD'
}

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
