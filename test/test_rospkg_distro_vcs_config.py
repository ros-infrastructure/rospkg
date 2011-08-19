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

def test_BZRConfig():
    pass

def test_HgConfig():
    from rospkg.rosdistro import HgConfig
    anon_rules = {
        'dev-branch': 'default',
        'distro-tag': '$RELEASE_NAME',
        'release-tag': '$STACK_NAME-$STACK_VERSION',
        'anon-uri': 'https://kforge.ros.org/navigation/navigation',
        'uri': 'ssh://user@kforge.ros.org/navigation/navigation'
        }
    rules = {
        'dev-branch': 'default',
        'distro-tag': '$RELEASE_NAME',
        'release-tag': '$STACK_NAME-$STACK_VERSION',
        'uri': 'https://kforge.ros.org/navigation/navigation'
        }

    config = HgConfig()
    anon_config = HgConfig()

    required = ['dev-branch', 'distro-tag', 'release-tag', 'uri']
    for r in required:
        bad_copy = rules.copy()
        del bad_copy[r]
        try:
            config.load(bad_copy, lambda x: x)
            assert False, "should have raised"
        except KeyError: pass
    
    config.load(rules, lambda x: x+'evaled')
    anon_config.load(anon_rules, lambda x: x+'evaled')

    repo_uri = 'ssh://user@kforge.ros.org/navigation/navigationevaled'
    anon_repo_uri = 'https://kforge.ros.org/navigation/navigationevaled'
    assert config.repo_uri == anon_repo_uri, config.repo_uri
    assert config.anon_repo_uri == anon_repo_uri, config.anon_repo_uri
    assert anon_config.repo_uri == repo_uri, anon_config.repo_uri
    for c in [config, anon_config]:
        assert c.dev_branch == 'defaultevaled'
        assert c.distro_tag == '$RELEASE_NAMEevaled'
        assert c.release_tag == '$STACK_NAME-$STACK_VERSIONevaled'
        assert c.anon_repo_uri == anon_repo_uri

    c = anon_config
    assert c.get_branch('devel', False) == (repo_uri, 'defaultevaled')
    assert c.get_branch('devel', True) == (anon_repo_uri, 'defaultevaled')
    assert c.get_branch('distro', False) == (repo_uri, '$RELEASE_NAMEevaled')
    assert c.get_branch('distro', True) == (anon_repo_uri, '$RELEASE_NAMEevaled')
    assert c.get_branch('release', False) == (repo_uri, '$STACK_NAME-$STACK_VERSIONevaled')
    assert c.get_branch('release', True) == (anon_repo_uri, '$STACK_NAME-$STACK_VERSIONevaled')

    # test equals
    config2 = HgConfig()
    config2.load(rules, lambda x: x+'evaled')
    assert config == config2
    anon_config2 = HgConfig()    
    anon_config2.load(anon_rules, lambda x: x+'evaled')
    assert anon_config == anon_config2

def test_GitConfig():
    from rospkg.rosdistro import GitConfig
    anon_rules = {
        'anon-uri': 'https://github.com/ipa320/$STACK_NAME.git',
        'dev-branch': 'release_electric',
        'distro-tag': '$RELEASE_NAME',
        'release-tag': '$STACK_NAME-$STACK_VERSION',
        'uri': 'git@github.com:ipa320/$STACK_NAME.git'
        }
    rules = anon_rules.copy()
    del rules['anon-uri']

    config = GitConfig()
    anon_config = GitConfig()

    required = ['dev-branch', 'distro-tag', 'release-tag', 'uri']
    for r in required:
        bad_copy = rules.copy()
        del bad_copy[r]
        try:
            config.load(bad_copy, lambda x: x)
            assert False, "should have raised"
        except KeyError: pass
    
    config.load(rules, lambda x: x+'evaled')
    anon_config.load(anon_rules, lambda x: x+'evaled')
    repo_uri = 'git@github.com:ipa320/$STACK_NAME.gitevaled'
    anon_repo_uri ='https://github.com/ipa320/$STACK_NAME.gitevaled'
    
    assert config.repo_uri == repo_uri
    assert anon_config.anon_repo_uri == anon_repo_uri
    for c in [config, anon_config]:
        dev_branch = 'release_electricevaled'
        assert c.dev_branch == dev_branch
        assert c.distro_tag == '$RELEASE_NAMEevaled'
        assert c.release_tag == '$STACK_NAME-$STACK_VERSIONevaled'
        assert c.repo_uri == repo_uri

    c = anon_config
    assert c.get_branch('devel', False) == (repo_uri, dev_branch), c.get_branch('devel', False)
    assert c.get_branch('devel', True) == (anon_repo_uri, dev_branch)
    assert c.get_branch('distro', False) == (repo_uri, '$RELEASE_NAMEevaled')
    assert c.get_branch('distro', True) == (anon_repo_uri, '$RELEASE_NAMEevaled')
    assert c.get_branch('release', False) == (repo_uri, '$STACK_NAME-$STACK_VERSIONevaled')
    assert c.get_branch('release', True) == (anon_repo_uri, '$STACK_NAME-$STACK_VERSIONevaled')

    # test equals
    config2 = GitConfig()
    config2.load(rules, lambda x: x+'evaled')
    assert config == config2
    anon_config2 = GitConfig()    
    anon_config2.load(anon_rules, lambda x: x+'evaled')
    assert anon_config == anon_config2

