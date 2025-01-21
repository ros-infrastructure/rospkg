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
import subprocess
import tempfile


def get_package_test_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'package_tests'))


def test_ManifestManager_constructor():
    from rospkg import RosPack, RosStack, get_ros_paths

    r = RosPack()
    assert r._manifest_name == 'manifest.xml'
    r = RosStack()
    assert r._manifest_name == 'stack.xml'
    for c in [RosPack, RosStack]:
        r = c()
        assert r.ros_paths == get_ros_paths()

        tmp = tempfile.gettempdir()

        r = c(ros_paths=[tmp])
        assert r.ros_paths == [tmp]
        # make sure we can't accidentally mutate the actual data
        r.ros_paths.append('foo')
        assert r.ros_paths == [tmp]


def test_ManifestManager_get_instance():
    from rospkg import RosPack, RosStack, get_ros_paths

    for c in [RosPack, RosStack]:
        # make sure we get the same instance for defaults ros_paths
        r1 = c.get_instance()
        assert r1.ros_paths == get_ros_paths()
        r2 = c.get_instance()
        assert r1 is r2

        # make sure we get the same instance for identical custom ros_paths
        tmp = tempfile.gettempdir()
        r3 = c.get_instance(ros_paths=[tmp])
        assert r3.ros_paths == [tmp]
        r4 = c.get_instance(ros_paths=[tmp])
        assert r3 is r4

        # make sure for different ros_paths we got different instances
        assert r1 is not r3


def rospackexec(args):
    rospack_bin = 'rospack'
    val = (subprocess.Popen([rospack_bin] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0] or '').strip()
    if val.startswith('rospack:'):  # rospack error message
        raise Exception(val)
    return val


# for comparing against 'ground truth'
def rospack_list():
    return [s.strip() for s in rospackexec(['list-names']).split('\n') if s.strip()]


def rospack_find(package):
    return rospackexec(['find', package]).strip()


def rospack_depends(package):
    return unicode(rospackexec(['depends', package])).split()


def rospack_depends1(package):
    return unicode(rospackexec(['depends1', package])).split()


def rospack_depends_on(package):
    return unicode(rospackexec(['depends-on', package])).split()


def rospack_depends_on1(package):
    return unicode(rospackexec(['depends-on1', package])).split()


def delete_cache():
    from rospkg import get_ros_home
    p = os.path.join(get_ros_home(), 'rospack_cache')
    if os.path.exists(p):
        os.remove(p)


def rospack_is_available():
    try:
        rospackexec(['-h'])
        return True
    except:
        return False


def test_RosPack_list():
    from rospkg import RosPack, get_ros_root
    if get_ros_root() is not None and rospack_is_available():
        r = RosPack()

        pkgs = rospack_list()
        retval = r.list()
        assert set(pkgs) == set(retval), "%s vs %s" % (pkgs, retval)

        # test twice for caching
        retval = r.list()
        assert set(pkgs) == set(retval), "%s vs %s" % (pkgs, retval)

        # make sure stress test works with rospack_cache invalidated
        delete_cache()
        r = RosPack()
        retval = r.list()
        assert set(pkgs) == set(retval), "%s vs %s" % (pkgs, retval)


def test_RosPack_no_env():
    # regression test for #3680
    from rospkg import RosPack, ResourceNotFound
    try:
        environ_copy = os.environ.copy()
        if 'ROS_ROOT' in os.environ:
            del os.environ['ROS_ROOT']
        if 'ROS_PACKAGE_PATH' in os.environ:
            del os.environ['ROS_PACKAGE_PATH']
        r = RosPack()
        try:
            r.get_depends('roscpp')
            assert False, "should have raised"
        except ResourceNotFound:
            pass
    finally:
        os.environ.clear()
        os.environ.update(environ_copy)


