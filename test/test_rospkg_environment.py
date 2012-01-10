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
import sys
import time
import tempfile
  
import subprocess

def test_get_ros_root():
    from rospkg import get_ros_root
    assert None == get_ros_root(env={})

    env = {'ROS_ROOT': '/fake/path'}
    assert '/fake/path' == get_ros_root(env=env)

    real_ros_root = get_ros_root()

    if real_ros_root is not None:
        # make sure that ros root is a directory
        p = os.path.join(real_ros_root, 'Makefile')
        env = {'ROS_ROOT': p}
        assert p == get_ros_root(env=env)
    
def test_get_ros_package_path():
    from rospkg import get_ros_package_path
    assert None == get_ros_package_path(env={})
    env = {'ROS_PACKAGE_PATH': ':'}
    assert ':' == get_ros_package_path(env=env)

    # trip-wire tests. Cannot guarantee that ROS_PACKAGE_PATH is set
    # to valid value on test machine, just make sure logic doesn't crash
    assert os.environ.get('ROS_PACKAGE_PATH', None) == get_ros_package_path()

def test_get_log_dir():
    from rospkg import get_log_dir, get_ros_root
    base = tempfile.gettempdir()
    ros_log_dir = os.path.join(base, 'ros_log_dir')
    ros_home_dir = os.path.join(base, 'ros_home_dir')
    home_dir = os.path.expanduser('~')

    # ROS_LOG_DIR has precedence
    env = {'ROS_ROOT': get_ros_root(), 'ROS_LOG_DIR': ros_log_dir, 'ROS_HOME': ros_home_dir }
    assert ros_log_dir == get_log_dir(env=env)

    env = {'ROS_ROOT': get_ros_root(), 'ROS_HOME': ros_home_dir }
    assert os.path.join(ros_home_dir, 'log') == get_log_dir(env=env)

    env = {'ROS_ROOT': get_ros_root()}
    assert os.path.join(home_dir, '.ros', 'log') == get_log_dir(env=env)

    # test default assignment of env. Don't both checking return value as we would duplicate get_log_dir
    assert get_log_dir() is not None

def test_get_test_results_dir():
    from rospkg import get_ros_root, get_test_results_dir
    base = tempfile.gettempdir()
    ros_test_results_dir = os.path.join(base, 'ros_test_results_dir')
    ros_home_dir = os.path.join(base, 'ros_home_dir')
    home_dir = os.path.expanduser('~')

    # ROS_TEST_RESULTS_DIR has precedence
    env = {'ROS_ROOT': get_ros_root(), 'ROS_TEST_RESULTS_DIR': ros_test_results_dir, 'ROS_HOME': ros_home_dir }
    assert ros_test_results_dir == get_test_results_dir(env=env)

    env = {'ROS_ROOT': get_ros_root(), 'ROS_HOME': ros_home_dir }
    assert os.path.join(ros_home_dir, 'test_results') == get_test_results_dir(env=env)

    env = {'ROS_ROOT': get_ros_root()}
    assert os.path.join(home_dir, '.ros', 'test_results') == get_test_results_dir(env=env)

    # test default assignment of env. Don't both checking return value as we would duplicate get_test_results_dir
    assert get_test_results_dir() is not None

def test_get_ros_home():
    from rospkg import get_ros_root, get_ros_home
    base = tempfile.gettempdir()
    ros_home_dir = os.path.join(base, 'ros_home_dir')
    home_dir = os.path.expanduser('~')

    # ROS_HOME has precedence
    env = {'ROS_ROOT': get_ros_root(), 'ROS_HOME': ros_home_dir }
    assert ros_home_dir == get_ros_home(env=env)

    env = {'ROS_ROOT': get_ros_root()}
    assert os.path.join(home_dir, '.ros') == get_ros_home(env=env)

    # test default assignment of env. Don't both checking return value 
    assert get_ros_home() is not None
    
def test_on_ros_path():
    from rospkg import on_ros_path, get_ros_root, get_ros_package_path
    from rospkg.environment import _resolve_paths

    assert not on_ros_path(tempfile.gettempdir())

    if get_ros_root() is not None:
        assert on_ros_path(get_ros_root())

        paths = _resolve_paths(get_ros_package_path()).split(os.pathsep)
        for p in paths:
            assert on_ros_path(p), "failed: %s, [%s]"%(p, paths)

def test_compute_package_paths():
    from rospkg.environment import _compute_package_paths as compute_package_paths
    assert compute_package_paths(None, None) == []
    assert compute_package_paths('foo', None) == ['foo']
    assert compute_package_paths(None, 'bar') == ['bar'], compute_package_paths(None, 'bar')
    assert compute_package_paths('foo', '') == ['foo']    
    assert compute_package_paths('foo', 'bar') == ['foo', 'bar']
    assert compute_package_paths('foo', 'bar:bz') == ['foo', 'bar', 'bz']
    assert compute_package_paths('foo', 'bar:bz::blah') == ['foo', 'bar', 'bz', 'blah']
    
def test_resolve_path():
    # mainly for coverage
    from rospkg.environment import _resolve_path
    assert os.path.expanduser('~') == _resolve_path('~')
