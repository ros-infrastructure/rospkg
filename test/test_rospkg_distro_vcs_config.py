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

default_rules = {}
rosinstalls = {}
default_rules['git'] = {'git': {'anon-uri': 'https://github.com/ipa320/$STACK_NAME.git',
                                'dev-branch': 'release_electric',
                                'distro-tag': '$RELEASE_NAME',
                                'release-tag': '$STACK_NAME-$STACK_VERSION',
                                'uri': 'git@github.com:ipa320/$STACK_NAME.git'}}
rosinstalls['git'] = {}
rosinstalls['git']['release-tar'] = [{'tar': {'local-name': 'local_name',
                                              'uri': 'https://code.ros.org/svn/release/download/stacks/$STACK_NAME/$STACK_NAME-$STACK_VERSION/$STACK_NAME-$STACK_VERSION.tar.bz2evaled'}}]
rosinstalls['git']['devel'] = [{'git': {'local-name': 'local_name',
                                        'version': 'release_electricevaled',
                                        'uri': 'https://github.com/ipa320/$STACK_NAME.gitevaled'}}]
rosinstalls['git']['release'] = [{'git': {'local-name': 'local_name',
                                          'version': '$STACK_NAME-$STACK_VERSIONevaled',
                                          'uri': 'https://github.com/ipa320/$STACK_NAME.gitevaled'}}]
rosinstalls['git']['distro'] = [{'git': {'local-name': 'local_name',
                                         'version': '$RELEASE_NAMEevaled',
                                         'uri': 'https://github.com/ipa320/$STACK_NAME.gitevaled'}}]
default_rules['svn'] = {'svn': {'dev': 'https://alufr-ros-pkg.googlecode.com/svn/trunk/$STACK_NAME',
                                'distro-tag': 'https://alufr-ros-pkg.googlecode.com/svn/tags/distros/$RELEASE_NAME/stacks/$STACK_NAME',
                                'release-tag': 'https://alufr-ros-pkg.googlecode.com/svn/tags/stacks/$STACK_NAME/$STACK_NAME-$STACK_VERSION'}}
rosinstalls['svn'] = {}
rosinstalls['svn']['release-tar'] = rosinstalls['git']['release-tar']
rosinstalls['svn']['devel'] = [{'svn': {'local-name': 'local_name',
                                        'uri': 'https://alufr-ros-pkg.googlecode.com/svn/trunk/$STACK_NAMEevaled',
                                        }}]
rosinstalls['svn']['release'] = [{'svn': {'local-name': 'local_name',
                                          'uri': 'https://alufr-ros-pkg.googlecode.com/svn/tags/stacks/$STACK_NAME/$STACK_NAME-$STACK_VERSIONevaled',
                                          }}]
rosinstalls['svn']['distro'] = [{'svn': {'local-name': 'local_name',
                                          'uri': 'https://alufr-ros-pkg.googlecode.com/svn/tags/distros/$RELEASE_NAME/stacks/$STACK_NAMEevaled',
                                          }}]
default_rules['hg'] = {'hg': {'dev-branch': 'default',
                              'distro-tag': '$RELEASE_NAME',
                              'release-tag': '$STACK_NAME-$STACK_VERSION',
                              'uri': 'https://kforge.ros.org/navigation/navigation'}}
default_rules['bzr'] = {'bzr': {'anon-uri': 'lp:sr-ros-interface',
                                'dev-branch': 'stable',
                                'distro-tag': '$RELEASE_NAME',
                                'release-tag': '$STACK_NAME-$STACK_VERSION',
                                'uri': 'bzr+ssh://bazaar.launchpad.net/~shadowrobot/sr-ros-interface'}}

def test_to_rosinstall():
    from rospkg.distro import load_vcs_config
    rule_eval = lambda x: x+'evaled'
    anonymous = True
    #TODO: for branch in ['devel', 'release', 'distro']:
    for vcs in ['git', 'svn']:
        vcs_config = load_vcs_config(default_rules[vcs], rule_eval)
        for branch in ['release', 'distro', 'release-tar', 'devel']:
            retval = vcs_config.to_rosinstall('local_name', branch, anonymous)
            assert retval == rosinstalls[vcs][branch], "%s %s:\n%s\nvs.\n%s"%(vcs, branch, retval, rosinstalls[vcs][branch])
    
def test_VcsConfig():
    from rospkg.distro import VcsConfig
    vcs_config = VcsConfig('fake')
    vcs_config.tarball_url = 'http://foo'
    assert 'fake' == vcs_config.type
    for b in ['devel', 'release', 'distro']:
        try:
            vcs_config.get_branch(b, False)
            assert False, "should have raised"+b
        except ValueError: pass
    for anon in [True, False]:
        assert ('http://foo', None) == vcs_config.get_branch('release-tar', anon)
    
