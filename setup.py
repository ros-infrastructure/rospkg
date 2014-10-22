#!/usr/bin/env python

import os
from setuptools import setup
import sys

exec(open(os.path.join(os.path.dirname(__file__), 'src', 'rospkg', '_version.py')).read())

install_requires = ['PyYAML']
if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    install_requires.append('argparse')

setup(name='rospkg',
      version=__version__,
      packages=['rospkg'],
      package_dir = {'':'src'},
      scripts = ['scripts/rosversion'],
      install_requires=install_requires,
      author = "Ken Conley", 
      author_email = "kwc@willowgarage.com",
      url = "http://wiki.ros.org/rospkg",
      download_url = "http://download.ros.org/downloads/rospkg/",
      keywords = ["ROS"],
      classifiers = [
        "Programming Language :: Python", 
        "License :: OSI Approved :: BSD License" ],
      description = "ROS package library", 
      long_description = """\
Library for retrieving information about ROS packages and stacks.
""",
      license = "BSD"
      )
