#!/usr/bin/env python

from distutils.core import setup

import sys
sys.path.insert(0, 'src')

from rospkg import __version__

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