def test_BZRConfig():
    from rospkg.distro import BzrConfig
    anon_rules = default_rules['bzr']['bzr']
    rules = anon_rules.copy()
    rules['uri'] = rules['anon-uri']
    del rules['anon-uri']

    config = BzrConfig()
    anon_config = BzrConfig()

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

    repo_uri = anon_rules['uri']+'evaled'
    anon_repo_uri = anon_rules['anon-uri']+'evaled'
    assert config.repo_uri == anon_repo_uri, config.repo_uri
    assert config.anon_repo_uri == anon_repo_uri, config.anon_repo_uri
    assert anon_config.repo_uri == repo_uri, anon_config.repo_uri
    for c in [config, anon_config]:
        assert c.dev_branch == 'stableevaled'
        assert c.distro_tag == '$RELEASE_NAMEevaled'
        assert c.release_tag == '$STACK_NAME-$STACK_VERSIONevaled'
        assert c.anon_repo_uri == anon_repo_uri

    c = anon_config
    assert c.get_branch('devel', False) == (repo_uri, 'stableevaled')
    assert c.get_branch('devel', True) == (anon_repo_uri, 'stableevaled')
    assert c.get_branch('distro', False) == (repo_uri, '$RELEASE_NAMEevaled')
    assert c.get_branch('distro', True) == (anon_repo_uri, '$RELEASE_NAMEevaled')
    assert c.get_branch('release', False) == (repo_uri, '$STACK_NAME-$STACK_VERSIONevaled')
    assert c.get_branch('release', True) == (anon_repo_uri, '$STACK_NAME-$STACK_VERSIONevaled')
    try:
        c.get_branch('foo', True)
        assert False
    except ValueError:
        pass
    # setup for coverage -- invalidate release branch
    rel_tag = c.release_tag
    c.release_tag = None
    try:
        assert c.get_branch('release', False)
        assert False
    except ValueError:
        pass
    c.release_tag = rel_tag
    
    # test equals
    config2 = BzrConfig()
    config2.load(rules, lambda x: x+'evaled')
    assert config == config2
    anon_config2 = BzrConfig()    
    anon_config2.load(anon_rules, lambda x: x+'evaled')
    assert anon_config == anon_config2

    # test eq
    config_check = BzrConfig()
    config_check_eq = BzrConfig()
    config_check_neq = BzrConfig()
    config_check.load(rules, lambda x: x+'evaled')
    config_check_eq.load(rules, lambda x: x+'evaled')
    config_check_neq.load(anon_rules, lambda x: x+'evaled')
    assert config_check == config_check_eq
    assert config_check != config_check_neq

def test_HgConfig():
    from rospkg.distro import HgConfig
    anon_rules = {
        'dev-branch': 'default',
        'distro-tag': '$RELEASE_NAME',
        'release-tag': '$STACK_NAME-$STACK_VERSION',
        'anon-uri': 'https://kforge.ros.org/navigation/navigation',
        'uri': 'ssh://user@kforge.ros.org/navigation/navigation'
        }
    rules = default_rules['hg']['hg'] 

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

    # test eq
    config_check = HgConfig()
    config_check_eq = HgConfig()
    config_check_neq = HgConfig()
    config_check.load(rules, lambda x: x+'evaled')
    config_check_eq.load(rules, lambda x: x+'evaled')
    config_check_neq.load(anon_rules, lambda x: x+'evaled')
    assert config_check == config_check_eq
    assert config_check != config_check_neq

def test_GitConfig():
    from rospkg.distro import GitConfig
    anon_rules = default_rules['git']['git']
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
    from rospkg.distro import SvnConfig
    config = SvnConfig()
    required = ['dev', 'distro-tag', 'release-tag']
    rules = default_rules['svn']['svn']

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

    # test eq
    config_check = SvnConfig()
    config_check_eq = SvnConfig()
    config_check_neq = SvnConfig()
    config_check.load(rules, lambda x: x+'evaled')
    config_check_eq.load(rules, lambda x: x+'evaled')
    config_check_neq.load(anon_rules, lambda x: x+'evaled')
    assert config_check == config_check_eq
    assert config_check != config_check_neq
    
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

    # test get_branch
    assert c.get_branch('devel', True) == ('http://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/trunkevaled', None)
    assert c.get_branch('distro', True) == ('http://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/tags/$RELEASE_NAMEevaled', None)
    assert c.get_branch('release', True) == ('http://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/tags/$STACK_NAME-$STACK_VERSIONevaled', None)
    assert c.get_branch('devel', False) == ('https://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/trunkevaled', None)
    assert c.get_branch('distro', False) == ('https://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/tags/$RELEASE_NAMEevaled', None)
    assert c.get_branch('release', False) == ('https://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/tags/$STACK_NAME-$STACK_VERSIONevaled', None)

    # get full coverage on get_branch()
    try:
        c.get_branch('fake', False)
        assert False
    except KeyError:
        pass
    # setup for coverage -- invalidate release branch
    rel_tag = c.release_tag
    c.release_tag = None
    try:
        assert c.get_branch('release', False)
        assert False
    except ValueError:
        pass
    c.release_tag = rel_tag

def test_load_vcs_config():
    from rospkg.distro import load_vcs_config, get_vcs_configs
    for t in ['svn', 'git', 'hg', 'bzr']:
        assert t in get_vcs_configs()
        config = load_vcs_config(default_rules[t], lambda x: x+'evaled')
        assert config.type == t, t
