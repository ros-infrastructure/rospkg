#!/usr/bin/env python
# Copyright (c) 2009, Willow Garage, Inc.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Willow Garage, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Author Tully Foote/tfoote@willowgarage.com, Ken Conley/kwc@willowgarage.com

"""
Library for detecting the current OS, including detecting specific
Linux distributions. 
"""

from __future__ import print_function

import os
import sys
import subprocess

def _read_stdout(cmd):
    try:
        pop = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (std_out, std_err) = pop.communicate()
        return std_out.strip()
    except:
        return None
    
# for test mocking
_lsb_release = 'lsb_release'

def lsb_get_os():
    """
    Linux: wrapper around lsb_release to get the current OS
    """
    return _read_stdout([_lsb_release, '-si'])
    
def lsb_get_codename():
    """
    Linux: wrapper around lsb_release to get the current OS codename
    """
    return _read_stdout([_lsb_release, '-sc'])
    
def lsb_get_version():
    """
    Linux: wrapper around lsb_release to get the current OS version
    """
    return _read_stdout([_lsb_release, '-sr'])

def uname_get_machine():
    """
    Linux: wrapper around uname to determine if OS is 64-bit
    """
    return _read_stdout(['uname', '-m'])

def read_issue(filename="/etc/issue"):
    """
    :returns: list of strings in issue file, or None if issue file cannot be read/split
    """
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return f.read().split()
    return None

class OsNotDetected(Exception):
    """
    Exception to indicate failure to detect operating system.
    """
    pass

class OsDetector:
    """
    Generic API for detecting a specific OS.
    """
    def is_os(self):
        """
        :returns: if the specific OS which this class is designed to
          detect is present.  Only one version of this class should
          return for any version.
        """
        raise NotImplementedError("is_os unimplemented")

    def get_version(self):
        """
        :returns: standardized version for this OS. (ala Ubuntu Hardy Heron = "8.04")
        :raises: :exc:`OsNotDetected` if called on incorrect OS.
        """
        raise NotImplementedError("get_version unimplemented")

    def get_codename(self):
        """
        :returns: codename for this OS. (ala Ubuntu Hardy Heron = "hardy").  If codenames are not available for this OS, return empty string.
        :raises: :exc:`OsNotDetected` if called on incorrect OS.
        """
        raise NotImplementedError("get_codename unimplemented")

class LsbDetect(OsDetector):
    """
    Generic detector for Debian, Ubuntu, and Mint
    """
    def __init__(self, lsb_name, get_version_fn=None):
        self.lsb_name = lsb_name

    def is_os(self):
        return lsb_get_os() == self.lsb_name

    def get_version(self):
        if self.is_os():
            return lsb_get_version()
        raise OsNotDetected('called in incorrect OS')
        
    def get_codename(self):
        if self.is_os():
            return lsb_get_codename()
        raise OsNotDetected('called in incorrect OS')

class OpenSuse(OsDetector):
    """
    Detect OpenSuse OS.
    """
    def __init__(self, brand_file="/etc/SuSE-brand"):
        self._brand_file = brand_file
        
    def is_os(self):
        os_list = read_issue(self._brand_file)
        return os_list and os_list[0] == "openSUSE"

    def get_version(self):
        if self.is_os() and os.path.exists(self._brand_file):
            with open(self._brand_file, 'r') as fh:
                os_list = fh.read().strip().split('\n')
                if len(os_list) == 2:
                    os_list = os_list[1].split(' = ')
                    if os_list[0] == "VERSION":
                        return os_list[1]
        raise OsNotDetected('cannot get version on this OS')

class Fedora(OsDetector):
    """
    Detect Fedora OS.
    """
    def __init__(self, release_file="/etc/redhat-release", issue_file="/etc/issue"):
        self._release_file = release_file
        self._issue_file = issue_file
        
    def is_os(self):
        os_list = read_issue(self._release_file)
        return os_list and os_list[0] == "Fedora" 

    def get_version(self):
        if self.is_os():
            os_list = read_issue(self._issue_file)
            idx = os_list.index('release')
            if idx > 0:
                return os_list[idx+1]
        raise OsNotDetected('cannot get version on this OS')