def test_RosPack_get_path():
    from rospkg import RosPack, ResourceNotFound, get_ros_root

    path = get_package_test_path()
    foo_path = os.path.join(path, 'p1', 'foo')
    foo_path_alt = os.path.join(path, 'p2', 'foo')
    bar_path = os.path.join(path, 'p1', 'bar')
    baz_path = os.path.join(path, 'p2', 'baz')

    # point ROS_ROOT at top, should spider entire tree
    print("ROS path: %s" % (path))
    r = RosPack(ros_paths=[path])
    # precedence in this case is undefined as there are two 'foo's in the same path
    assert r.get_path('foo') in [foo_path, foo_path_alt]
    assert bar_path == r.get_path('bar')
    assert baz_path == r.get_path('baz')
    try:
        r.get_path('fake')
        assert False
    except ResourceNotFound:
        pass

    # divide tree in half to test precedence
    print("ROS_PATH 1: %s" % (os.path.join(path, 'p1')))
    print("ROS_PATH 2: %s" % (os.path.join(path, 'p2')))
    r = RosPack(ros_paths=[os.path.join(path, 'p1'), os.path.join(path, 'p2')])
    assert foo_path == r.get_path('foo'), "%s vs. %s" % (foo_path, r.get_path('foo'))
    assert bar_path == r.get_path('bar')
    assert baz_path == r.get_path('baz')

    if get_ros_root() and rospack_is_available():
        # stresstest against rospack
        r = RosPack()
        for p in rospack_list():
            retval = r.get_path(p)
            rospackval = rospack_find(p)
            assert retval == rospackval, "[%s]: %s vs. %s" % (p, retval, rospackval)


def test_RosPackage_get_depends():
    from rospkg import RosPack, ResourceNotFound, get_ros_root
    path = get_package_test_path()
    r = RosPack(ros_paths=[path])

    # test on multiple calls to bad package -- there was an ordering
    # issue in the logic that caused get_depends() to return an empty
    # set on the second call.
    for i in range(1, 4):
        try:
            r.get_depends('bad', implicit=True)
            assert False, "should have raised"
        except ResourceNotFound:
            pass

    # TODO: need one more step
    assert set(r.get_depends('baz')) == set(['foo', 'bar'])
    assert r.get_depends('bar') == ['foo']
    assert r.get_depends('foo') == []

    if get_ros_root() and rospack_is_available():
        # stress test: test default environment against rospack
        r = RosPack()
        for p in rospack_list():
            retval = set(r.get_depends(p))
            rospackval = set(rospack_depends(p))
            assert retval == rospackval, "[%s]: %s vs. %s" % (p, retval, rospackval)


def get_stack_test_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'stack_tests'))


def test_stack_of():
    from rospkg import RosPack, ResourceNotFound
    path = os.path.join(get_stack_test_path(), 's1')
    r = RosPack(ros_paths=[path])

    # test with actual stacks
    assert r.stack_of('foo_pkg') == 'foo'
    assert r.stack_of('foo_pkg_2') == 'foo'
    assert r.stack_of('bar_pkg') == 'bar'

    try:
        r.stack_of('fake')
        assert False, "should have raised ResourceNotFound"
    except ResourceNotFound:
        pass

    path = os.path.join(get_package_test_path(), 'p1')
    r = RosPack(ros_paths=[path])

    # test with actual not stacked-packages
    assert r.stack_of('foo') is None


def test_RosPackage_get_depends_explicit():
    from rospkg import RosPack, get_ros_root
    path = get_package_test_path()
    r = RosPack(ros_paths=[path])

    implicit = False
    assert set(r.get_depends('baz', implicit)) == set(['bar', 'foo'])
    assert r.get_depends('bar', implicit) == ['foo']
    assert r.get_depends('foo', implicit) == []

    if get_ros_root() and rospack_is_available():
        # stress test: test default environment against rospack
        r = RosPack()
        for p in rospack_list():
            retval = set(r.get_depends(p, implicit))
            rospackval = set(rospack_depends1(p))
            assert retval == rospackval, "[%s]: %s vs. %s" % (p, retval, rospackval)


