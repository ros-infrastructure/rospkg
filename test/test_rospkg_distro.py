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
import yaml

def get_test_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'rosdistro'))

def get_etc_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'fakeetcros'))

def test_distro_uri():
    from rospkg.distro import distro_uri
    assert distro_uri('electric') == "https://code.ros.org/svn/release/trunk/distros/electric.rosdistro"
    
def test_current_distro_codename():
    import rospkg.environment
    from rospkg.distro import current_distro_codename
    assert 'awesome' == current_distro_codename(env={'ROS_DISTRO':'awesome'})
    env={rospkg.environment.ROS_ETC_DIR: get_etc_path()}
    val = current_distro_codename(env=env)
    assert 'rosawesome' == current_distro_codename(env=env), val
    
def test__current_distro_electric():
    from rospkg.distro import _current_distro_electric
    # tripwire, not allowed to throw
    _current_distro_electric()
    
def test__current_distro_electric_parse_roscore():
    from rospkg.distro import _current_distro_electric_parse_roscore
    roscore_file = os.path.join(get_test_path(), 'roscore-electric.xml')
    assert os.path.exists(roscore_file), roscore_file
    val = _current_distro_electric_parse_roscore(roscore_file)
    assert 'electric' == val, val

    bad_roscore_file = os.path.join(get_test_path(), 'roscore-bad.xml')
    assert None == _current_distro_electric_parse_roscore(bad_roscore_file)
    
    no_roscore_file = os.path.join(get_test_path(), 'non-existent.xml')
    assert None == _current_distro_electric_parse_roscore(no_roscore_file)

def xtest_Distro_dback(self):
    # TODO: better unit tests. For now this is mostly a tripwire
    from rospkg.distro import Distro, DistroStack, Variant
    distros = load_Distros_dback()
    dback = distros['diamondback']
    r = 'diamondback'
    v = 'r8596'

    self.assertEquals(r, dback.release_name)
    self.assertEquals(v, dback.version)        

    # make sure ros got assigned and is correct
    ros = DistroStack('ros', dback_ros_rules, dback_versions['ros'], r, v)
    self.assertEquals(ros, dback.ros)
    self.assertEquals(ros, dback.stacks['ros'])        

    # make sure the variants are configured
    self.assert_('base' not in dback.variants)

    ros_base = dback.variants['ros-base']
    self.assertEquals([], ros_base.extends)
    ros_base_stacks = ['ros', 'ros_comm']
    self.assertEquals(ros_base_stacks, ros_base.stack_names)

    robot = dback.variants['robot'] #extends ros-base
    self.assertEquals(set(['ros-base']), set(robot.extends))
    robot_stacks = ['common_msgs', 'common', 'diagnostics', 'driver_common', 'geometry', 'robot_model', 'executive_smach']
    self.assertEquals(set(ros_base_stacks+robot_stacks), set(robot.stack_names))
    self.assertEquals(set(robot_stacks), set(robot.stack_names_explicit))

    mobile = dback.variants['mobile'] #extends robot
    mobile_stacks = ['navigation', 'slam_gmapping']
    self.assertEquals(set(ros_base_stacks+robot_stacks+mobile_stacks), set(mobile.stack_names))
    self.assertEquals(set(mobile_stacks), set(mobile.stack_names_explicit))

    viz = dback.variants['viz'] 
    self.assertEquals([], viz.extends)
    viz_stacks = ['visualization_common', 'visualization'] 
    self.assertEquals(set(viz_stacks), set(viz.stack_names))
    self.assertEquals(set(viz_stacks), set(viz.stack_names_explicit))

    desktop = dback.variants['desktop'] #robot, rviz
    self.assertEquals(set(['robot', 'viz']), set(desktop.extends))
    desktop_stacks = ['ros_tutorials', 'common_tutorials', 'geometry_tutorials', 'visualization_tutorials']
    self.assertEquals(set(ros_base_stacks+robot_stacks+viz_stacks+desktop_stacks), set(desktop.stack_names))
    self.assertEquals(set(desktop_stacks), set(desktop.stack_names_explicit))

    simulator_stacks = ['simulator_stage', 'simulator_gazebo', 'physics_ode']
    perception_stacks = ['image_common', 'image_transport_plugins', 'image_pipeline', 'laser_pipeline', 'perception_pcl', 'vision_opencv']
    desktop_full = dback.variants['desktop-full'] 
    self.assertEquals(set(['desktop', 'mobile', 'perception', 'simulators']), set(desktop_full.extends))
    self.assertEquals(set(ros_base_stacks+robot_stacks+mobile_stacks+perception_stacks+simulator_stacks+desktop_stacks+viz_stacks), set(desktop_full.stack_names))
    self.assertEquals([], desktop_full.stack_names_explicit)


    # make sure we loaded the stacks
    stack_names = ['common', 'common_msgs', 'navigation']
    for s in stack_names:
        val = DistroStack(s, dback_rospkg_rules, dback_versions[s], r, v)
        self.assertEquals(val, dback.stacks[s])

    # test an hg rule
    dback_geometry_rules = {'hg':
                            {'dev-branch': 'tf_rework',
                             'distro-tag': '$RELEASE_NAME',
                             'release-tag': '$STACK_NAME-$STACK_VERSION',
                             'uri': 'https://ros-geometry.googlecode.com/hg/'},
                            'repo': 'ros-pkg',
                            }
    s = 'geometry'
    val = DistroStack(s, dback_geometry_rules, dback_versions[s], r, v)
    self.assertEquals(val, dback.stacks[s])

