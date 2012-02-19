.. _rosstack:

rosstack
^^^^^^^^

rosstack overview
=================

*rosstack* is a command-line tool for retrieving information about ROS stacks
available on the filesystem. It implements a wide variety of commands
ranging from locating ROS stacks in the filesystem, to listing available
stacks, to calculating the dependency tree of stacks. It is also used in
the ROS build system for calculating build information for stacks.

For an equivalent tool for packages, see :ref:`rospack <rospack>`.

.. contents:: Table of Contents
   :depth: 2

rosstack usage
==============

The rosstack tool implements many commands that print information about ROS
stacks. All of these commands print their results to stdout. Any errors or
warnings go to stderr. This separation ensures that error output does not
confuse programs that execute rosstack as a subprocess to, for example,
recover build flags for a stack.

NOTE: for all commands, if `stack` is omitted, the current working
directory is used. 

::

    $ rosstack [options] <command> [stack]
    [rosstack] USAGE: rosstack [options] <command> [stack]
      Allowed commands:
        help
        find [stack]
        contents [stack]
        list
        list-names
        depends [stack] (alias: deps)
        depends-manifests [stack] (alias: deps-manifests)
        depends1 [stack] (alias: deps1)
        depends-indent [stack] (alias: deps-indent)
        depends-on [stack]
        depends-on1 [stack]
        depends-why --target=<target> [package] (alias: deps-why)
        contains [package]
        contains-path [package]
        profile [--length=<length>] 
    
     If [stack] is omitted, the current working directory
     is used (if it contains a stack.xml).


.. program:: rosstack

.. program:: rosstack help

rosstack help [subcommand]
--------------------------

Print help message.  Since 2.0.9, you can give a subcommand as an argument
to get more specific help.

.. _rosstack_find:
.. program:: rosstack find

rosstack find [stack]
---------------------

Print absolute path to the stack, empty string if stack is not found.

Example::

    $ rosstack find common
    /Users/homer/ros-pkg/common

.. program:: rosstack list

rosstack list
-------------

Print newline-separated list, ``<stack-name> <stack-dir>``, for all stacks. 

Example::

    $ rosstack list | grep common
    common /Users/kwc/ros-pkg/common
    common_msgs /Users/kwc/ros-pkg/common_msgs
    driver_common /Users/kwc/ros-pkg/driver_common
    image_common /Users/kwc/ros-pkg/image_common
    pr2_common /Users/kwc/ros-pkg/pr2_common
    visualization_common /Users/kwc/ros-pkg/visualization_common

.. program:: rosstack list-names

rosstack list-names
-------------------

Print newline-separated list of stack names for all stacks.

Example::

    $ rosstack list-names | grep common
    common
    common_msgs
    driver_common
    image_common
    pr2_common
    visualization_common

.. program:: rosstack list-duplicates

rosstack list-duplicates
------------------------

Print newline-separated list of names of stacks that appear more than
once during the search.

.. _rosstack_depends:

.. program:: rosstack depends

rosstack depends [stack]
------------------------

Print newline-separated, ordered list of all dependencies of the stack.

Example::

    $ rosstack depends driver_common
    ros
    common_msgs
    common
    diagnostics

.. program:: rosstack depends1

rosstack depends1 [stack]
-------------------------

Print newline-separated, ordered list of immediate dependencies of the
stack. 
   
.. program:: rosstack depends-manifests

rosstack depends-manifests [stack]
----------------------------------

Print space-separated, ordered list of stack.xml files for all
dependencies of the stack. 

.. program:: rosstack depends-indent

rosstack depends-indent [stack]
-------------------------------

Print newline-separated list of the entire dependency chain for the stack,
indented to indicate where in the chain each dependency arises. This may
contain duplicates.

.. program:: rosstack depends-why


rosstack depends-why --target=<target> [stack]
----------------------------------------------

Print newline-separated presentation of all dependency chains from the stack to ``<target>``.

.. _rosstack_depends-on:
.. program:: rosstack depends-on

rosstack depends-on [stack]
---------------------------

Print newline-separated list of all stacks that depend on the stack.

.. program:: rosstack depends-on1

rosstack depends-on1 [stack]
----------------------------

Print newline-separated list of all stacks that directly depend on the
stack. 

Example::

    $ rosstack depends-on1 driver_common
    camera_drivers
    image_pipeline
    laser_drivers
    pr2_robot

.. program:: rosstack contains

rosstack contains [package]
---------------------------

Print the name of the stack that contains the package.  If the containing stack cannot be found, returns non-zero.

Example::

    $ rosstack contains roscpp
    ros_comm

rosstack contains-path [package]
--------------------------------

Print the path to the stack that contains the package.  If the containing stack cannot be found, returns non-zero.

Example::

    $ rosstack contains-path roscpp
    /home/gerkey/code/ros_comm

.. _cmd_rosstack_profile:

.. program:: rosstack profile

rosstack profile
----------------

.. cmdoption:: --length=N

 Force a full crawl of stack directories (i.e., don't use cache, and report to console on the N (default 20) directories that took the longest time to crawl.  Useful for finding stray directories that are adversely affecting ``rosstack``'s performance.  

.. cmdoption:: --zombie-only

 Only print directories that do not have any manifests.  In this case, the output can be fed directly into ``rm`` to clean up your tree, e.g.::

     rosstack profile --zombie-only | xargs rm -rf

 NOTE: be sure to check the output before deleting any files!
