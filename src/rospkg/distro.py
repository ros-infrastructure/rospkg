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

"""
Representation/model of rosdistro format.
"""

import os
import sys
import urllib2
import yaml

TARBALL_URI_EVAL ='https://code.ros.org/svn/release/download/stacks/$STACK_NAME/$STACK_NAME-$STACK_VERSION/$STACK_NAME-$STACK_VERSION.tar.bz2'

class DistroException(Exception): pass

class InvalidDistro(DistroException): pass

def distro_uri(distro_name):
    """
    Get distro URI of main ROS distribution files.
    
    @param distro_name: name of distro, e.g. 'diamondback'
    @return: the SVN/HTTP URL of the specified distro.  This function should only be used
    with the main distros.
    """
    return "https://code.ros.org/svn/release/trunk/distros/%s.rosdistro"%(distro_name)

def expand_rule(rule, stack_name, stack_ver, release_name):
    s = rule.replace('$STACK_NAME', stack_name)
    if stack_ver:
        s = s.replace('$STACK_VERSION', stack_ver)
    s = s.replace('$RELEASE_NAME', release_name)
    return s

class DistroStack(object):
    """Stores information about a stack release"""

    def __init__(self, stack_name, stack_version, release_name, rules):
        """
        @param stack_name: Name of stack
        @param stack_version: Version number of stack.
        @param release_name: name of distribution release.  Necessary for rule expansion.
        @param rules: raw '_rules' data.  Will be converted into appropriate vcs config instance.
        """
        self.name = stack_name
        self.version = stack_version
        self.release_name = release_name
        self._rules = rules
        self.repo = rules.get('repo', None)
        self.vcs_config = load_vcs_config(self._rules, self._expand_rule)

    def _expand_rule(self, rule):
        """
        Perform variable substitution on stack rule.
        """
        return expand_rule(rule, self.name, self.version, self.release_name)
        
    def __eq__(self, other):
        return self.name == other.name and \
            self.version == other.version and \
            self.vcs_config == other.vcs_config

class Variant(object):
    """
    A variant defines a specific set of stacks ("metapackage", in Debian
    parlance). For example, "base", "pr2". These variants can extend
    another variant.
    """

    def __init__(self, variant_name, stack_names_implicit, raw_data):
        """
        @param variant_name: name of variant to load from distro file
        @type  variant_name: str
        @param stack_names_implicit: full list of stacks implicitly included in this variant
        @type  stack_names_implicit: [str]
        @param raw_data: raw rosdistro data for this variant

        @raise InvalidDistro
        """
        self.name = variant_name
        self.raw_data = raw_data
        self._stack_names_implicit = stack_names_implicit

    def get_parent_names(self):
        return self.raw_data.get('extends', [])

    def get_stack_names(self, implicit=True):
        if implicit:
            return self._stack_names_implicit
        else:
            return self.raw_data.get('stacks', [])
    
    parent_names = property(get_parent_names)

    # stack_names includes implicit stack names. Use get_stack_names()
    # to get explicit only
    stack_names  = property(get_stack_names)
    
class Distro(object):
    """
    Store information in a rosdistro file.
    """
    
    def __init__(self, stacks, variants, release_name, version, raw_data):
        """
        @param release_name: name of release, e.g. 'diamondback'
        @param version: version number of release
        @param raw_data: raw dictionary representation of a distro
        """
        self._stacks = stacks
        self.variants = variants
        self.release_name = release_name
        self.version = version
        self.raw_data = raw_data

    def get_stacks(self, released=False):
        """
        @param released: only included released stacks
        """
        if released:
            return _get_released_stacks()
        else:
            return self._stacks.copy()

    def _get_released_stacks(self):
        retval = {}
        for s, obj in self._stacks.items(): #py3k
            if obj.version:
                retval[s] = obj
        return retval

    stacks = property(get_stacks)
    released_stacks = property(_get_released_stacks)

def load_distro(source_uri):
    """
    @param source_uri: source URI of distro file, or path to distro file
    """
    try:
        # parse rosdistro yaml
        if os.path.isfile(source_uri):
            # load rosdistro file
            with open(source_uri) as f:
                raw_data = yaml.load(f.read())
        else:
            raw_data = yaml.load(urllib2.urlopen(source_uri))
    except yaml.YAMLError as e:
        raise InvalidDistro(str(e))

    try:
        stack_props = y['stacks']
        stack_names = [x for x in stack_props.keys() if not x[0] == '_']
        version = _distro_version(raw_data.get('version', '0'))
        release_name = raw_data['release']

        variants = {}
        for props in y['variants']:
            if len(props.keys()) != 1:
                raise InvalidDistro("invalid variant spec: %s"%props)
            n = props.keys()[0]
            variants[n] = _load_variant(v, varaint_props)

        stacks = _load_distro_stacks(raw_data, stack_names, release_name)
        return Distro(stacks, variants, release_name, version, raw_data)
    except KeyError as e:
        raise InvalidDistro("distro is missing required '%s' key"%(str(e)))

