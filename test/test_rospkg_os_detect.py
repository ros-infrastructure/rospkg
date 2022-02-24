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

from __future__ import absolute_import

import os

try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch


class TrueOs():
    def is_os(self):
        return True

    def get_version(self):
        return "os_version"

    def get_codename(self):
        return "os_codename"


class TrueOs2():
    def is_os(self):
        return True

    def get_version(self):
        return "os_version"

    def get_codename(self):
        return "os_codename"


class FalseOs(object):
    def is_os(self):
        return False

    def get_version(self):
        return "os_version2"

    def get_codename(self):
        return "os_codename"


def test__read_stdout():
    from rospkg.os_detect import _read_stdout
    assert 'hello' == _read_stdout(['echo', 'hello'])
    assert _read_stdout(['bad-command-input-for-rospkg-os-detect']) is None


def test_tripwire_ubuntu():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('ubuntu')


def test_LsbDetect():
    from rospkg.os_detect import LsbDetect, OsNotDetected

    # test non-match
    detect = LsbDetect('bad')
    assert not detect.is_os()
    try:
        detect.get_version()
        assert False
    except OsNotDetected:
        pass
    try:
        detect.get_codename()
        assert False
    except OsNotDetected:
        pass

    # test match
    # to be removed after Ubuntu Xenial is out of support
    import sys
    if sys.version_info >= (3, 8):
        import distro
    else:
        import platform as distro

    # Mock different interfaces based on the module used.
    if distro.__name__ == 'distro':
        distro.id = Mock()
        distro.id.return_value = 'Ubuntu'
        distro.version = Mock()
        distro.version.return_value = '10.04'
        distro.codename = Mock()
        distro.codename.return_value = 'lucid'
    elif hasattr(distro, 'linux_distribution'):
        distro.linux_distribution = Mock()
        distro.linux_distribution.return_value = ('Ubuntu', '10.04', 'lucid')
    elif hasattr(distro, 'dist'):
        distro.dist = Mock()
        distro.dist.return_value = ('Ubuntu', '10.04', 'lucid')

    detect = LsbDetect('Ubuntu')
    assert detect.is_os(), "should be Ubuntu"
    assert detect.get_codename() == 'lucid', detect.get_codename()

    # test freely
    if not detect.is_os():
        try:
            detect.get_version()
            assert False
        except OsNotDetected:
            pass


def test_ubuntu():
    from rospkg.os_detect import OsDetect, OsNotDetected

    os_detector = OsDetect()
    detect = os_detector.get_detector('ubuntu')
    detect.lsb_info = ('Ubuntu', '10.04', 'lucid')

    assert detect.get_version() == '10.04', detect.get_version()
    assert detect.get_codename() == 'lucid', detect.get_codename()

    # test freely
    if not detect.is_os():
        try:
            detect.get_version()
            assert False
        except OsNotDetected:
            pass
        try:
            detect.get_codename()
            assert False
        except OsNotDetected:
            pass


def test_tripwire_debian():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('debian')


def test_tripwire_osx():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('osx')


def test_osx():
    if 'posix' != os.name:
        from unittest.case import SkipTest
        raise SkipTest('Test requires POSIX platform, not "{}"'.format(os.name))

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
    except OsNotDetected:
        pass

    # regression test codename mapping
    assert 'lion' == _osx_codename(10, 7)
    try:
        _osx_codename(9, 7)
        assert False
    except OsNotDetected:
        pass


def test_osx_patched():
    from rospkg.os_detect import OSX, OsNotDetected

    @patch.object(OSX, 'is_os')
    def test(mock):
        mock.return_value = False
        detect = OSX()
        try:
            detect.get_codename()
            assert False
        except OsNotDetected:
            pass
        try:
            detect.get_version()
            assert False
        except OsNotDetected:
            pass
    test()


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
        except OsNotDetected:
            pass
        try:
            detect.get_codename()
            assert False
        except OsNotDetected:
            pass

    @patch.object(Arch, 'is_os')
    def test(mock):
        mock.is_os.return_value = True
        detect = Arch()
        assert detect.get_version() == ''
        assert detect.get_codename() == ''
    test()


def test_tripwire_manjaro():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('manjaro')


def test_manjaro():
    from rospkg.os_detect import Manjaro, OsNotDetected
    test_dir = os.path.join(get_test_dir(), 'manjaro')
    detect = Manjaro(os.path.join(test_dir, "manjaro-release"))
    assert detect.is_os()
    assert detect.get_version() == ''

    detect = Manjaro()
    if not detect.is_os():
        try:
            detect.get_version()
            assert False
        except OsNotDetected:
            pass
        try:
            detect.get_codename()
            assert False
        except OsNotDetected:
            pass

    @patch.object(Manjaro, 'is_os')
    def test(mock):
        mock.is_os.return_value = True
        detect = Manjaro()
        assert detect.get_version() == ''
        assert detect.get_codename() == ''
    test()


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
        except OsNotDetected:
            pass