class Rhel(Fedora):
    """
    Detect Redhat OS.
    """
    def __init__(self, release_file="/etc/redhat-release"):
        self._release_file = release_file

    def is_os(self):
        os_list = read_issue(self._release_file)
        return os_list and os_list[:3] == ['Red', 'Hat', 'Enterprise']

    def get_version(self):
        if self.is_os():
            os_list = read_issue(self._release_file)
            idx = os_list.index('release')
            return os_list[idx+1]
        raise OsNotDetected('called in incorrect OS')

    def get_codename(self):
        # taroon, nahant, tikanga, santiago, pensacola
        if self.is_os():
            os_list = read_issue(self._release_file)
            idx = os_list.index('release')
            matches = [x for x in os_list if x[0] == '(']
            codename = matches[0][1:]
            if codename[-1] == ')':
                codename = codename[:-1]
            return codename.lower()
        raise OsNotDetected('called in incorrect OS')
    
# Source: http://en.wikipedia.org/wiki/Mac_OS_X#Versions
_osx_codename_map = {4: 'tiger',
                     5:  'leopard',
                     6: 'snow',
                     7: 'lion'}
def _osx_codename(major, minor):
    if major != 10 or minor not in _osx_codename_map:
        raise OsNotDetected("unrecognized version: %s.%s"%(major, minor))
    return _osx_codename_map[minor]
    
class OSX(OsDetector):
    """
    Detect OS X 
    """
    def __init__(self, sw_vers_file="/usr/bin/sw_vers"):
        self._sw_vers_file = sw_vers_file

    def is_os(self):
        return os.path.exists(self._sw_vers_file)
    
    def get_codename(self):
        if self.is_os():
            version = self.get_version()
            import distutils.version # To parse version numbers
            try:
                ver = distutils.version.StrictVersion(version).version
            except ValueError:
                raise OsNotDetected("invalid version string: %s"%(version))
            return _osx_codename(*ver[0:2])
        raise OsNotDetected('called in incorrect OS')
        
    def get_version(self):
        if self.is_os():
            return _read_stdout([self._sw_vers_file,'-productVersion']).strip()
        raise OsNotDetected('called in incorrect OS')

class Arch(OsDetector):
    """
    Detect Arch Linux.
    """
    def __init__(self, release_file='/etc/arch-release'):
        self._release_file = release_file

    def is_os(self):
        return os.path.exists(self._release_file)

    def get_version(self):
        if self.is_os():
            return ""
        raise OsNotDetected('called in incorrect OS')        

    def get_codename(self):
        if self.is_os():
            return ""
        raise OsNotDetected('called in incorrect OS')        

class Cygwin(OsDetector):
    """
    Detect Cygwin presence on Windows OS.
    """
    def is_os(self):
        return os.path.exists("/usr/bin/cygwin1.dll")
    
    def get_version(self):
        if self.is_os():
            return _read_stdout(['uname','-r'])
        raise OsNotDetected('called in incorrect OS')        

    def get_codename(self):
        if self.is_os():
            return ''
        raise OsNotDetected('called in incorrect OS')        

class Gentoo(OsDetector):
    """
    Detect Gentoo OS.
    """
    def __init__(self, release_file="/etc/gentoo-release"):
        self._release_file = release_file

    def is_os(self):
        os_list = read_issue(self._release_file)
        return os_list and os_list[0] == "Gentoo" and os_list[1] == "Base"

    def get_version(self):
        if self.is_os():
            os_list = read_issue(self._release_file)
            if os_list[0] == "Gentoo" and os_list[1] == "Base":
                return os_list[4]
        raise OsNotDetected('called in incorrect OS')        

    def get_codename(self):
        if self.is_os():
            return ''
        raise OsNotDetected('called in incorrect OS')        

class FreeBSD(OsDetector):
    """
    Detect FreeBSD OS.
    """
    def __init__(self, uname_file="/usr/bin/uname"):
        self._uname_file = uname_file

    def is_os(self):
        if os.path.exists(self._uname_file):
            std_out = _read_stdout([self._uname_file])
            return std_out.strip() == "FreeBSD"
        else:
            return False

    def get_version(self):
        if self.is_os() and os.path.exists(self._uname_file):
            return _read_stdout([self._uname_file, "-r"])
        raise OsNotDetected('called in incorrect OS')        

    def get_codename(self):
        if self.is_os():
            return ''
        raise OsNotDetected('called in incorrect OS')        

