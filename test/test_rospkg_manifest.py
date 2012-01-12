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

from __future__ import print_function

import os
import sys
  
def test_InvalidManifest():
    from rospkg import InvalidManifest
    assert isinstance(InvalidManifest(), Exception)

def test_Platform():
    from rospkg.manifest import Platform, InvalidManifest
    for bad in [None, '']:
        try:
            Platform(bad, '1')
            assert False, "should have failed on [%s]"%bad
        except ValueError: pass
        try:
            Platform('ubuntu', bad)
            assert False, "should have failed on [%s]"%bad
        except ValueError: pass
    
    p = Platform('ubuntu', '8.04')
    assert 'ubuntu 8.04' == str(p)
    assert 'ubuntu 8.04' == repr(p)

    for v in [Platform('ubuntu', '8.04'), Platform('ubuntu', '8.04', notes=None)]:
        assert p == p
    for v in [Platform('ubuntu', '8.04', 'some notes'), 'foo', 1]:
        assert p != v

    # note: probably actually "osx"
    p = Platform('OS X', '10.6', 'macports')
    assert 'OS X 10.6' == str(p)
    assert 'OS X 10.6' == repr(p)

    for v in [p, Platform('OS X', '10.6', 'macports')]: 
        assert p == p
    for v in [Platform('OS X', '10.6'), 'foo', 1]:
        assert p != v
    
def test_Depend():
    from rospkg.manifest import Depend, InvalidManifest
    for bad in [None, '']:
        try:
            Depend(bad, 'package')
            assert False, "should have failed on [%s]"%bad
        except ValueError: pass
        try:
            Depend('foo', bad)
            assert False, "should have failed on [%s]"%bad
        except ValueError: pass
    
    d = Depend('roslib', 'package')
    assert 'roslib' == str(d)
    assert 'roslib' == repr(d)

    assert d == Depend('roslib', 'package')
    for v in [Depend('roslib', 'stack'), Depend('roslib2', 'package'), 1]:
        assert d != v
    
def _subtest_parse_example1(m):
    from rospkg.manifest import Manifest
    assert isinstance(m, Manifest)
    assert 'package' == m.type
    assert "a brief description" == m.brief
    assert "Line 1\nLine 2" == m.description.strip()
    assert "The authors\ngo here" == m.author.strip()
    assert "Public Domain\nwith other stuff" == m.license.strip()
    assert "http://pr.willowgarage.com/package/" == m.url
    for d in m.depends:
        assert 'package' == d.type
    dpkgs = [d.name for d in m.depends]
    assert set(['pkgname', 'common']) == set(dpkgs)
    rdpkgs = [d.name for d in m.rosdeps]
    assert set(['python', 'bar', 'baz']) == set(rdpkgs)
    for p in m.platforms:
        if p.os == 'ubuntu':
            assert "8.04" == p.version
            assert '' == p.notes
        elif p.os == 'OS X':
            assert "10.6" == p.version
            assert "macports" == p.notes
        else:
            assert False, "unknown platform "+str(p)

def _subtest_parse_stack_example1(m):
    from rospkg.manifest import Manifest
    assert isinstance(m, Manifest)
    assert 'stack' == m.type
    assert "a brief description" == m.brief
    assert "Line 1\nLine 2" == m.description.strip()
    assert "The authors\ngo here" == m.author.strip()
    assert "Public Domain\nwith other stuff" == m.license.strip()
    assert "http://ros.org/stack/" == m.url
    for d in m.depends:
        assert 'stack' == d.type
    dpkgs = [d.name for d in m.depends]
    assert set(['stackname', 'common']) == set(dpkgs)
    assert [] == m.rosdeps
    assert [] == m.exports

def _subtest_parse_stack_version(m):
    assert "1.2.3" == m.version

def get_test_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'manifest'))

def test_is_catkin():
    from rospkg.manifest import parse_manifest_file, MANIFEST_FILE, STACK_FILE
    d = get_test_dir()
    m = parse_manifest_file(os.path.join(d, 'catkin'), MANIFEST_FILE)
    assert m.is_catkin
    m = parse_manifest_file(os.path.join(d, 'example1'), MANIFEST_FILE)
    assert not m.is_catkin