def test_expand_rule():
    from rospkg.distro import expand_rule
    assert 'foo' == expand_rule('$STACK_NAME', 'foo', 'version', 'release')
    assert 'version' == expand_rule('$STACK_VERSION', 'foo', 'version', 'release')
    assert 'release' == expand_rule('$RELEASE_NAME', 'foo', 'version', 'release')
    assert 'foo-version-release' == expand_rule('$STACK_NAME-$STACK_VERSION-$RELEASE_NAME', 'foo', 'version', 'release')    

default_rules = {}
default_rules['git'] = {'git': {'anon-uri': 'https://github.com/ipa320/$STACK_NAME.git',
                                'dev-branch': 'release_electric',
                                'distro-tag': '$RELEASE_NAME',
                                'release-tag': '$STACK_NAME-$STACK_VERSION',
                                'uri': 'git@github.com:ipa320/$STACK_NAME.git'}}
rule = default_rules['git']

def test_DistroStack():
    from rospkg.distro import DistroStack
    s = DistroStack('stack', 'version', 'electric', rule)
    assert 'stack' == s.name
    assert 'version' == s.version
    assert rule == s._rules
    assert 'git' == s.vcs_config.type
    assert s.vcs_config.get_branch('devel', False) == ('git@github.com:ipa320/stack.git', 'release_electric')
    assert s.vcs_config.get_branch('devel', True) == ('https://github.com/ipa320/stack.git', 'release_electric')
    assert s.vcs_config.get_branch('distro', False) == ('git@github.com:ipa320/stack.git', 'electric'), s.vcs_config.get_branch('release', False)
    assert s.vcs_config.get_branch('distro', True) == ('https://github.com/ipa320/stack.git', 'electric')
    assert s.vcs_config.get_branch('release', False) == ('git@github.com:ipa320/stack.git', 'stack-version'), s.vcs_config.get_branch('release', False)
    assert s.vcs_config.get_branch('release', True) == ('https://github.com/ipa320/stack.git', 'stack-version')
    
    assert s == s
    assert s == DistroStack('stack', 'version', 'electric', rule)
    assert s != 'stack'
    assert s != DistroStack('stack2', 'version', 'electric', rule)    
    assert s != DistroStack('stack', 'version2', 'electric', rule)
    assert s != DistroStack('stack', 'version', 'dback', rule)
    rule2 = rule.copy()
    rule2['git']['uri'] == 'foo'
    assert s != DistroStack('stack', 'version', 'dback', rule2)  

