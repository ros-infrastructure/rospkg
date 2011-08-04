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

from .common import RosPkgException, MANIFEST_FILE
from .environment import get_ros_root, get_ros_package_path, get_ros_home

class PackageNotFound(RosPkgException):
    """
    Exception that indicates that a ROS package does not exist
    """
    pass

class InvalidPackage(RosPkgException):
    """
    Exception that indicates that a ROS package is invalid (e.g. bad manifest).
    """
    pass

def is_package_dir(d):
    """
    @param d: directory location
    @type  d: str
    @return: True if d is the root directory of a ROS package
    @rtype: bool
    """
    return os.path.isfile(os.path.join(d, MANIFEST_FILE))

def _compute_package_paths(ros_root, ros_package_path):
    """
    Get the paths to search for packages in reverse precedence order (i.e. last path wins).
    """
    if ros_package_path:
        return list(reversed([x for x in ros_package_path.split(os.pathsep) if x])) + [ros_root]
    else:
        return [ros_root]

_pkg_dir_cache = {}

def _read_rospack_cache(cache, ros_root, ros_package_path):
    """
    Read in rospack_cache data into cache. On-disk cache specifies a
    ROS_ROOT and ROS_PACKAGE_PATH, which must match the requested
    environment.
    
    @param cache: empty dictionary to store package list in. 
        The format of the cache is {package_name: file_path}.
    @type  cache: {str: str, str, str}
    @param ros_package_path: ROS_ROOT value to validate cache.
    @type  ros_root: str
    @param ros_package_path: ROS_PACKAGE_PATH value or '' if not specified
    @type  ros_package_path: str
    @return: True if on-disk cache matches and was loaded, false otherwise
    @rtype: bool
    """
    try:
        ros_root_validated = ros_package_path_validated = False
        with open(os.path.join(get_ros_home(), 'rospack_cache')) as f:
            for l in f.readlines():
                l = l[:-1]
                if not len(l):
                    continue
                if l[0] == '#':
                    # check that the cache matches our env
                    if l.startswith('#ROS_ROOT='):
                        ros_root_validated = True
                        if not l[len('#ROS_ROOT='):] == ros_root:
                            return False
                    elif l.startswith('#ROS_PACKAGE_PATH='):
                        ros_package_path_validated = True
                        if not l[len('#ROS_PACKAGE_PATH='):] == ros_package_path:
                            return False
                else:
                    cache[os.path.basename(l)] = l
                    
        if not ros_root_validated or not ros_package_path_validated:
            return False
        return True
    except Exception as e:
        pass
    
def list_packages_by_path(path, cache):
    """
    List ROS packages within the specified path.  Also updates a dictionary
    cache that records the directories wher epackages are found.
    
    @param path: path to list packages in
    @type  path: str
    @param packages: list of packages to append to. If package is
      already present in packages, it will be ignored.
    @type  packages: [str]
    @param cache: package path cache to update. Maps package name to directory path.
    @type  cache: {str: str}
    @return: complete list of package names in path.
    @rtype: [str]
    """
    packages = []

    path = os.path.abspath(path)
    for d, dirs, files in os.walk(path, topdown=True):
        if MANIFEST_FILE in files:
            package = os.path.basename(d)
            if package not in packages:
                packages.append(package)
                cache[package] = d
            del dirs[:]
            continue #leaf
        elif 'rospack_nosubdirs' in files:
            del dirs[:]
            continue #leaf
        #small optimization
        elif '.svn' in dirs:
            dirs.remove('.svn')
        elif '.git' in dirs:
            dirs.remove('.git')

        for sub_d in dirs:
            # followlinks=True only available in Python 2.6, so we
            # have to implement manually
            sub_p = os.path.join(d, sub_d)
            if os.path.islink(sub_p):
                packages.extend(list_pkgs_by_path(sub_p, cache=cache))
            
    return packages

def _safe_load_manifest(p):
    """
    Calls roslib.manifest.load_manifest and returns None if the calls raises an Exception (i.e. invalid package)
    """
    try:
        return roslib.manifest.load_manifest(p)
    except:
        return roslib.manifest.Manifest()

