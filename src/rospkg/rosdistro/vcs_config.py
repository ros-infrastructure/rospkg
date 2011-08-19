# Software License Agreement (BSD License)
#
# Copyright (c) 2010, Willow Garage, Inc.
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
#
# Revision $Id: distro.py 10301 2010-07-09 01:21:23Z kwc $

"""
VCS configuration objects to load and represent rosdistro 'rules'
"""

class DVCSConfig(object):
    """
    Configuration information for a distributed VCS-style repository.

     * repo_uri: base URI of repo
     * dev_branch: git branch the code is developed
     * distro_tag: a tag of the latest released code for a specific ROS distribution
     * release_tag: a tag of the code for a specific release
    """

    def __init__(self, type_):
        self.type = type_
        self.repo_uri      = None
        self.anon_repo_uri = None
        self.dev_branch    = None
        self.distro_tag    = None
        self.release_tag   = None

    def load(self, rules, rule_eval):
        self.repo_uri = rule_eval(rules['uri'])

        if 'anon-uri' in r:
            self.anon_repo_uri = rule_eval(rules['anon-uri'])
        else:
            self.anon_repo_uri = self.repo_uri

        self.dev_branch  = rule_eval(rules['dev-branch'])
        self.distro_tag  = rule_eval(rules['distro-tag'])
        self.release_tag = rule_eval(rules['release-tag'])
        
    def get_branch(self, branch, anonymous):
        if anonymous:
            uri = self.anon_repo_uri
        else:
            uri = self.repo_uri
        if branch == 'devel':
            version_tag = self.dev_branch
        elif branch == 'distro':
            version_tag = self.distro_tag
        elif branch == 'release':
            version_tag = self.release_tag
        return uri, version_tag
        
    def __eq__(self, other):
        return self.type == other.type and \
               self.repo_uri == other.repo_uri and \
               self.anon_repo_uri == other.anon_repo_uri and \
               self.dev_branch == other.dev_branch and \
               self.release_tag == other.release_tag and \
               self.distro_tag == other.distro_tag
    
class GITConfig(DVCSConfig):
    """
    Configuration information about an GIT repository
    """

    def __init__(self):
        super(GITConfig, self).__init__('git')

class HGConfig(DVCSConfig):
    """
    Configuration information about a Mercurial repository.
    """

    def __init__(self):
        super(HGConfig, self).__init__('bzr')

class BZRConfig(DVCSConfig):
    """
    Configuration information about an BZR repository.
    
     * repo_uri: base URI of repo
     * dev_branch: hg branch the code is developed
     * distro_tag: a tag of the latest released code for a specific ROS distribution
     * release_tag: a tag of the code for a specific release
     """

    def __init__(self):
        super(BZRConfig, self).__init__('bzr')

class SVNConfig(object):
    """
    Configuration information about an SVN repository.

     * dev: where the code is developed
     * distro_tag: a tag of the code for a specific ROS distribution
     * release_tag: a tag of the code for a specific release
    """
    
    def __init__(self):
        self.type = 'svn'
        self.dev = None
        self.distro_tag = None
        self.release_tag = None

        # anonymously readable version of URLs above. Some repos have
        # separate URLs for read-only vs. writable versions of repo
        # and many tools need to be able to read repos without
        # providing credentials.
        self.anon_dev         = None
        self.anon_distro_tag  = None
        self.anon_release_tag = None

    def load(self, rules, rule_eval):
        for k in ['dev', 'distro-tag', 'release-tag']:
            if not k in rules:
                raise KeyError("svn rules missing required %s key: %s"%(k, rules))
        self.dev = rule_eval(rules['dev'])
        self.distro_tag  = rule_eval(rules['distro-tag'])
        self.release_tag = rule_eval(rules['release-tag'])

        # specify urls that are safe to anonymously read
        # from. Users must supply a complete set.
        if 'anon-dev' in rules:
            self.anon_dev = rule_eval(rules['anon-dev'])
            self.anon_distro_tag = rule_eval(rules['anon-distro-tag'])                
            self.anon_release_tag = rule_eval(rules['anon-release-tag'])
        else:
            # if no login credentials, assume that anonymous is
            # same as normal keys.
            self.anon_dev = self.dev
            self.anon_distro_tag = self.distro_tag
            self.anon_release_tag = self.release_tag
        
    def get_branch(self, branch, anonymous):
        if branch == 'devel':
            if anonymous: 
                uri = self.anon_dev
            else:
                uri = self.dev
        elif branch == 'distro':
            if anonymous: 
                uri = self.anon_distro_tag
            else:
                uri = self.distro_tag
        elif branch == 'release':
            if anonymous: 
                uri = self.anon_release_tag
            else:
                uri = self.release_tag
        return uri, None
        
    def __eq__(self, other):
        return self.dev == other.dev and \
            self.distro_tag == other.distro_tag and \
            self.release_tag == other.release_tag and \
            self.anon_dev == other.anon_dev and \
            self.anon_distro_tag == other.anon_distro_tag and \
            self.anon_release_tag == other.anon_release_tag

_vcs_configs = {
    'svn': SVNConfig,
    'git': GITConfig,
    'hg': HGConfig,    
    'bzr': BZRConfig,    
    }

def get_vcs_configs():
    return _vcs_configs.copy()

def load_vcs_config(rules, rule_eval):
    vcs_config = None
    for k, clazz in _vcs_configs.items():
        if k in rules:
            vcs_config = clazz()
            vcs_config.load(rules[k], rule_eval)
            break
    return vcs_config
    