def test_RosPack_get_rosdeps():
    from rospkg import RosPack

    path = get_package_test_path()
    r = RosPack(ros_paths=[os.path.join(path, 'p1'), os.path.join(path, 'p2')])

    # repeat tests due to caching
    assert set(['foo_rosdep1', 'foo_rosdep2', 'foo_rosdep3']) == set(r.get_rosdeps('foo', implicit=True)), r.get_rosdeps('foo', implicit=True)
    assert set(['foo_rosdep1', 'foo_rosdep2', 'foo_rosdep3']) == set(r.get_rosdeps('foo', implicit=True))
    assert set(['foo_rosdep1', 'foo_rosdep2', 'foo_rosdep3']) == set(r.get_rosdeps('foo', implicit=False))

    assert set(['bar_rosdep1', 'bar_rosdep2']) == set(r.get_rosdeps('bar', implicit=False))
    assert set(['foo_rosdep1', 'foo_rosdep2', 'foo_rosdep3', 'bar_rosdep1', 'bar_rosdep2']) == set(r.get_rosdeps('bar', implicit=True))
    assert set(['foo_rosdep1', 'foo_rosdep2', 'foo_rosdep3', 'bar_rosdep1', 'bar_rosdep2']) == set(r.get_rosdeps('bar', implicit=True))
    assert set(['foo_rosdep1', 'foo_rosdep2', 'foo_rosdep3', 'bar_rosdep1', 'bar_rosdep2']) == set(r.get_rosdeps('bar'))

    assert ['baz_rosdep1'] == r.get_rosdeps('baz', implicit=False)
    assert set(['baz_rosdep1', 'foo_rosdep1', 'foo_rosdep2', 'foo_rosdep3', 'bar_rosdep1', 'bar_rosdep2']) == set(r.get_rosdeps('baz'))
    assert set(['baz_rosdep1', 'foo_rosdep1', 'foo_rosdep2', 'foo_rosdep3', 'bar_rosdep1', 'bar_rosdep2']) == set(r.get_rosdeps('baz'))

    # create a brand new instance to test with brand new cache
    r = RosPack(ros_paths=[os.path.join(path, 'p1'), os.path.join(path, 'p2')])
    assert set(['baz_rosdep1', 'foo_rosdep1', 'foo_rosdep2', 'foo_rosdep3', 'bar_rosdep1', 'bar_rosdep2']) == set(r.get_rosdeps('baz'))
    assert set(['baz_rosdep1', 'foo_rosdep1', 'foo_rosdep2', 'foo_rosdep3', 'bar_rosdep1', 'bar_rosdep2']) == set(r.get_rosdeps('baz'))


def test_get_package_name():
    from rospkg import __version__
    from rospkg import get_package_name

    test_dir = get_package_test_path()

    test_dir_foo = os.path.join(test_dir, 'p1', 'foo')
    assert 'foo' == get_package_name(test_dir_foo)

    # baz dir is a subdirectory of foo package
    test_dir_foo_baz = os.path.join(test_dir_foo, 'baz')
    assert 'foo' == get_package_name(test_dir_foo_baz)

    # test with path outside of our hierarchy
    assert get_package_name(tempfile.tempdir) is None


def test_get_depends_on():
    from rospkg import RosPack, get_ros_root
    test_dir = get_package_test_path()
    rp = RosPack(ros_paths=[test_dir])
    # test direct depends
    val = rp.get_depends_on('foo', implicit=False)
    assert set(['bar', 'baz']) == set(val), val
    val = rp.get_depends_on('bar', implicit=False)
    assert ['baz'] == val, val
    val = rp.get_depends_on('baz', implicit=False)
    assert [] == val, val

    # test implicit depends
    val = rp.get_depends_on('foo', implicit=True)
    assert set(['bar', 'baz']) == set(val), val
    val = rp.get_depends_on('bar', implicit=True)
    assert ['baz'] == val, val
    val = rp.get_depends_on('baz', implicit=True)
    assert [] == val, val

    if get_ros_root() and rospack_is_available():
        # stress test: test default environment against rospack
        r = RosPack()
        for p in rospack_list():
            retval = set(r.get_depends_on(p, False))
            rospackval = set(rospack_depends_on1(p))
            assert retval == rospackval, "[%s]: %s vs. %s" % (p, retval, rospackval)
        for p in rospack_list():
            retval = set(r.get_depends_on(p, True))
            rospackval = set(rospack_depends_on(p))
            assert retval == rospackval, "[%s]: %s vs. %s" % (p, retval, rospackval)