def test_opensuse13():
    from rospkg.os_detect import OpenSuse, OsNotDetected
    test_dir = os.path.join(get_test_dir(), 'opensuse13')
    detect = OpenSuse(os.path.join(test_dir, "SUSE-brand"))
    assert detect.is_os()
    assert detect.get_version() == '13.1'

    detect = OpenSuse()
    if not detect.is_os():
        try:
            detect.get_version()
            assert False
        except OsNotDetected:
            pass


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
    assert detect.get_codename() == ''

    # test freely
    detect = Gentoo()
    if not detect.is_os():
        try:
            detect.get_version()
            assert False
        except OsNotDetected:
            pass
        try:
            detect.get_codename()
            assert False
        except OsNotDetected:
            pass


def test_tripwire_fedora():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('fedora')


def get_test_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        'os_detect'))


def test_read_issue():
    from rospkg.os_detect import read_issue
    assert read_issue('/fake/file') is None
    test_dir = os.path.join(get_test_dir(), 'rhel')
    assert read_issue(os.path.join(test_dir, 'issue')) == \
        ['Red', 'Hat', 'Enterprise', 'Linux', 'AS', 'release', '3', '(Taroon)']


def test_OsDetector():
    from rospkg.os_detect import OsDetector
    d = OsDetector()
    try:
        d.is_os()
        assert False
    except NotImplementedError:
        pass
    try:
        d.get_version()
        assert False
    except NotImplementedError:
        pass
    try:
        d.get_codename()
        assert False
    except NotImplementedError:
        pass


def test_tripwire_uname_get_machine():
    from rospkg.os_detect import uname_get_machine
    retval = uname_get_machine()
    assert retval in [None, 'aarch64', 'armv7l', 'armv8l', 'i386', 'i686', 'ppc', 'ppc64', 'ppc64le', 'riscv32', 'riscv64', 's390', 's390x', 'x86_64']


def test_tripwire_rhel():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('rhel')


def test_tripwire_slackware():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('slackware')


def test_slackware():
    from rospkg.os_detect import Slackware, OsNotDetected
    test_dir = os.path.join(get_test_dir(), 'slackware')
    detect = Slackware(os.path.join(test_dir, "slackware-version"))
    assert detect.is_os()
    assert detect.get_version() == '14.2'
    assert detect.get_codename() == ''

    # test freely
    detect = Slackware()
    if not detect.is_os():
        try:
            detect.get_version()
            assert False
        except OsNotDetected:
            pass
        try:
            detect.get_codename()
            assert False
        except OsNotDetected:
            pass


def test_tripwire_freebsd():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('freebsd')


def test_freebsd():
    from rospkg.os_detect import FreeBSD, OsNotDetected
    # TODO
    if 0:
        test_dir = os.path.join(get_test_dir(), 'freebsd')
        release_file, issue_file = [os.path.join(test_dir, x) for
                                    x in ["redhat-release", "issue"]]
        detect = FreeBSD(release_file, issue_file)
        assert detect.is_os()
        assert detect.get_version() == '3'

    # test freely
    detect = FreeBSD()
    if not detect.is_os():
        try:
            detect.get_version()
            assert False
        except OsNotDetected:
            pass

    # assure failure
    detect = FreeBSD("/fake/uname/file")
    assert not detect.is_os()
    try:
        detect.get_version()
        assert False
    except OsNotDetected:
        pass
    try:
        detect.get_codename()
        assert False
    except OsNotDetected:
        pass

    @patch.object(FreeBSD, 'is_os')
    def test(mock):
        mock.is_os.return_value = True
        detect = FreeBSD()
        assert detect.get_codename() == ''
    test()


def test_cygwin():
    from rospkg.os_detect import Cygwin, OsNotDetected
    # TODO
    detect = Cygwin()
    if not detect.is_os():
        try:
            detect.get_version()
            assert False
        except OsNotDetected:
            pass

        try:
            detect.get_codename()
            assert False
        except OsNotDetected:
            pass

    @patch.object(Cygwin, 'is_os')
    def test(mock):
        mock.is_os.return_value = True
        detect = Cygwin()
        assert detect.get_codename() == ''
    test()


def test_tripwire_centos():
    from rospkg.os_detect import OsDetect
    os_detect = OsDetect()
    os_detect.get_detector('centos')