def test_parse_manifest_file():
    from rospkg.manifest import parse_manifest_file, MANIFEST_FILE, STACK_FILE

    d = get_test_dir()
    m = parse_manifest_file(os.path.join(d, 'example1'), MANIFEST_FILE)
    _subtest_parse_example1(m)
    
    m = parse_manifest_file(os.path.join(d, 'stack_example1'), STACK_FILE)
    _subtest_parse_stack_example1(m)

    m = parse_manifest_file(os.path.join(d, 'stack_version'), STACK_FILE)
    _subtest_parse_stack_version(m)

def test_parse_manifest():
    # test_parse_manifest_file is more thorough; just want to make sure we have one call to lower-levle API
    from rospkg.manifest import parse_manifest, MANIFEST_FILE, STACK_FILE
    d = get_test_dir()
    p = os.path.join(d, 'example1', MANIFEST_FILE)
    with open(p, 'r') as f:
        contents = f.read()
    _subtest_parse_example1(parse_manifest(MANIFEST_FILE, contents, p))
    
def test__Manifest():
    from rospkg.manifest import Manifest
    m = Manifest()
    # check defaults
    assert 'package' == m.type

    m = Manifest('package')
    assert 'package' == m.type
    m = Manifest('stack')
    assert 'stack' == m.type

    # tripwire, no defined value
    str(m)
    repr(m)
    
# bad file examples should be more like the roslaunch tests where there is just 1 thing wrong
def test_parse_bad_file():
    from rospkg.manifest import parse_manifest, InvalidManifest, MANIFEST_FILE
    base_p = get_test_dir()
    for b in ['bad1.xml', 'bad2.xml', 'bad3.xml']:
        p = os.path.join(base_p, b)
        with open(p, 'r') as f:
            contents = f.read()
        try:
            parse_manifest(MANIFEST_FILE, contents, filename=p)
            assert False, "parse should have failed on bad manifest"
        except InvalidManifest as e:
            print(str(e))
            assert p in str(e), "file name [%s] should be in error message [%s]"%(p, str(e))
    
EXAMPLE1 = """<package>
  <description brief="a brief description">Line 1
Line 2
  </description>
  <author>The authors
go here</author>
  <license>Public Domain
with other stuff</license>
  <url>http://pr.willowgarage.com/package/</url>
  <logo>http://www.willowgarage.com/files/willowgarage/robot10.jpg</logo>
  <depend package="pkgname" />
  <depend package="common"/>
  <export>
    <cpp cflags="-I${prefix}/include" lflags="-L${prefix}/lib -lros"/>
    <cpp os="osx" cflags="-I${prefix}/include" lflags="-L${prefix}/lib -lrosthread -framework CoreServices"/>
  </export>
  <rosdep name="python" />
  <rosdep name="bar" />
  <rosdep name="baz" />
  <platform os="ubuntu" version="8.04" />
  <platform os="OS X" version="10.6" notes="macports" />
  <rosbuild2> 
    <depend thirdparty="thisshouldbeokay"/> 
  </rosbuild2>
</package>"""

STACK_EXAMPLE1 = """<stack>
  <description brief="a brief description">Line 1
Line 2
  </description>
  <author>The authors
go here</author>
  <license>Public Domain
with other stuff</license>
  <url>http://ros.org/stack/</url>
  <logo>http://www.willowgarage.com/files/willowgarage/robot10.jpg</logo>
  <depend stack="stackname" />
  <depend stack="common"/>
</stack>"""

STACK_INVALID1 = """<stack>
  <description brief="a brief description">Line 1</description>
  <author>The authors</author>
  <license>Public Domain</license>
  <rosdep name="python" />
</stack>"""

STACK_INVALID2 = """<stack>
  <description brief="a brief description">Line 1</description>
  <author>The authors</author>
  <license>Public Domain</license>
  <export>
    <cpp cflags="-I${prefix}/include" lflags="-L${prefix}/lib -lros"/>
    <cpp os="osx" cflags="-I${prefix}/include" lflags="-L${prefix}/lib -lrosthread -framework CoreServices"/>
  </export>
</stack>"""
