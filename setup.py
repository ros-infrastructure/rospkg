#!/usr/bin/env python

import os
from setuptools import setup

exec(open(os.path.join(os.path.dirname(__file__), 'src', 'rospkg', '_version.py')).read())

setup(name='rospkg',
      version=__version__,
      packages=['rospkg'],
      package_dir = {'':'src'},
      scripts = ['scripts/rosversion'],
      author = "Ken Conley", 
      author_email = "kwc@willowgarage.com",
      url = "http://www.ros.org/wiki/rospkg",
      download_url = "http://pr.willowgarage.com/downloads/rospkg/", 
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