def test_OsDetect():
    from rospkg.os_detect import OsDetect
    detect = OsDetect()
    try:
        detect.get_detector('fake')
        assert False, "should raise"
    except KeyError:
        pass


def test_OsDetect_ROS_OVERRIDE():
    from rospkg.os_detect import OsDetect
    detect = OsDetect([('TrueOs', TrueOs())])
    env = {'ROS_OS_OVERRIDE': 'arch'}
    assert detect.detect_os(env=env) == ('arch', '', ''), \
        detect.detect_os(env=env)
    env = {'ROS_OS_OVERRIDE': 'fubuntu:04.10'}
    assert detect.detect_os(env=env) == ('fubuntu', '04.10', '')
    env = {'ROS_OS_OVERRIDE': 'fubuntu:04.10:opaque'}
    assert detect.detect_os(env=env) == ('fubuntu', '04.10', 'opaque')


def test_OsDetect_single():
    # test each method twice with new instance b/c of caching
    from rospkg.os_detect import OsDetect
    detect = OsDetect([('TrueOs', TrueOs())])
    assert "TrueOs" == detect.get_name()
    assert "TrueOs" == detect.get_name()
    detect = OsDetect([('TrueOs', TrueOs())])
    assert "os_version" == detect.get_version()
    assert "os_version" == detect.get_version()
    detect = OsDetect([('TrueOs', TrueOs())])
    assert "os_codename" == detect.get_codename()
    assert "os_codename" == detect.get_codename()

    detect = OsDetect([('TrueOs', TrueOs())])
    assert isinstance(detect.get_detector(), TrueOs)
    assert isinstance(detect.get_detector('TrueOs'), TrueOs)


def test_OsDetect_register_default_add_detector():
    # test behavior of register_default and add_detector.  Both take
    # precedence over previous detectors, but at different scopes.
    from rospkg.os_detect import OsDetect
    o1 = TrueOs()
    o2 = TrueOs2()
    key = 'TrueOs'
    detect = OsDetect([(key, o1)])

    assert detect.get_detector(key) == o1
    detect.register_default(key, o2)
    assert detect.get_detector(key) == o1
    detect.add_detector(key, o2)
    assert detect.get_detector(key) == o2

    detect = OsDetect()
    assert detect.get_detector(key) == o2
    detect.add_detector(key, o1)
    assert detect.get_detector(key) == o1

    # restore precendence of o1 in default list
    detect.register_default(key, o1)
    detect = OsDetect()
    assert detect.get_detector(key) == o1


def test_OsDetect_nomatch():
    from rospkg.os_detect import OsDetect, OsNotDetected
    detect = OsDetect([('Dummy', FalseOs())])
    assert isinstance(detect.get_detector('Dummy'), FalseOs)
    try:
        detect.get_name()
        assert False
    except OsNotDetected:
        pass
    try:
        detect.get_version()
        assert False
    except OsNotDetected:
        pass
    try:
        detect.get_detector()
        assert False
    except OsNotDetected:
        pass


def xTrueOsDetect_first_of_two():
    osa = roslib.os_detect.OSDetect([TrueOs(), FalseOs()])
    assert "os_name" == osa.get_name()
    assert "os_version" == osa.get_version()
    os_class = osa.get_os()
    assert "os_name" == os_class.get_name()
    assert "os_version" == os_class.get_version()


def xTrueOsDetect_second_of_two():
    osa = roslib.os_detect.OSDetect([FalseOs(), TrueOs()])
    assert "os_name", osa.get_name()
    assert "os_version", osa.get_version()
    os_class = osa.get_os()
    assert "os_name" == os_class.get_name()
    assert "os_version" == os_class.get_version()


def xTrueOsDetect_first_of_many():
    osa = roslib.os_detect.OSDetect([TrueOs(), FalseOs(), FalseOs(), FalseOs(), FalseOs()])
    assert "os_name" == osa.get_name()
    assert "os_version" == osa.get_version()
    os_class = osa.get_os()
    assert "os_name" == os_class.get_name()
    assert "os_version" == os_class.get_version()


def xTrueOsDetect_second_of_many():
    osa = roslib.os_detect.OSDetect([FalseOs(), TrueOs(), FalseOs(), FalseOs(), FalseOs()])
    assert "os_name" == osa.get_name()
    assert "os_version" == osa.get_version()
    os_class = osa.get_os()
    assert "os_name" == os_class.get_name()
    assert "os_version" == os_class.get_version()


def xTrueOsDetect_last_of_many():
    osa = roslib.os_detect.OSDetect([FalseOs(), FalseOs(), FalseOs(), FalseOs(), TrueOs()])
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
