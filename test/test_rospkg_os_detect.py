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

class TestOs():
    def is_os(self):
        return True
    def get_version(self):
        return "os_version"

class DummyOs(object):
    def is_os(self):
        return False
    def get_version(self):
        return "os_version2"

def test__read_stdout():
    from rospkg.os_detect import _read_stdout
    assert 'hello' == _read_stdout(['echo', 'hello'])
    assert None == _read_stdout(['bad-command-input-for-rospkg-os-detect'])

def test_tripwire_ubuntu():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('ubuntu')
    
def test_ubuntu():
    import rospkg.os_detect
    from rospkg.os_detect import LsbDetect, OsDetect, OsNotDetected
    test_dir = os.path.join(get_test_dir(), 'ubuntu')
    rospkg.os_detect._lsb_release = os.path.join(test_dir, 'lsb_release')
    detect = OsDetect().get_detector('ubuntu')
    assert detect.is_os()
    assert detect.get_version() == 'lucid'

    # test freely
    if not detect.is_os():
        try:
            detect.get_version()
            assert False
        except OsNotDetected: pass

def test_tripwire_debian():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('debian')

def test_tripwire_osx():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('osx')
    
def test_osx():
    from rospkg.os_detect import OSX, _osx_codename, OsNotDetected
    test_dir = os.path.join(get_test_dir(), 'osx')
    detect = OSX(os.path.join(test_dir, "sw_vers"))
    assert detect.is_os()
    assert detect.get_codename() == 'snow'
    assert detect.get_version() == '10.6.5', detect.get_version()

    # trigger bad version number detect
    detect = OSX(os.path.join(test_dir, "sw_vers_bad"))
    assert detect.is_os()
    try:
        detect.get_codename()
        assert False
    except OsNotDetected: pass

    # regression test codename mapping
    assert 'lion' == _osx_codename(10, 7)
    try:
        _osx_codename(9, 7)
        assert False
    except OsNotDetected: pass

def test_tripwire_arch():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('arch')

def test_arch():
    from rospkg.os_detect import Arch, OsNotDetected
    test_dir = os.path.join(get_test_dir(), 'arch')
    detect = Arch(os.path.join(test_dir, "arch-release"))
    assert detect.is_os()
    assert detect.get_version() == ''

    detect = Arch()
    if not detect.is_os():
        try:
            detect.get_version()
            assert False
        except OsNotDetected: pass

def test_tripwire_opensuse():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('opensuse')

def test_opensuse():
    from rospkg.os_detect import OpenSuse, OsNotDetected
    test_dir = os.path.join(get_test_dir(), 'opensuse')
    detect = OpenSuse(os.path.join(test_dir, "SuSE-brand"))
    assert detect.is_os()
    assert detect.get_version() == '11.2'

    detect = OpenSuse()
    if not detect.is_os():
        try:
            detect.get_version()
            assert False
        except OsNotDetected: pass

def test_tripwire_gentoo():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('gentoo')

def test_gentoo():
    from rospkg.os_detect import Gentoo, OsNotDetected
    test_dir = os.path.join(get_test_dir(), 'gentoo')
    detect = Gentoo(os.path.join(test_dir, "gentoo-release"))
    assert detect.is_os()
    assert detect.get_version() == '2.0.1'

    detect = Gentoo()
    if not detect.is_os():
        try:
            detect.get_version()
            assert False
        except OsNotDetected: pass

def test_tripwire_fedora():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('fedora')

def get_test_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'os_detect'))

def test_fedora():
    from rospkg.os_detect import Fedora, OsNotDetected
    test_dir = os.path.join(get_test_dir(), 'fedora')
    release_file, issue_file = [os.path.join(test_dir, x) for x in ["redhat-release", "issue"]]
    detect = Fedora(release_file, issue_file)
    assert detect.is_os()
    assert detect.get_version() == '1'
    
    detect = Fedora()
    if not detect.is_os():
        try:
            detect.get_version()
            assert False
        except OsNotDetected: pass

def test_read_issue():
    from rospkg.os_detect import read_issue
    assert read_issue('/fake/file') == None
    test_dir = os.path.join(get_test_dir(), 'rhel')
    assert read_issue(os.path.join(test_dir, 'issue')) == ['Red', 'Hat', 'Enterprise', 'Linux', 'AS', 'release', '3', '(Taroon)']
    
def test_OsDetector():
    from rospkg.os_detect import OsDetector
    d = OsDetector()
    try:
        d.is_os()
        assert False
    except NotImplementedError: pass
    try:
        d.get_version()
        assert False
    except NotImplementedError: pass
    
def test_tripwire_lsb_get_version():
    # value is platform dependent, so just make sure it doesn't throw
    from rospkg.os_detect import lsb_get_version
    retval = lsb_get_version()
    assert retval == None or type(retval) == str
    
def test_tripwire_lsb_get_codename():
    # value is platform dependent, so just make sure it doesn't throw
    from rospkg.os_detect import lsb_get_codename
    retval = lsb_get_codename()
    assert retval == None or type(retval) == str

def test_tripwire_uname_get_machine():
    from rospkg.os_detect import uname_get_machine
    retval = uname_get_machine()
    assert retval in [None, 'i386', 'x86_64']