def test_Variant():
    from rospkg.distro import Variant
    v = Variant("foo", [], [], [])
    assert 'foo' == v.name
    assert [] == v.extends
    assert [] == v.get_stack_names(True)
    assert [] == v.get_stack_names(False)

    raw_data = {'extends': ['robot', 'viz'],
                'stacks': ['arm_navigation', 'octomap_mapping', 'physics_ode', 'perception_pcl', 'pr2_controllers',
                           'control', 'pr2_mechanism', 'pr2_common']}
    stack_names_implicit = raw_data['stacks'] + ['a', 'b', 'c', 'd']
    v = Variant('bar', raw_data['extends'], raw_data['stacks'], stack_names_implicit)
    assert set(v.extends) == set(['robot', 'viz']), v.extends
    assert set(v.get_stack_names(True)) == set(['arm_navigation', 'octomap_mapping', 'physics_ode', 'perception_pcl', 'pr2_controllers',
                                                'control', 'pr2_mechanism', 'pr2_common', 'a', 'b', 'c', 'd'])
    assert set(v.get_stack_names(False)) == set(['arm_navigation', 'octomap_mapping', 'physics_ode', 'perception_pcl', 'pr2_controllers',
                                                 'control', 'pr2_mechanism', 'pr2_common'])

def test_Distro():
    from rospkg.distro import Distro, Variant, DistroStack

    raw_data = {'extends': ['robot', 'viz'],
                'stacks': ['arm_navigation', 'octomap_mapping', 'physics_ode', 'perception_pcl', 'pr2_controllers',
                           'control', 'pr2_mechanism', 'pr2_common']}
    stack_names_implicit = raw_data['stacks'] + ['a', 'b', 'c', 'd']
    v = Variant('bar', raw_data['extends'], raw_data['stacks'], stack_names_implicit)
    s = DistroStack('stack', 'version', 'electric', rule)
    s_unreleased = DistroStack('unreleased', None, 'electric', rule)

    variants = {'bar': v}
    stacks = {'stack': s, 'unreleased': s_unreleased}
    d = Distro(stacks, variants, 'electric', '1', {})
    assert d._stacks == stacks
    assert d.variants == variants
    assert d.release_name == 'electric'
    assert d.version == '1'
    assert {} == d.raw_data
    assert stacks == d.get_stacks(released=False)
    assert {'stack': s} == d.get_stacks(released=True)
    assert stacks == d.stacks
    assert {'stack': s} == d.released_stacks

dback_ros_rules = {'svn': {'dev': 'https://code.ros.org/svn/ros/stacks/$STACK_NAME/trunk',
                           'distro-tag': 'https://code.ros.org/svn/ros/stacks/$STACK_NAME/tags/$RELEASE_NAME',
                           'release-tag': 'https://code.ros.org/svn/ros/stacks/$STACK_NAME/tags/$STACK_NAME-$STACK_VERSION'},
                   'repo': 'ros'}
dback_rospkg_rules = {'svn': {'dev': 'https://code.ros.org/svn/ros-pkg/stacks/$STACK_NAME/trunk',
                              'distro-tag': 'https://code.ros.org/svn/ros-pkg/stacks/$STACK_NAME/tags/$RELEASE_NAME',
                              'release-tag': 'https://code.ros.org/svn/ros-pkg/stacks/$STACK_NAME/tags/$STACK_NAME-$STACK_VERSION'},
                      'repo': 'ros-pkg'}

dback_versions = {
  'common': '1.3.3',
  'common_msgs': '1.3.5',
  'geometry': '1.3.1',
  'navigation': '1.3.1',
  'ros':'1.4.0',
  }

def test_load_distro_bad_data():
    from rospkg import ResourceNotFound
    from rospkg.distro import load_distro, InvalidDistro
    try:
        load_distro('bad')
        assert False
    except ResourceNotFound: pass
    for i in range(1, 10):
        filename = 'bad%s.rosdistro'%(i)
        try:
            d = get_test_path()
            p = os.path.join(d, filename)
            load_distro(p)
            assert False, "should have raised: %s"%(filename)
        except InvalidDistro: pass
    
