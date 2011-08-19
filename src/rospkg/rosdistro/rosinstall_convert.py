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
Conversion utilities for converting rosdistro files to rosinstall format
"""

from __future__ import print_function

from . vcs_config import get_vcs_configs
from . distro import InvalidDistro

def _get_tar(stack):
    name = '%s-%s'%(stack.name, stack.version)
    return 'https://code.ros.org/svn/release/download/stacks/%s/%s/%s.tar.bz2'%(stack.name, name, name)

def stack_to_rosinstall(stack, branch, anonymous=True):
    """
    Generate the rosinstall dictionary entry for a stack in the
    rosdistro.
    
    @param stack: A DistroStack for a particular stack
    @type  stack: L{DistroStack}
    @param branch: Select the branch or tag from 'devel', 'release' or 'distro' of the stack to checkout
    @type  branch: str
    @param anonymous: If True, use anonymous-access URLs if available (optional, default True).
    @type  anonymous: bool

    @raise InvalidDistro
    """
    result = []

    uri = None
    version = stack.version
    if not version and not branch == 'devel':
        print("Stack %s at version null, skipping"%stack.name)
        print("Can only get 'deve' branch from a stack at version null.")
        return result

    version_tag = None # to be conditionally filled later

    vcs = stack.vcs_config
    if not branch in ['devel', 'release', 'distro', 'release-tar']:
        raise InvalidDistro('Unsupported branch type %s for stack %s'%(branch, stack.name))
    if not vcs.type in get_vcs_configs().keys():
        raise InvalidDistro( 'Unsupported vcs type %s for stack %s'%(vcs.type, stack.name))

    if branch == 'release-tar':
        uri = _get_tar(stack)
        version_tag = '%s-%s'%(stack.name, stack.version)
        vcs_type = 'tar'
    else:
        vcs_type = vcs.type
        uri_version_tag = vcs.get_branch(branch, anonymous)

    if version_tag:
        result.append({vcs_type: {"uri": uri, 'local-name': stack.name, 'version': version_tag} } )
    else:
        result.append({vcs_type: {"uri": uri, 'local-name': stack.name} } )
    return result

def variant_to_rosinstall(variant_name, distro, branch, anonymous=True):
    rosinstall_dict = []
    variant = distro.variants.get(variant_name, None)
    if not variant:
        return []
    done = []
    for s in variant.stack_names_explicit:
        if s in distro.released_stacks and not s in done:
            done.append(s)
            rosinstall_dict.extend(stack_to_rosinstall(distro.stacks[s], branch, anonymous))
    return rosinstall_dict

def extended_variant_to_rosinstall(variant_name, distro, branch, anonymous=True):
    rosinstall_dict = []
    variant = distro.variants.get(variant_name, None)
    if not variant:
        return []
    done = [] # avoid duplicates
    for s in variant.stack_names:
        if s in distro.released_stacks and not s in done:
            done.append(s)
            rosinstall_dict.extend(stack_to_rosinstall(distro.stacks[s], branch, anonymous))
    return rosinstall_dict

def distro_to_rosinstall(distro, branch, anonymous=True):
    rosinstall_dict = []
    for s in distro.released_stacks.values():
        rosinstall_dict.extend(stack_to_rosinstall(s, branch, anonymous))
    return rosinstall_dict