def test_tripwire_rhel():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('rhel')

def test_redhat():
    from rospkg.os_detect import Rhel, OsNotDetected
    test_dir = os.path.join(get_test_dir(), 'rhel')

    # go through several test files
    detect = Rhel(os.path.join(test_dir, "redhat-release"))
    assert detect.is_os()
    assert detect.get_version() == '3'
    assert detect.get_codename() == 'taroon'
    
    detect = Rhel(os.path.join(test_dir, "redhat-release-pensacola"))
    assert detect.is_os()
    assert detect.get_version() == '2.1AS', detect.get_version()
    assert detect.get_codename() == 'pensacola'
    
    detect = Rhel(os.path.join(test_dir, "redhat-release-tikanga"))
    assert detect.is_os()
    assert detect.get_version() == '5'
    assert detect.get_codename() == 'tikanga'

    detect = Rhel(os.path.join(test_dir, "redhat-release-nahant"))
    assert detect.is_os()
    assert detect.get_version() == '4'
    assert detect.get_codename() == 'nahant'

    # test freely
    detect = Rhel()
    if not detect.is_os():
        try:
            detect.get_version()
            assert False
        except OsNotDetected: pass
    
def test_tripwire_freebsd():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('freebsd')

def test_freebsd():
    from rospkg.os_detect import FreeBSD, OsNotDetected
    #TODO
    if 0:
        test_dir = os.path.join(get_test_dir(), 'freebsd')
        release_file, issue_file = [os.path.join(test_dir, x) for x in ["redhat-release", "issue"]]
        detect = FreeBSD(release_file, issue_file)
        assert detect.is_os()
        assert detect.get_version() == '3'
        
    # test freely
    detect = FreeBSD()
    if not detect.is_os():
        try:
            detect.get_version()
            assert False
        except OsNotDetected: pass

    # assure failure
    detect = FreeBSD("/fake/uname/file")
    assert not detect.is_os()
    try:
        detect.get_version()
        assert False
    except OsNotDetected: pass
    
def test_cygwin():
    from rospkg.os_detect import Cygwin, OsNotDetected
    #TODO
    detect = Cygwin()
    if not detect.is_os():
        try:
            detect.get_version()
            assert False
        except OsNotDetected: pass
    
def test_OsDetect():
    from rospkg.os_detect import OsDetect    
    detect = OsDetect()
    try:
        detect.get_detector('fake')
        assert False, "should raise"
    except KeyError: pass
    
def test_OsDetect_single():
    from rospkg.os_detect import OsDetect    
    detect = OsDetect([('TestOs', TestOs())])
    assert "TestOs" == detect.get_name()
    assert "TestOs" == detect.get_name()
    detect = OsDetect([('TestOs', TestOs())])
    assert "os_version" == detect.get_version()
    assert "os_version" == detect.get_version()
    
    detect = OsDetect([('TestOs', TestOs())])
    assert isinstance(detect.get_detector(), TestOs)
    assert isinstance(detect.get_detector('TestOs'), TestOs)

def test_OsDetect_nomatch():
    from rospkg.os_detect import OsDetect, OsNotDetected
    detect = OsDetect([('Dummy', DummyOs())])
    assert isinstance(detect.get_detector('Dummy'), DummyOs)
    try:
        detect.get_name()
        assert False
    except OsNotDetected: pass
    try:
        detect.get_version()
        assert False
    except OsNotDetected: pass
    try:
        detect.get_detector()
        assert False
    except OsNotDetected: pass
    

def xTestOsDetect_first_of_two():
    osa = roslib.os_detect.OSDetect([TestOs(), DummyOs()])
    assert "os_name" == osa.get_name()
    assert "os_version" == osa.get_version()
    os_class = osa.get_os()
    assert "os_name" == os_class.get_name()
    assert "os_version" == os_class.get_version()

def xTestOsDetect_second_of_two():
    osa = roslib.os_detect.OSDetect([DummyOs(), TestOs()])
    assert "os_name", osa.get_name()
    assert "os_version", osa.get_version()
    os_class = osa.get_os()
    assert "os_name" == os_class.get_name()
    assert "os_version" == os_class.get_version()

def xTestOsDetect_first_of_many():
    osa = roslib.os_detect.OSDetect([TestOs(), DummyOs(), DummyOs(), DummyOs(), DummyOs()])
    assert "os_name" == osa.get_name()
    assert "os_version" == osa.get_version()
    os_class = osa.get_os()
    assert "os_name" == os_class.get_name()
    assert "os_version" == os_class.get_version()

def xTestOsDetect_second_of_many():
    osa = roslib.os_detect.OSDetect([DummyOs(), TestOs(), DummyOs(), DummyOs(), DummyOs()])
    assert "os_name" == osa.get_name()
    assert "os_version" == osa.get_version()
    os_class = osa.get_os()
    assert "os_name" == os_class.get_name()
    assert "os_version" == os_class.get_version()

def xTestOsDetect_last_of_many():
    osa = roslib.os_detect.OSDetect([DummyOs(), DummyOs(), DummyOs(), DummyOs(), TestOs(),])
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