def test_load_distro_variants():
    # test with no and empty variants (issue found in fuerte bringup)
    from rospkg.distro import load_distro, Distro
    d = get_test_path()
    for name in ['no_variants.rosdistro', 'empty_variants.rosdistro']:
        p = os.path.join(d, name)
        distro = load_distro(p)
        assert distro.release_name == 'simple', distro.release_name
        assert distro.variants.keys() == []
    
def test_load_distro_simple():
    from rospkg.distro import load_distro, Distro
    d = get_test_path()
    p = os.path.join(d, 'simple.rosdistro')
    distro = load_distro(p)
    assert isinstance(distro, Distro)
    
    assert distro.release_name == 'simple', distro.release_name
    assert distro.version == '1', distro.version
    assert yaml.load(open(p)) == distro.raw_data, distro.raw_data
    assert distro.variants.keys() == ['base']
    assert distro.stacks.keys() == ['stack1']

    stack1 = distro.stacks['stack1']
    assert stack1.vcs_config.get_branch('devel', False) == ('https://simple.com/svn/trunk/stack1', None)
    assert stack1.vcs_config.get_branch('distro', False) == ('https://simple.com/svn/tags/distros/simple/stacks/stack1', None)
    assert stack1.vcs_config.get_branch('release', False) == ('https://simple.com/svn/tags/stacks/stack1/stack1-0.3.0', None)

def test_load_distro_diamondback():
    from rospkg.distro import load_distro, Distro
    d = get_test_path()
    p = os.path.join(d, 'diamondback.rosdistro')
    distro = load_distro(p)
    assert isinstance(distro, Distro)

    assert distro.release_name == 'diamondback', distro.release_name
    assert distro.version == 'r8596', distro.version
    assert yaml.load(open(p)) == distro.raw_data, distro.raw_data
    assert set(distro.variants.keys()) == set(diamondback_variants)
    assert set(distro.stacks.keys()) == set(diamondback_stacks), set(distro.stacks.keys()) ^ set(diamondback_stacks)

    assert distro.variants['ros-base'].extends == []
    retval = distro.variants['ros-base'].get_stack_names(True)
    assert retval == ['ros', 'ros_comm'], retval
    assert distro.variants['ros-base'].get_stack_names(False) == ['ros', 'ros_comm']    
    assert set(distro.variants['ros-full'].get_stack_names(True)) == set(['ros', 'ros_comm', 'rx', 'documentation'])
    
    assert distro.stacks['common'].version == '1.3.3'
    assert distro.stacks['common'].vcs_config.get_branch('devel', True) == ('https://code.ros.org/svn/ros-pkg/stacks/common/trunk', None)

def test__load_variants():
    from rospkg.distro import _load_variants
    raw_data = yaml.load("""variants:
- ros-base:
    stacks: [ros, ros_comm]
- ros-full:
    extends: ros-base
    stacks: [rx, documentation]
- viz:
    stacks: [visualization_common, visualization]
- robot:
    extends: [ros-base]
    stacks: [common_msgs, common, diagnostics]
- desktop:
    extends: [robot, viz, ros-full]
    stacks: [ros_tutorials, common_tutorials]
""")
    raw_data = raw_data['variants']
    # mock data so variants validate
    stacks = dict(ros=1, ros_comm=2, rx=3, documentation=4, visualization_common=5,
                  visualization=6, common_msgs=7, common=8, ros_tutorials=9, common_tutorials=10, diagnostics=11)
    variants = _load_variants(raw_data, stacks)
    assert set(variants.keys()) == set(['ros-base', 'ros-full', 'viz', 'robot', 'desktop']), variants.keys()
    assert variants['ros-base'].extends == []
    assert variants['ros-full'].extends == ['ros-base']    
    assert variants['desktop'].extends == ['robot', 'viz', 'ros-full']

    assert set(variants['ros-base'].get_stack_names(True)) == set(['ros', 'ros_comm'])
    assert set(variants['ros-base'].get_stack_names(False)) == set(['ros', 'ros_comm'])

    assert set(variants['ros-full'].get_stack_names(True)) == set(['rx', 'documentation', 'ros', 'ros_comm'])
    assert set(variants['ros-full'].get_stack_names(False)) == set(['rx', 'documentation'])

    assert set(variants['desktop'].get_stack_names(True)) == set(stacks.keys())
    assert set(variants['desktop'].get_stack_names(False)) == set(['ros_tutorials', 'common_tutorials'])
    