class RosPack(object):
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
        self._ros_root = ros_root or get_ros_root()
        self._ros_package_path = ros_package_path
        if self._ros_package_path is None:
            self._ros_package_path = get_ros_package_path()
            
        self._package_paths = _compute_package_paths(ros_root, ros_package_path)
        
        self._manifests = {}
        self._depends_cache = {}
        self._rosdeps_cache = {}
        self._package_cache = None

    def get_ros_root(self):
        return self._ros_root
    ros_root = property(get_ros_root, doc="Get ROS_ROOT of this RosPack instance")

    def get_ros_package_path(self):
        return self._ros_package_path
    ros_package_path = property(get_ros_package_path, doc="Get ROS_PACKAGE_PATH of this RosPack instance")

    def get_manifest(self, package):
        if package in self._manifests:
            return self._manifests[package]
        else:
            return self._load_manifest(package)
            
    def _update_package_cache(self):
        if self._package_cache is not None:
            return
        # initialize cache
        cache = self._package_cache = {}
        # - first attempt to read .rospack_cache
        if _read_rospack_cache(cache, self._ros_root, self._ros_package_path):
            return list(cache.keys()) #py3k
        # - else, crawl paths using our own logic, in reverse order to get correct precedence
        for pkg_root in _compute_package_paths(self._ros_root, self._ros_package_path):
            list_packages_by_path(pkg_root, cache)
    
    def list_packages(self):
        """
        List ROS packages.

        @return: complete list of package names in ROS environment
        @rtype: [str]
        """
        self._update_package_cache()
        return self._package_cache.keys()

    def get_path(self, package):
        """
        @param package: package name
        @type  package: str
        @return: filesystem path of package
        @raise PackageNotFound
        """
        self._update_package_cache()
        if not package in self._package_cache:
            raise PackageNotFound(package)
        else:
            return self._package_cache[package]
        
    def _load_manifest(self, package):
        """
        @raise PackageNotFound
        @raise InvalidPackage
        """
        # TODO: move manifestlib code in
        import roslib.manifest
        manifest_path = os.path.join(self.get_path(package), MANIFEST_FILE)
        retval = self._manifests[package] = roslib.manifest.parse_file(manifest_path)
        return retval
        
    def get_direct_depends(self, package):
        """
        Get the explicit dependencies of a package.
        
        @param package: package name
        @type  package: str
        @return: list of package names of direct dependencies
        @rtype: str
        @raise PackageNotFound
        @raise InvalidPackage
        """
        m = self.get_manifest(package)
        return [d.package for d in m.depends]

    def _invalidate_cache(self):
        self._rospack_cache.clear()

    def get_depends(self, package):
        """
        Get explicit and implicit dependencies of a package.

        @param package: package name
        @type  package: str
        @return: list of package names of dependencies.
        @rtype: [str]
        """
        if package in self._depends_cache:
            return self._depends_cache[package]

        # assign key before recursive call to prevent infinite case
        self._depends_cache[package] = s = set()
        
        # take the union of all dependencies
        packages = [p.package for p in self.get_manifest(package).depends]
        for p in packages:
            s.update(self.get_depends(p))
        # add in our own deps
        s.update(packages)
        # cache the return value as a list
        s = list(s)
        self._depends_cache[package] = s
        return s
    
    def rosdeps0(self, packages):
        """
        Collect rosdeps of specified packages into a dictionary.
        @param packages: package names
        @type  packages: [str]
        @return: dictionary mapping package names to list of rosdep names.
        @rtype: {str: [str]}
        """

        self.load_manifests(packages)
        map = {}
        manifests = self.manifests
        for pkg in packages:
            map[pkg] = [d.name for d in manifests[pkg].rosdeps]
        return map
        
    def rosdeps(self, packages):
        """
        Collect all (recursive) dependencies of specified packages
        into a dictionary.
        
        @param packages: package names
        @type  packages: [str]
        @return: dictionary mapping package names to list of dependent package names.
        @rtype: {str: [str]}
        """

        self.load_manifests(packages)
        map = {}
        for pkg in packages:
            if pkg in self._rosdeps_cache:
                map[pkg] = self._rosdeps_cache[pkg]
            else:
                # this will cache for future reference
                map[pkg] = self._rosdeps(pkg)
        return map

    def _rosdeps(self, package):
        """
        Compute recursive rosdeps of a single package and cache the
        result in self._rosdeps_cache.

        This is an internal routine. It assumes that
        load_manifests() has already been invoked for package.
        
        @param package: package name
        @type  package: str
        @return: list of rosdeps
        @rtype: [str]
        """

        if package in self._rosdeps_cache:
            return self._rosdeps_cache[package]
        # set the key before recursive call to prevent infinite case
        self._rosdeps_cache[package] = s = set()

        manifests = self.manifests
        # take the union of all dependencies
        pkgs = [p.package for p in manifests[package].depends]
        self.load_manifests(pkgs)
        for p in pkgs:
            s.update(self._rosdeps(p))
        # add in our own deps
        s.update([d.name for d in manifests[package].rosdeps])
        # cache the return value as a list
        s = list(s)
        self._rosdeps_cache[package] = s
        return s
        

