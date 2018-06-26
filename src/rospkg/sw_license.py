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

from collections import defaultdict, OrderedDict
import logging
import yaml

from rospkg import ResourceNotFound, RosPack
from rospkg.environment import get_ros_root
from rospkg.os_detect import OsDetect


class SwLicenseException(Exception):
    """Software license detection problem occurred."""

    def __init__(self, msg=""):
        super(SwLicenseException, self).__init__(msg)


class LicenseUtil(object):
    _URL_ISSUE_RELEVANT = "https://github.com/ros-infrastructure/rospkg/pull/129#issue-168007083"

    def __init__(self, ros_paths=None):
        """
        :param ros_paths: Ordered list of paths to search for
                                      resources. If `None` (default), use environment ROS path.
        """
        self.rp = RosPack(ros_paths=ros_paths)
        self._os_detect = OsDetect()

    def compare_license(self, path_licensefile_new, path_licensefile_prev):
        """
        @summary Compare 2 files of license output and returns any new license entries.
        """
        if not (path_licensefile_new and path_licensefile_prev):
            raise ValueError(
                "Check if both 2 paths are passed and correct. What you passed are:\n"
                "- path_licensefile_new: {}\n"
                "- path_licensefile_prev: {}".format(path_licensefile_new, path_licensefile_prev))
        ret = True
        stream_a = open(path_licensefile_new, "r")
        yaml_new = yaml.load_all(stream_a)

        stream_b = open(path_licensefile_prev, "r")
        yaml_prev = yaml.load_all(stream_b)

        # PyYaml doesn't preserve order of input yaml, so this is needed.
        # https://github.com/yaml/pyyaml/issues/110
        set_new = set(sorted(list(yaml_new)[0]))
        set_prev = set(sorted(list(yaml_prev)[0]))
        logging.debug("yaml_new: {}\n\tyaml_prev: {}".format(set_new, set_prev))
        # What to check?
        # - Key addition
        # - Values
        set_new_found = set_new - set_prev
        set_removed_found = set_prev - set_new
        ERRMSG_NEWLICENSE_FOUND = "New license(s) '{}' found.".format(set_new_found)
        ERRMSG_LICENSES_REMOVED = "License(s) '{}' removed.".format(set_removed_found)
        if (set_new_found and not set_removed_found):
            raise SwLicenseException(ERRMSG_NEWLICENSE_FOUND)
        elif (not set_new_found and set_removed_found):
            raise SwLicenseException(ERRMSG_LICENSES_REMOVED)
        elif (set_new_found and set_removed_found):
            raise SwLicenseException("{}\n{}".format(
                ERRMSG_NEWLICENSE_FOUND, ERRMSG_LICENSES_REMOVED))

        logging.info("No new or removed license found.")
        return ret

    def software_license(self, pkgnames):
        """
        @type pkgnames: Either one of the following:
                    - [str]: list of str.
                    - str str...str: space separated string.
        @param pkgnames: Name of one or more packages to start software license
                       introspection from (i.e. leaf packages in the dependency chain).
        @return List of software licenses found in the dependency chain started from
                       the package names passed in 'pkgnames'. When multiple packages
                       passed to start with, union of all the results is returned.
        @raise AttributeError, ResourceNotFound
        """
        if not pkgnames:
            raise ValueError("Argument was insufficient: pkgname {}".format(pkgnames))

        # Check if pkgnames is str, not list.
        if isinstance(pkgnames, basestring):
            # If space(s) are found, 1) take it as a single package name if only one str
            # element is found. 2) Convert to [str] if multiple str elements found.
            pkgnames = pkgnames.split()

        # Could store multiple resulted dicts for a package
        dicts_of_result = []
        for pkg_name in pkgnames:
            try:
                dict_license = self.rp.get_licenses(pkg_name)
            except AttributeError as e:
                raise e
            except ResourceNotFound as e:
                logging.warn(
                    "{}\nRe-running Rospack.get_licenses to work around an issue with"
                    " get_depends (see {} if needed).".format(
                        repr(e), self._URL_ISSUE_RELEVANT))
                dict_license = self.rp.get_licenses(pkg_name)
            dicts_of_result.append(dict_license)

        # Take the union of the results.
        dict_licenses = self._union_dicts(dicts_of_result)
        logging.debug(dict_licenses)
        return dict_licenses

    def _union_dicts(self, d):
        """
        @param *d: dictionaries, each of which needs to be formatted as the output of
                       rospkg.RosPack.get_licenses (otherwise), i.e. { k, [d] }.
        @rtype { k, [d] }
        """
        # https://stackoverflow.com/a/14766978/577001

        logging.debug("d: {} len(d): {}\n".format(d, len(d)))

        newdicts = defaultdict(set)  # Define a defaultdict
        for each_dict in d:
            logging.debug("each_dict: {}\n".format(each_dict))
            #ordered_dic = OrderedDict(sorted(list(each_dict)[0].items()))
            ordered_dic = OrderedDict(sorted(each_dict.items()))

            # dict.items() returns a list of (k, v) tuple.
            # So, you can directly unpack the tuple in two loop variables.
            for k, v in ordered_dic.items():
                newdicts[k] |= set(v)

            logging.debug("newdicts: {}\n".format(newdicts))
        # And if you want the exact representation that you have shown
        # You can build a normal dict out of your newly built dict.
        union = {key: sorted(list(value)) for key, value in newdicts.items()}
        logging.debug(union)
        return union

    def save_licenses(
            self, licenses, pkgnames, implicit=True, sortbylicense=True,
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

        if isinstance(pkgnames, basestring):
            pkgnames = pkgnames.split()

        if not description_output:
            description_output = """# Output of software license introspection started from {}""".format(pkgnames)

        output_header = "{}\n# Environment this file was generated on:\n# - OS: {}\n# - ROS root: {}".format(
            description_output, self._os_detect.detect_os(), get_ros_root())

        pkgnames_versions = []
        for pkgname in pkgnames:
            try:
                pkg_version = self.rp.get_manifest(pkgname).version
                pkgnames_versions.append("{}-{}".format(pkgname, pkg_version))
            except Exception as e:
                print(str(e))

        # Delimits package name with underscore.
        pkgnames_versions_str = "_".join(pkgnames_versions)

        path_outputfile = '{}-{}.yml'.format(prefix_outfile, pkgnames_versions_str)
        with open(path_outputfile, 'w') as outfile:
            outfile.write("{}\n".format(output_header))
            yaml.dump(licenses, outfile, default_flow_style=False, allow_unicode=True)
            logging.debug("Result saved at {}".format(path_outputfile))
        return path_outputfile