diamondback_stacks = [
    'pr2_web_apps', 'octomap_mapping', 'motion_planning_environment', 'robot_calibration',
    'sound_drivers', 'joystick_drivers', 'ros',
    'pano', 'knowrob', 'perception_pcl', 'image_pipeline', 'kinect',
    'bosch_skin', 'pr2_common_actions', 'pr2_arm_navigation_apps', 'ocr', 'articulation',
    'nxt_robots', 'visualization_common', 'physics_ode', 'arm_navigation', 'collision_environment',
    'executive_smach', 'ethzasl_aseba', 'cart_pushing', 'velodyne', 'pr2_arm_navigation_tests',
    'art_vehicle', 'common', 'motion_planning_visualization', 'geometry_tutorials', 'people',
    'pr2_power_drivers', 'joystick_drivers_tutorials', 'cob_common', 'vslam', 'pr2_arm_navigation',
    'ias_common', 'pr2_navigation_apps', 'geometry_experimental', 'rx', 'motion_planners',
    'pr2_gui', 'simulator_stage', 'linux_networking', 'pr2_calibration', 'image_common',
    'visualization', 'mpi', 'cob_extern', 'camera_drivers', 'laser_drivers',
    'orocos_toolchain_ros', 'driver_common', 'common_msgs', 'pr2_controllers', 'robot_model',
    'motion_planning_common', 'simulator_gazebo', 'cram_pl', 'multimaster_experimental', 'navigation',
    'pr2_robot', 'geometry', 'freiburg_tools', 'nxt_apps', 'wifi_drivers',
    'slam_gmapping', 'web_interface', 'vision_opencv', 'kinematics', 'pr2_simulator',
    'roshpit', 'pr2_cockpit', 'pr2_kinematics', 'sql_database',
    'navigation_experimental', 'pr2_object_manipulation', 'erratic_robot', 'object_manipulation', 'tabletop_object_perception',
    'pr2_tabletop_manipulation_apps', 'bosch_drivers', 'image_transport_plugins', 'perception_pcl_addons', 'slam_karto',
    'wg_hardware_test', 'ros_release', 'pr2_navigation', 'exploration', 'continuous_ops',
    'control', 'ros_tutorials', 'pr2_ethercat_drivers', 'ethzasl_message_transport', 'client_rosjava',
    'ros_realtime', 'pr2_mechanism', 'point_cloud_perception', 'wg_pr2_apps', 'graph_mapping',
    'cob_driver', 'cob_simulation', 'pr2_common', 'wg_robots_gazebo', 'pr2_common_alpha',
    'trajectory_filters', 'topological_navigation', 'imu_drivers', 'ros_applications', 'pr2_exploration',
    'common_tutorials', 'ros_comm', 'mapping', 'pr2_plugs', 'roslisp_common',
    'wg_common', 'roslisp_support', 'cob_apps', 'nxt', 'pr2_apps', 'visualization_tutorials',
    'laser_pipeline', 'pr2_kinematics_with_constraints', 'documentation', 'pr2_self_test', 'diagnostics', 'pr2_doors']

diamondback_variants = [
    'ros-base', 'ros-full', 'viz', 'robot', 'simulators', 'mobile', 'perception', 'desktop',
    'desktop-full', 'move-arm', 'pr2-base', 'pr2', 'pr2-desktop', 'pr2-applications',
    'wg-pr2', 'care-o-bot', 'bosch', 'nxtall', 'alufr', 'utexas-art', 'tum']
