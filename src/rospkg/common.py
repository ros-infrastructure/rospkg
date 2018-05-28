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

"""
Common definitions for rospkg modules.
"""

MANIFEST_FILE = 'manifest.xml'
PACKAGE_FILE = 'package.xml'
STACK_FILE = 'stack.xml'
ROS_STACK = 'ros'


class ResourceNotFound(Exception):
    """
    A ROS filesystem resource was not found.
    """

    def __init__(self, msg, ros_paths=None, deps_sofar=None, deps_unavailable=None):
        """
        :type deps_sofar: [str]
        :param deps_sofar: List of depended packages at the time the command
                           stopped due to this exception.
        :type deps_unavailable: [str]
        :param deps_unavailable: List of packages defined in the dependency but are not
                                 available on the platform.
        """
        super(ResourceNotFound, self).__init__(msg)
        self.ros_paths = ros_paths
        self.deps_sofar = deps_sofar
        self.deps_unavailable = set()
        if deps_unavailable:
            self.deps_unavailable.update(deps_unavailable)

    def __str__(self):
        s = self.args[0]  # python 2.6
        if self.ros_paths:
            for i, p in enumerate(self.ros_paths):
                s = s + '\nROS path [%s]=%s' % (i, p)
        return s

    def get_depends(self):
        return self.deps_sofar