def test_SvnConfig():
    from rospkg.rosdistro import SvnConfig
    config = SvnConfig()
    required = ['dev', 'distro-tag', 'release-tag']
    rules = {'dev': 'https://alufr-ros-pkg.googlecode.com/svn/trunk/$STACK_NAME',
             'distro-tag': 'https://alufr-ros-pkg.googlecode.com/svn/tags/distros/$RELEASE_NAME/stacks/$STACK_NAME',
             'release-tag': 'https://alufr-ros-pkg.googlecode.com/svn/tags/stacks/$STACK_NAME/$STACK_NAME-$STACK_VERSION'}

    anon_rules = {
        'anon-dev': 'http://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/trunk',
        'anon-distro-tag': 'http://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/tags/$RELEASE_NAME',
        'anon-release-tag': 'http://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/tags/$STACK_NAME-$STACK_VERSION',
        'dev': 'https://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/trunk',
        'distro-tag': 'https://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/tags/$RELEASE_NAME',
        'release-tag': 'https://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/tags/$STACK_NAME-$STACK_VERSION'}

    # make sure it validates
    for k in required:
        bad_copy = rules.copy()
        del bad_copy[k]
        try:
            config.load(bad_copy, lambda x: x)
            assert False, "should have raised"
        except KeyError: pass
        
    # load w/o anon rules
    config.load(rules, lambda x: x+'evaled')
    assert config.dev == 'https://alufr-ros-pkg.googlecode.com/svn/trunk/$STACK_NAMEevaled'
    assert config.distro_tag == 'https://alufr-ros-pkg.googlecode.com/svn/tags/distros/$RELEASE_NAME/stacks/$STACK_NAMEevaled'
    assert config.release_tag == 'https://alufr-ros-pkg.googlecode.com/svn/tags/stacks/$STACK_NAME/$STACK_NAME-$STACK_VERSIONevaled'

    assert config.anon_dev == 'https://alufr-ros-pkg.googlecode.com/svn/trunk/$STACK_NAMEevaled'
    assert config.anon_distro_tag == 'https://alufr-ros-pkg.googlecode.com/svn/tags/distros/$RELEASE_NAME/stacks/$STACK_NAMEevaled'
    assert config.anon_release_tag == 'https://alufr-ros-pkg.googlecode.com/svn/tags/stacks/$STACK_NAME/$STACK_NAME-$STACK_VERSIONevaled'

    # load w anon rules
    config2 = SvnConfig()
    config.load(anon_rules, lambda x: x+'evaled')
    config2.load(anon_rules, lambda x: x+'evaled')
    for c in [config, config2]:
        assert c.anon_dev == 'http://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/trunkevaled'
        assert c.anon_distro_tag == 'http://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/tags/$RELEASE_NAMEevaled'
        assert c.anon_release_tag == 'http://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/tags/$STACK_NAME-$STACK_VERSIONevaled'
        assert c.dev == 'https://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/trunkevaled'
        assert c.distro_tag == 'https://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/tags/$RELEASE_NAMEevaled'
        assert c.release_tag == 'https://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/tags/$STACK_NAME-$STACK_VERSIONevaled'