def _load_variant(variant_name, variants_raw_data):
    # save the properties for this variant
    raw_data = variants_raw_data[variant_name]
    if not 'stacks' in raw_data and not 'extends' in raw_data:
        raise InvalidDistro("variant properties must define 'stacks' or 'extends':\n%s"%(raw_data))

    # stack_names accumulates the full expanded list
    stack_names_implicit = list(raw_data.get('stacks', []))
    if 'extends' in raw_data:
        extends = raw_data['extends']
        if type(extends) == type('str'):
            extends = [extends]

        for e in extends:
            parent_variant = _load_variant(e, variants_raw_data)
            stack_names_implicit = parent_variant.get_stack_names(implicit=True) + stack_names_implicit

    return Variant(variant_name, stack_names_implicit, raw_data)
    
def _load_distro_stacks(distro_doc, stack_names, release_name):
    """
    @param distro_doc: dictionary form of rosdistro file
    @type distro_doc: dict
    @param stack_names: names of stacks to load
    @type  stack_names: [str]
    @return: dictionary of stack names to DistroStack instances
    @rtype: {str : DistroStack}
    @raise DistroException: if distro_doc format is invalid
    """

    # load stacks and expand out uri rules
    stacks = {}
    try:
        stack_props = distro_doc['stacks']
    except KeyError:
        raise DistroException("distro is missing required 'stacks' key")
    for stack_name in stack_names:
        # ignore private keys like _rules
        if stack_name[0] == '_':
            continue

        stack_version = stack_props[stack_name].get('version', None)
        rules = get_rules(distro_doc, stack_name)
        stacks[stack_name] = DistroStack(stack_name, stack_version, release_name, rules)
    return stacks

def _distro_version(version_val):
    """
    Parse distro version value, converting SVN revision to version value if necessary
    """
    version_val = str(version_val)
    m = re.search('\$Revision:\s*([0-9]*)\s*\$', version_val)
    if m is not None:
        version_val = 'r'+m.group(1)

    # Check that is a valid version string
    valid = string.ascii_letters + string.digits + '.+~'
    if False in (c in valid for c in version_val):
        raise InvalidDistro("Version string %s not valid"%version_val)
    return version_val

def distro_to_rosinstall(distro, branch, variant_name=None, implicit=True, released_only=True, anonymous=True):
    """
    @param branch: branch to convert for
    @param variant_name: if not None, only include stacks in the specified variant.
    @param implicit: if variant_name is provided, include full (recursive) dependencies of variant, default True
    @param released_only: only included released stacks, default True.
    @param anonymous: create for anonymous access rules

    @raise KeyError: if branch is invalid or if distro is mis-configured
    """
    variant = distro.variants.get(variant_name, None)
    if variant_name:
        if implicit:
            stack_names = set(variant.stack_names)
        else:
            stack_names = set(variant.stack_names_explicit)
    else:
        stack_names = distro.released_stacks.keys()
    rosinstall_data = []
    for s in stack_names:
        if released_only and not s in distro.released_stacks:
            continue
        rosinstall_data.extend(distro.stacks[s].vcs_config.to_rosinstall(s, branch, anonymous))
    return rosinstall_data

class _VcsConfig(object):

    def __init__(self, type_):
        self.type = type_
        self.tarball_url = None
        
    def to_rosinstall(self, local_name, branch, anonymous):
        uri, version_tag = self.get_branch(branch, anonymous)
        if branch == 'release-tar':
            type_ = 'tar'
        else:
            type_ = self.type
        if version_tag:
            return [{type_: {"uri": uri, 'local-name': local_name, 'version': version_tag} } ]
        else:
            return [({type_: {"uri": uri, 'local-name': local_name} } )]
        
    def load(self, rules, rule_eval):
        self.tarball_url = rule_eval(TARBALL_URI_EVAL)
        
    def get_branch(self, branch, anonymous):
        """
        @raise ValueError: if branch is invalid
        """
        if branch == 'release-tar':
            return self.tarball_url, None
        else:
            raise ValueError(branch)

    def __eq__(self, other):
        return self.type == other.type and \
               self.tarball_url == other.tarball_url

