# Copyright 2018 PlusOne Robotics Inc.
# Software License Agreement (BSD License)
#
# Copyright (c) 2018, PlusOne Robotics, Inc.
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
#  * Neither the name of PlusOne Robotics, Inc. nor the names of its
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

from collections import OrderedDict
import logging
from rospkg import ResourceNotFound, RosPack
import yaml


class LicenseUtil(object):

    def __init__(self):
        self.rp = RosPack()

    def compare_license(self, path_a="", path_b=""):
        """
        @summary Compare 2 files of license output and returns any new license entries.
        """
        ret = True
        stream_a = open(path_a, "r")
        yaml_a = yaml.load_all(stream_a)

        stream_b = open(path_b, "r")
        yaml_b = yaml.load_all(stream_b)

        # PyYaml doesn't preserve order of input yaml, so this is needed.
        # https://github.com/yaml/pyyaml/issues/110
        ordered_a = OrderedDict(sorted(list(yaml_a)[0].items()))
        ordered_b = OrderedDict(sorted(list(yaml_b)[0].items()))
        logging.debug("yaml_a: {}\nyaml_b: {}".format(ordered_a, ordered_b))
        # What to check?
        # - Key addition
        # - Values
        for key in ordered_a:
            if key not in ordered_b:
                logging.error("License '{}' was NOT present in the input file.".format(key))
                ret = False
            else:
                logging.info("License '{}' was present.".format(key))
        return ret

    def software_license(self, pkgname):
        """
        @return List of licenses and packages.
        @raise AttributeError, ResourceNotFound
        """
        if not pkgname:
            raise ValueError("Argument was insufficient: pkgname {}".format(pkgname))
        try:
            dict_license = self.rp.get_licenses(pkgname)
        except AttributeError as e:
            raise e
        except ResourceNotFound as e:
            URL_ISSUE_RELEVANT="https://github.com/ros-infrastructure/rospkg/pull/129#issue-168007083"
            logging.warn("{}\nRe-run get_licenses to work around an issue with get_depends (see {} if needed).".format(repr(e), URL_ISSUE_RELEVANT))
            dict_license = self.rp.get_licenses(pkgname)
        logging.debug(dict_license)
        return dict_license

    def save_licenses(
            self, licenses, pkgname, implicit=True, sortbylicense=True,
            prefix_outfile="/tmp/licenses", description_output=None):
        """
        @summary:  If True save the result of get_licenses to a text file.
        @param licenses: TBD
        @param implicit: Same as the one in get_depends
        @param sortbylicense: Same as the one in get_licenses
        @param prefix_outfile: Prefix of the output file in an absolute full path style.
                                              E.g. by default output of pkgA version 1.0.0 will be saved at:
                                                   /tmp/licenses_pkgA-1.0.0.log
        @param description_output: Description printed at the top of the output file.
        @return 1) License object, 2) Path of the resulted file (either absolute/relative
                       depending on the prefix_outfile)
        @raise ResourceNotFound
        """
        pkg_version = "pkgversion"
        if not description_output:
            description_output = "# Output of software license introspection started from {}.".format(pkgname)

        try:
            pkg_version = self.rp.get_manifest(pkgname).version
        except Exception as e:
            print(str(e))
        path_outputfile = '{}_{}-{}.yml'.format(prefix_outfile, pkgname, pkg_version)
        with open(path_outputfile, 'w') as outfile:
            outfile.write("{}\n".format(description_output))
            yaml.dump(licenses, outfile, default_flow_style=False, allow_unicode=True)
            logging.debug("Result saved at {}".format(path_outputfile))
        return licenses, path_outputfile
