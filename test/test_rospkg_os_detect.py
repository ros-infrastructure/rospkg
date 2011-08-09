# Software License Agreement (BSD License)
#
# Copyright (c) 2009, Willow Garage, Inc.
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

import os
import sys
import unittest

class test_OS():
    def check_presence(self):
        return True
    def get_version(self):
        return "os_version"

class dummy_OS(object):
    def check_presence(self):
        return False
    def get_version(self):
        return "os_version2"

def test_tripwire_ubuntu():
    from rospkg import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('ubuntu')
    
def test_ubuntu():
    import rospkg.os_detect
    from rospkg.os_detect import LsbDetect, OsDetect
    test_dir = os.path.join(get_test_dir(), 'ubuntu')
    rospkg.os_detect._lsb_release = os.path.join(test_dir, 'lsb_release')
    detect = OsDetect().get_detector('ubuntu')
    assert detect.is_os()
    assert detect.get_version() == 'lucid'

def test_tripwire_debian():
    from rospkg import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('debian')

def test_tripwire_osx():
    from rospkg import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('osx')
    
def test_osx():
    from rospkg.os_detect import OSX
    test_dir = os.path.join(get_test_dir(), 'osx')
    detect = OSX(os.path.join(test_dir, "sw_vers"))
    assert detect.is_os()
    assert detect.get_version() == 'snow'

def test_tripwire_arch():
    from rospkg import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('arch')

def test_arch():
    from rospkg.os_detect import Arch
    test_dir = os.path.join(get_test_dir(), 'arch')
    detect = Arch(os.path.join(test_dir, "arch-release"))
    assert detect.is_os()
    assert detect.get_version() == ''

def test_tripwire_opensuse():
    from rospkg import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('opensuse')

def test_opensuse():
    from rospkg.os_detect import OpenSuse
    test_dir = os.path.join(get_test_dir(), 'opensuse')
    detect = OpenSuse(os.path.join(test_dir, "SuSE-brand"))
    assert detect.is_os()
    assert detect.get_version() == '11.2'

def test_tripwire_gentoo():
    from rospkg import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('gentoo')

def test_gentoo():
    from rospkg.os_detect import Gentoo
    test_dir = os.path.join(get_test_dir(), 'gentoo')
    detect = Gentoo(os.path.join(test_dir, "gentoo-release"))
    assert detect.is_os()
    assert detect.get_version() == '2.0.1'

def test_tripwire_fedora():
    from rospkg import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('fedora')

def get_test_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'os_detect'))

def test_fedora():
    from rospkg.os_detect import Fedora
    test_dir = os.path.join(get_test_dir(), 'fedora')
    release_file, issue_file = [os.path.join(test_dir, x) for x in ["redhat-release", "issue"]]
    detect = Fedora(release_file, issue_file)
    assert detect.is_os()
    assert detect.get_version() == '1'
    
def test_tripwire_rhel():
    from rospkg import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('rhel')

def test_redhat():
    from rospkg.os_detect import Rhel
    test_dir = os.path.join(get_test_dir(), 'rhel')
    release_file, issue_file = [os.path.join(test_dir, x) for x in ["redhat-release", "issue"]]
    detect = Rhel(release_file, issue_file)
    assert detect.is_os()
    assert detect.get_version() == '3'
    
def xtest_OSDetect_single():
    osa = roslib.os_detect.OSDetect([test_OS()])
    assert "os_name" == osa.get_name()
    assert "os_version" == osa.get_version()

def xtest_OSDetect_first_of_two():
    osa = roslib.os_detect.OSDetect([test_OS(), dummy_OS()])
    assert "os_name" == osa.get_name()
    assert "os_version" == osa.get_version()
    os_class = osa.get_os()
    assert "os_name" == os_class.get_name()
    assert "os_version" == os_class.get_version()

def xtest_OSDetect_second_of_two():
    osa = roslib.os_detect.OSDetect([dummy_OS(), test_OS()])
    assert "os_name", osa.get_name()
    assert "os_version", osa.get_version()
    os_class = osa.get_os()
    assert "os_name" == os_class.get_name()
    assert "os_version" == os_class.get_version()

def xtest_OSDetect_first_of_many():
    osa = roslib.os_detect.OSDetect([test_OS(), dummy_OS(), dummy_OS(), dummy_OS(), dummy_OS()])
    assert "os_name" == osa.get_name()
    assert "os_version" == osa.get_version()
    os_class = osa.get_os()
    assert "os_name" == os_class.get_name()
    assert "os_version" == os_class.get_version()

def xtest_OSDetect_second_of_many():
    osa = roslib.os_detect.OSDetect([dummy_OS(), test_OS(), dummy_OS(), dummy_OS(), dummy_OS()])
    assert "os_name" == osa.get_name()
    assert "os_version" == osa.get_version()
    os_class = osa.get_os()
    assert "os_name" == os_class.get_name()
    assert "os_version" == os_class.get_version()

def xtest_OSDetect_last_of_many():
    osa = roslib.os_detect.OSDetect([dummy_OS(), dummy_OS(), dummy_OS(), dummy_OS(), test_OS(),])
    assert "os_name", osa.get_name()
    assert "os_version", osa.get_version()
    os_class = osa.get_os()
    assert "os_name" == os_class.get_name()
    assert "os_version" == os_class.get_version()

def xtest_ubuntu_in_OSA():
    ubuntu = roslib.os_detect.Ubuntu()
    def return_true():
        return True
    ubuntu.check_presence = return_true
    osa = roslib.os_detect.OSDetect([ubuntu])
    assert "ubuntu" == ubuntu.get_name()
    os_class = osa.get_os()
    assert "ubuntu" == os_class.get_name()
