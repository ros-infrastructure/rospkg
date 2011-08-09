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

import os
import sys
import subprocess

####### Linux Helper Functions #####
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
    @return: list of strings in issue file, or None if issue file cannot be read/split
    """
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return f.read().split()
    except:
        pass
    return None

class OsNotDetected(Exception): pass

class OsDetector:
    """
    Generic API for detecting a specific OS.
    """
    def is_os(self):
        """
        @return: if the specific OS which this class is designed to
        detect is present.  Only one version of this class should
        return for any version.
        """
        raise NotImplemented("is_os unimplemented")

    def get_version(self):
        """
        @return: standardized version for this OS. (ala Ubuntu Hardy Heron = "8.04")
        """
        raise NotImplemented("get_version unimplemented")

class LsbDetect(OsDetector):
    """
    Generic detector for Debian, Ubuntu, Mint, and Mandriva
    """
    def __init__(self, lsb_name, get_version_fn):
        self.lsb_name = lsb_name
        self.get_version_fn = get_version_fn

    def is_os(self):
        return lsb_get_os() == self.lsb_name

    def get_version(self):
        return self.get_version_fn()
        
def mandriva_version():
    return lsb_get_version()+uname_get_machine()

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
        try:
            if os.path.exists(self._brand_file):
                with open(self._brand_file, 'r') as fh:
                    os_list = fh.read().strip().split('\n')
                    if len(os_list) == 2:
                        os_list = os_list[1].split(' = ')
                        if os_list[0] == "VERSION":
                            return os_list[1]
        except: pass
        return False

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
        os_list = read_issue(self._issue_file)
        idx = os_list.index('release')
        if idx > 0:
            return os_list[idx+1]
        else:
            return False

class Rhel(Fedora):
    """
    Detect Redhat OS.
    """
    def __init__(self, release_file="/etc/redhat-release", issue_file="/etc/issue"):
        self._release_file = release_file
        self._issue_file = issue_file

    def is_os(self):
        os_list = read_issue(self._release_file)
        return os_list and os_list[2] == "Enterprise"

    def get_version(self):
        os_list = read_issue(self._issue_file)
        if os_list[2] == "Enterprise":
            return os_list[6]
        else:
            raise OsNotDetected("cannot determine RHEL version")

class OSX(OsDetector):
    """
    Detect OS X 
    """
    def __init__(self, sw_vers_file="/usr/bin/sw_vers"):
        self._sw_vers_file = sw_vers_file

    def is_os(self):
        return os.path.exists(self._sw_vers_file)
    
    def get_version(self):
        import distutils.version # To parse version numbers
        # REP 111 this should be the code name (e.g., lion, snow, tiger) #3570
        std_out = _read_stdout([self._sw_vers_file,'-productVersion'])
        ver = distutils.version.StrictVersion(std_out).version
        if len(ver) < 2:
            raise OsNotDetected("invalid version string: %s"%(std_out))
        major, minor = ver[0:2]
        # Source: http://en.wikipedia.org/wiki/Mac_OS_X#Versions
        if major == 10 and minor == 4:
            return 'tiger'
        elif major == 10 and minor == 5:
            return 'leopard'
        elif major == 10 and minor == 6:
            return 'snow'
        elif major == 10 and minor == 7:
            return 'lion'
        else:
            raise OsNotDetected("unrecognized version: %s"%(std_out))

class Arch(OsDetector):
    """
    Detect Arch Linux.
    """
    def __init__(self, release_file='/etc/arch-release'):
        self._release_file = release_file

    def is_os(self):
        return os.path.exists(self._release_file)

    def get_version(self):
        return ""

class Cygwin(OsDetector):
    """
    Detect Cygwin presence on Windows OS.
    """
    def is_os(self):
        return os.path.exists("/usr/bin/cygwin1.dll")
    
    def get_version(self):
        return _read_stdout(['uname','-r'])

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
        os_list = read_issue(self._release_file)
        if os_list[0] == "Gentoo" and os_list[1] == "Base":
            return os_list[4]
        else:
            return False

class FreeBSD(OsDetector):
    """
    Detect FreeBSD OS.
    """
    def __init__(self, uname_file="/usr/bin/uname"):
        self._uname_file = uname_file

    def is_os(self):
        if os.path.exists(self._uname_file):
            std_out = _read_stdout([filename])
            return std_out.strip() == "FreeBSD"
        else:
            return False

    def get_version(self):
        try:
            if os.path.exists(self._uname_file):
               return _read_stdout([self._uname_file, "-r"])
            else:
               return False
        except: pass
        return False

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
        self._override = False

    @staticmethod
    def register_default(os_name, os_detector):
        OsDetect.default_os_list.append((os_name, os_detector))
        
    def detect_os(self):
        """
        @return: (os_name, os_version)
        @raise OsNotDetected: is OS could not be detected
        """
        if 'ROS_OS_OVERRIDE' in os.environ:
            self._os_name, self._os_version = os.environ["ROS_OS_OVERRIDE"].split(':')
            self._override = True
        else:
            for os_name, os_detector in self._os_list:
                if os_detector.is_os():
                    self._os_name = os_name
                    self._os_version = os_detector.get_version()

        if self._os_name:
            return (self._os_name, self._os_version)            
        else:
            # No solution found
            attempted_oss = [o.get_name() for o in self._os_list]
            raise OsNotDetected("Could not detect OS, tried %s"%attempted_oss)

    def get_detector(self, name):
        """
        Get detector used for specified OS name.
        @raises: KeyError
        """
        try:
            return [d for d_name, d in self._os_list if d_name == name][0]
        except IndexError:
            raise KeyError(name)
        
    def get_os(self):
        if not self._os_detector:
            self.detect_os()
        return self._os_detector

    def get_name(self):
        if not self._os_name:
            self.detect_os()
        return self._os_name

    def get_version(self):
        if not self._os_version:
            not self.detect_os()
        return self._os_version

OsDetect.register_default("debian", LsbDetect("Debian", lsb_get_codename))
OsDetect.register_default("ubuntu", LsbDetect("Ubuntu", lsb_get_codename))
OsDetect.register_default("mint", LsbDetect("Mint", lsb_get_version))
OsDetect.register_default("mandriva", LsbDetect("MandrivaLinux", mandriva_version))
OsDetect.register_default("osx", OSX())
OsDetect.register_default("arch", Arch())
OsDetect.register_default("opensuse", OpenSuse())
OsDetect.register_default("fedora", Fedora())
OsDetect.register_default("rhel", Rhel())
OsDetect.register_default("gentoo", Gentoo())
OsDetect.register_default("cygwin", Cygwin())
OsDetect.register_default("freebsd", FreeBSD())
    