class OsDetect:
    """
    This class will iterate over registered classes to lookup the
    active OS and version
    """

    default_os_list = []
    
    def __init__(self, os_list = None):
        if os_list is None:
            os_list = OsDetect.default_os_list
        self._os_list = os_list
        self._os_name = None
        self._os_version = None
        self._os_codename = None
        self._os_detector = None
        self._override = False

    @staticmethod
    def register_default(os_name, os_detector):
        """
        Register detector to be used with all future instances of
        :class:`OsDetect`.  The new detector will have precedence over
        any previously registered detectors associated with *os_name*.

        :param os_name: OS key associated with OS detector
        :param os_detector: :class:`OsDetector` instance
        """
        OsDetect.default_os_list.insert(0, (os_name, os_detector))
        
    def detect_os(self, env=None):
        """
        Detect operating system.  Return value can be overridden by
        the :env:`ROS_OS_OVERRIDE` environment variable.
        
        :param env: override ``os.environ``
        :returns: (os_name, os_version, os_codename), ``(str, str, str)``
        :raises: :exc:`OsNotDetected` if OS could not be detected
        """
        if env is None:
            env = os.environ
        if 'ROS_OS_OVERRIDE' in env:
            splits = env["ROS_OS_OVERRIDE"].split(':')
            self._os_name = splits[0]
            if len(splits) > 1:
                self._os_version = splits[1]
                if len(splits) > 2:
                    self._os_codename = splits[2]
                else:
                    self._os_codename = ''
            else:
                self._os_version = self._os_codename = ''  
            self._override = True
        else:
            for os_name, os_detector in self._os_list:
                if os_detector.is_os():
                    self._os_name = os_name
                    self._os_version = os_detector.get_version()
                    self._os_codename = os_detector.get_codename()
                    self._os_detector = os_detector

        if self._os_name:
            return self._os_name, self._os_version, self._os_codename
        else: # No solution found
            attempted = [x[0] for x in self._os_list]
            raise OsNotDetected("Could not detect OS, tried %s"%attempted)

    def get_detector(self, name=None):
        """
        Get detector used for specified OS name, or the detector for this OS if name is ``None``.
        
        :raises: :exc:`KeyError`
        """
        if name is None:
            if not self._os_detector:
                self.detect_os()
            return self._os_detector
        else:
            try:
                return [d for d_name, d in self._os_list if d_name == name][0]
            except IndexError:
                raise KeyError(name)
        
    def add_detector(self, name, detector):
        """
        Add detector to list of detectors used by this instance.  *detector* will override any previous
        detectors associated with *name*.

        :param name: OS name that detector matches
        :param detector: :class:`OsDetector` instance
        """
        self._os_list.insert(0, (name, detector))

    def get_name(self):
        if not self._os_name:
            self.detect_os()
        return self._os_name

    def get_version(self):
        if not self._os_version:
            self.detect_os()
        return self._os_version

    def get_codename(self):
        if not self._os_codename:
            self.detect_os()
        return self._os_codename

OS_ARCH='arch'
OS_CYGWIN='cygwin'
OS_DEBIAN='debian'
OS_FEDORA='fedora'
OS_FREEBSD='freebsd'
OS_GENTOO='gentoo'
OS_MINT='mint'
OS_OPENSUSE='opensuse'
OS_OSX='osx'
OS_RHEL='rhel'
OS_UBUNTU='ubuntu'

OsDetect.register_default(OS_ARCH, Arch())
OsDetect.register_default(OS_CYGWIN, Cygwin())
OsDetect.register_default(OS_DEBIAN, LsbDetect("Debian"))
OsDetect.register_default(OS_FEDORA, Fedora())
OsDetect.register_default(OS_FREEBSD, FreeBSD())
OsDetect.register_default(OS_GENTOO, Gentoo())
OsDetect.register_default(OS_MINT, LsbDetect("Mint"))
OsDetect.register_default(OS_OPENSUSE, OpenSuse())
OsDetect.register_default(OS_OSX, OSX())
OsDetect.register_default(OS_RHEL, Rhel())
OsDetect.register_default(OS_UBUNTU, LsbDetect("Ubuntu"))
    

if __name__ == '__main__':
    detect = OsDetect()
    print("OS Name:     %s"%detect.get_name())
    print("OS Version:  %s"%detect.get_version())    
    print("OS Codename: %s"%detect.get_codename())    