class _DvcsConfig(_VcsConfig):
    """
    Configuration information for a distributed VCS-style repository.

     * repo_uri: base URI of repo
     * dev_branch: git branch the code is developed
     * distro_tag: a tag of the latest released code for a specific ROS distribution
     * release_tag: a tag of the code for a specific release
    """

    def __init__(self, type_):
        super(_DvcsConfig, self).__init__(type_)
        self.repo_uri = self.anon_repo_uri = None
        self.dev_branch = self.distro_tag = self.release_tag   = None

    def load(self, rules, rule_eval):
        super(_DvcsConfig, self).load(rules, rule_eval)

        self.repo_uri = rule_eval(rules['uri'])
        if 'anon-uri' in rules:
            self.anon_repo_uri = rule_eval(rules['anon-uri'])
        else:
            self.anon_repo_uri = self.repo_uri
        self.dev_branch  = rule_eval(rules['dev-branch'])
        self.distro_tag  = rule_eval(rules['distro-tag'])
        self.release_tag = rule_eval(rules['release-tag'])
        
    def get_branch(self, branch, anonymous):
        """
        @raise KeyError: invalid branch parameter 
        """
        if branch == 'release-tar':
            return super(_DvcsConfig, self).get_branch(branch, anonymous)            
        elif branch == 'devel':
            version_tag = self.dev_branch
        elif branch == 'distro':
            version_tag = self.distro_tag
        elif branch == 'release':
            version_tag = self.release_tag
        else:
            raise ValueError("invalid branch spec [%s]"%(branch))
        # occurs, for example, with unreleased stacks.  Only devel is valid
        if version_tag is None:
            raise ValueError("branch [%s] is not available for this config"%(branch))
        if anonymous:
            return self.anon_repo_uri, version_tag
        else:
            return self.repo_uri, version_tag            
        
    def __eq__(self, other):
        return super(_DvcsConfig, self).__eq__(other) and \
               self.repo_uri == other.repo_uri and \
               self.anon_repo_uri == other.anon_repo_uri and \
               self.dev_branch == other.dev_branch and \
               self.release_tag == other.release_tag and \
               self.distro_tag == other.distro_tag
    
class GitConfig(_DvcsConfig):
    """
    Configuration information about an GIT repository
    """

    def __init__(self):
        super(GitConfig, self).__init__('git')

class HgConfig(_DvcsConfig):
    """
    Configuration information about a Mercurial repository.
    """

    def __init__(self):
        super(HgConfig, self).__init__('hg')

class BzrConfig(_DvcsConfig):
    """
    Configuration information about an BZR repository.
    
     * repo_uri: base URI of repo
     * dev_branch: hg branch the code is developed
     * distro_tag: a tag of the latest released code for a specific ROS distribution
     * release_tag: a tag of the code for a specific release
     """

    def __init__(self):
        super(BzrConfig, self).__init__('bzr')

class SvnConfig(_VcsConfig):
    """
    Configuration information about an SVN repository.

     * dev: where the code is developed
     * distro_tag: a tag of the code for a specific ROS distribution
     * release_tag: a tag of the code for a specific release
    """
    
    def __init__(self):
        super(SvnConfig, self).__init__('svn')
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
        super(SvnConfig, self).load(rules, rule_eval)
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
        """
        @raise ValueError: if branch is invalid
        """
        if branch == 'release-tar':
            return super(SvnConfig, self).get_branch(branch, anonymous)
        else:
            key_map = dict(devel='dev', distro='distro_tag', release='release_tag')
            if not branch in key_map:
                raise KeyError("invalid branch spec [%s]"%(branch))
            attr_name = key_map[branch]
            if anonymous:
                attr_name = 'anon_'+attr_name
            uri = getattr(self, attr_name)
        # occurs, for example, with unreleased stacks.  Only devel is valid
        if uri is None:
            raise ValueError("branch [%s] is not available for this config"%(branch))
        return uri, None
        
    def __eq__(self, other):
        return super(SvnConfig, self).__eq__(other) and \
               self.dev == other.dev and \
               self.distro_tag == other.distro_tag and \
               self.release_tag == other.release_tag and \
               self.anon_dev == other.anon_dev and \
               self.anon_distro_tag == other.anon_distro_tag and \
               self.anon_release_tag == other.anon_release_tag

_vcs_configs = {
    'svn': SvnConfig,
    'git': GitConfig,
    'hg': HgConfig,    
    'bzr': BzrConfig,    
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
