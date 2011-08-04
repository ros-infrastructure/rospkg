# Software License Agreement (BSD License)
#
# Copyright (c) 2011, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id: packages.py 14291 2011-07-13 03:24:43Z kwc $
# $Author: kwc $

import os
import sys

from .common import RosPkgException, ManifestManager, ResourceNotFound, MANIFEST_FILE, STACK_FILE
from .environment import get_ros_root, get_ros_package_path, get_ros_home

class RosPack(ManifestManager):
    """
    Utility class for querying properties about ROS packages. This
    should be used when querying properties about multiple
    packages.

    NOTE: for performance reasons, RosPack caches information about
    packages.

    Example::
      rp = RosPack()
      packages = rp.list_packages()
      path = rp.get_path('rospy')
      depends = rp.get_depends('roscpp')
      depends1 = rp.get_depends1('roscpp')
    """
    
    def __init__(self, ros_root=None, ros_package_path=None):
        """
        @param ros_root: (optional) override ROS_ROOT.
        @param ros_package_path: (optional) override ROS_PACKAGE_PATH.
        To specify no ROS_PACKAGE_PATH, use the empty string.  An
        assignment of None will use the default path.
        """
        super(RosPack, self).__init__(MANIFEST_FILE,
                                      'rospack_cache',
                                      list_packages_by_path,
                                      ros_root, ros_package_path)
        self._rosdeps_cache = {}

    def get_rosdeps(self, package, implicit=False):
        """
        Collect rosdeps of specified package into a dictionary.
        
        @param package: package name
        @type  package: str
        @param implicit: include implicit (recursive) rosdeps
        @type  implicit: bool
        
        @return: list of rosdep names.
        @rtype: [str]
        """
        m = self.get_manifest(package)
        if implicit:
            return self._implicit_rosdeps(package)
        else:
            return [d.name for d in m.rosdeps]
        
    def _implicit_rosdeps(self, package):
        """
        Compute recursive rosdeps of a single package and cache the
        result in self._rosdeps_cache.

        @param package: package name
        @type  package: str
        @return: list of rosdeps
        @rtype: [str]
        """
        if package in self._rosdeps_cache:
            return self._rosdeps_cache[package]

        # set the key before recursive call to prevent infinite case
        self._rosdeps_cache[package] = s = set()

        # take the union of all dependencies
        packages = self.get_depends(package)
        for p in pkgs:
            s.update(self._rosdeps(p))
        # add in our own deps
        m = self.get_manifest(package)
        s.update([d.name for d in m.rosdeps])
        # cache the return value as a list
        s = list(s)
        self._rosdeps_cache[package] = s
        return s
        
    def stack_of(self, package):
        """
        @param package: package name
        @type  package: str
        @return: name of stack that package is in, or None if package is not part of a stack
        @rtype: str
        @raise ResourceNotFound: if package cannot be located
        """
        d = self.get_path(package)
        while d and os.path.dirname(d) != d:
            stack_file = os.path.join(d, STACK_FILE)
            if os.path.exists(stack_file):
                return os.path.basename(d)
            else:
                d = os.path.dirname(d)
        
