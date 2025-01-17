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

import os

import rospkg

search_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'catkin_package_tests'))


def test_find_packages():
    manager = rospkg.rospack.ManifestManager(rospkg.common.MANIFEST_FILE, ros_paths=[search_path])
    # for backward compatibility a wet package which is not a metapackage is found when searching for MANIFEST_FILE
    assert(len(manager.list()) == 1)
    manager = rospkg.rospack.ManifestManager(rospkg.common.STACK_FILE, ros_paths=[search_path])
    assert(len(manager.list()) == 0)
    manager = rospkg.rospack.ManifestManager(rospkg.common.PACKAGE_FILE, ros_paths=[search_path])

    for pkg_name in manager.list():
        assert(pkg_name == 'foo')
        path = manager.get_path(pkg_name)
        assert(path == os.path.join(search_path, 'p1', 'foo'))


def test_get_manifest():
    manager = rospkg.rospack.ManifestManager(rospkg.common.MANIFEST_FILE, ros_paths=[search_path])
    manif = manager.get_manifest("foo")
    assert(manif.type == "package")


def test_licenses():
    rospack = rospkg.rospack.RosPack(ros_paths=[search_path])
    licenses_list = ["BSD", "LGPL"]
    manif = rospack.get_manifest("foo")
    assert(manif.license == ", ".join(licenses_list))
    assert(len(manif.licenses) == 2)
    for l in manif.licenses:
        assert(l in licenses_list)
