.. _rospack:

rospack
^^^^^^^

rospack overview
================

*rospack* is the ROS package management tool. rospack is part
``dpkg``, part ``pkg-config``.  

The main function of ``rospack`` is to crawl through the packages in
:envvar:`ROS_ROOT` and :envvar:`ROS_PACKAGE_PATH`, read and parse the
:ref:`manifest.xml <manifest_file>` for each package, and assemble a
complete dependency tree for all packages.


Using this tree, ``rospack`` can answer a number of queries about
packages and their dependencies.  Common queries include:

 - :ref:`rospack find <rospack_find>` : return the absolute path to a package
 - :ref:`rospack depends <rospack_depends>` : return a list of all of a package's dependencies
 - :ref:`rospack depends-on <rospack_depends-on>` : return a list of packages that depend on the given package
 - :ref:`rospack export <rospack_export>` : return flags necessary for building and linking against a package

rospack is intended to be cross-platform.

.. seealso::

   :ref:`Package manifests <manifest_file>`
      Documentation on ``manifest.xml`` files, which ``rospack`` crawls and extracts information from.

   `rosbuild <http://ros.org/wiki/rosbuild>`_
      Documentation for the rosbuild system, which makes heavy use of the rospack commands

   `rosmake <http://ros.org/wiki/rosmake>`_
      Documentation for the rosmake command, which makes heavy use of the rospack commands



.. contents:: Table of Contents
   :depth: 2


Crawling algorithm
------------------

``rospack`` crawls the directory specified by the environment variable
:envvar:`ROS_ROOT`.  It then crawls the colon-separated directories in
:envvar:`ROS_PACKAGE_PATH`, in the ordered they are listd, determining
a directory to be package if it contains a file called
:ref:`manifest.xml <manifest_file>`.

If such a file is found, the directory containing it is considered to
be a ROS package, with the package name equal to the directory name.
The crawl does not descend further once a manifest is found (i.e.
packages cannot be nested inside one another).

If a ``manifest.xml`` file is not found in a given directory, each
subdirectory is searched.  This subdirectory search is prevented if a
file called ``rospack_nosubdirs`` is found.  The directory itself is
still searched for a manifest, but its subdirectories are not crawled.

If multiple packages by the same name exist within the search path, the
first one found wins.  It is strongly recommended that you keep packages by
the same name in separate trees, each having its own element within
:envvar:`ROS_PACKAGE_PATH`.  That way, you can deterministically control the search
order by the way that you specify :envvar:`ROS_PACKAGE_PATH`.  The search order
within a given element of :envvar:`ROS_PACKAGE_PATH` can be unpredictably affected by
the details of how files are laid out on disk.

Efficiency considerations
'''''''''''''''''''''''''

rospack re-parses the ``manifest.xml`` files and rebuilds the
dependency tree on each execution.  However, it maintains a cache of
package directories in ``ROS_ROOT/.rospack_cache``.  This cache is
updated whenever there is a cache miss, or when the cache is 60
seconds old.  You can change this timeout by setting the environment
variable :envvar:`ROS_CACHE_TIMEOUT`, in seconds.  Set it to 0.0 to force a
cache rebuild on every invocation of rospack.

rospack's performance can be adversely affected by the presence of
very broad and/or deep directory structures that don't contain
manifest files.  If such directories are in rospack's search path, it
can spend a lot of time crawling them only to discover that there are
no packages to be found.  You can prevent this latency by creating a
``rospack_nosubdirs`` file in such directories. If rospack seems to be
running annoyingly slowly, you can use the :ref:`profile command <cmd_rospack_profile>`, which will print out the 20 slowest trees to crawl
(or use ``profile --length=N`` to print the slowest N trees).

rospack_nosubdirs
-----------------

You can prevent rospack from descending into a directory by simply
adding an empty ``rospack_nosubdirs`` file.  This is useful when you
want to block off part of your package tree, either for performance
reasons, or to hide another version of your code. 

We recommend creating a ``rospack_nosubdirs`` file in packages that
checkout code from other code repositories, as those often create big
directory trees that don't get cleaned up if a package is moved or
deleted.

NOTE: the ``rospack_nosubdirs`` directive only affects the ``rospack`` tool.
It is not observed by tools like ``roslaunch`` or ``rosrun``.


rospack usage
=============

The ``rospack`` tool implements many commands that print information
about ROS packages. All of these commands print their results to
stdout.  Any errors or warnings go to stderr.  This separation ensures
that error output does not confuse programs that execute ``rospack``
as a subprocess to, for example, recover build flags for a package.

.. program:: rospack

General options
---------------

.. cmdoption:: -q

  The `-q` option can be given after any subcommand.  It will suppress most error messages that usually go to stderr.  The return code will still be non-zero, to indicate the error.  E.g., to search for a package, but suppress the error message if it's not found::

    $ rospack find -q foo
    $ echo $?
    255

NOTE: for all commands, if ``[package]`` is omitted, the current
working directory is used.


.. program:: rospack help

rospack help
------------

Print help message.

.. _rospack_find:
.. program:: rospack find

rospack find [package]
----------------------

Print absolute path to the package, empty string if package is not found. This is used within many tools, including rosbuild.

Example::

    $ rospack find roscpp
    /Users/homer/code/ros/core/roscpp
  

.. program:: rospack list
rospack list
------------

Print newline-separated list, ``<package-name> <package-dir>``, for all packages. 

Example::

    $ rospack list | grep visualization
    wxpropgrid /home/kwc/ros-pkg/visualization/wxpropgrid
    rviz /home/kwc/ros-pkg/visualization/rviz
    visualization_msgs /home/kwc/ros-pkg/visualization_common/visualization_msgs
    ogre /home/kwc/ros-pkg/visualization_common/ogre
    ogre_tools /home/kwc/ros-pkg/visualization_common/ogre_tools
 

.. program:: rospack list-names

Print newline-separated list of packages names for all packages.

.. program:: rospack langs

rospack langs
-------------

Print space-separated list of available language-specific client
libraries. The client library list is calculated as the list of
packages that depend directly on the placeholder package "roslang",
minus any packages that are listed in the environment variable
:envvar:`ROS_LANG_DISABLE`.


Example::

    $ rospack langs
    roscpp rospy


.. _rospack_depends:

.. program:: rospack depends

rospack depends [package]
-------------------------

Print newline-separated, ordered list of all dependencies of the package. This is used within ``rosmake``. 

Example::

    $ rospack depends map_server
    gtest
    genmsg_cpp
    roslib
    xmlrpc++
    rosthread
    roscpp
    std_msgs
    std_srvs
    sdl
    ijg_libjpeg
    sdl_image


.. program:: rospack depends1

rospack depends1 [package]
--------------------------

Print newline-separated, ordered list of immediate dependencies of the package.
   
.. program:: rospack depends-manifests

rospack depends-manifests [package]
-----------------------------------

Print space-separated, ordered list of manifest files for all dependencies of the package. This is used by rosbuild to create explicit dependencies from source files to other packages' manifests.

.. program:: rospack depends-indent

rospack depends-indent [package]
--------------------------------

Print newline-separated list of the entire dependency chain for the package, indented to indicate where in the chain each dependency arises.  This may contain duplicates.

.. program:: rospack depends-why


rospack depends-why --target=<target> [package]
-----------------------------------------------

Print newline-separated presentation of all dependency chains from the package to ``<target>``.


.. _rospack_depends-on:
.. program:: rospack depends-on

rospack depends-on [package]
----------------------------

Print newline-separated list of all packages that depend on the package.

.. program:: rospack depends-on1

rospack depends-on1 [package]
-----------------------------

Print newline-separated list of all packages that directly depend on the package. 

Example::

    $ rospack depends-on1 roslang
    roscpp
    rospy
    rosoct
    roslisp

 
.. _rospack_export:
.. program:: rospack export

rospack export --lang=LANGUAGE --attrib=ATTRIBUTE [package]
-----------------------------------------------------------

Print space-separated list of [export][LANGUAGE ATTRIBUTE=""/][/export] values from the manifest of the package and its dependencies.  

This is useful for getting language-specific build flags, e.g,. export/cpp/cflags.

.. cmdoption:: --deps-only

 If `--deps-only` is provided, then the package itself is excluded.  

 
.. program:: rospack cflag-only-I, cflags-only-other

rospack cflag-only-I, cflags-only-other
---------------------------------------

NOTE: the ``cflags-only-*`` commands are simply variants of the :ref:`rospack export <rospack_export>` command with additional processing.

.. cmdoption:: cflags-only-I [package]

 Print space-separated list of export/cpp/cflags that start with ``-I``.  This is used by rosbuild to assemble include paths for compiling.

.. cmdoption:: cflags-only-other [package]

 Print space-separated list of export/cpp/cflags that don't start with ``-I``. This is used by rosbuild to assemble non-include compile flags.

.. cmdoption:: --deps-only

 If :option:`--deps-only` is provided, then the package itself is excluded.  This can be used with all ``cflags-only-*`` variants.

rospack libs-only-L, libs-only-l, libs-only-other
-------------------------------------------------

.. program:: rospack libs-only-L, libs-only-l, libs-only-other

NOTE: the ``libs-only-*`` commands are simply variants of the :ref:`rospack export <rospack_export>` command with additional processing.

.. cmdoption:: libs-only-L [package]

 Print space-separated list of export/cpp/libs that start with ``-L``.  If --deps-only is provided, then the package itself is excluded. This is used by rosbuild to assemble library search paths for linking.

.. cmdoption:: libs-only-l [package]

 Print space-separated list of export/cpp/libs that start with ``-l``.  If --deps-only is provided, then the package itself is excluded. This is used by rosbuild to assemble libraries for linking.

.. cmdoption:: libs-only-other [package]

 Print space-separated list of export/cpp/libs that don't start with ``-l`` or ``-L``. Used by rosbuild to assemble non-library link flags.

.. cmdoption:: --deps-only

 If :option:`--deps-only` is provided, then the package itself is excluded. This can be used with all ``libs-only-*`` variants.
 

.. _cmd_rospack_profile:

.. program:: rospack profile

rospack profile
---------------

.. cmdoption:: --length=N

 Force a full crawl of package directories (i.e., don't use cache, and report to console on the N (default 20) directories that took the longest time to crawl.  Useful for finding stray directories that are adversely affecting ``rospack``'s performance.  

.. cmdoption:: --zombie-only

 Only print directories that do not have any manifests.  In this case, the output can be fed directly into ``rm`` to clean up your tree, e.g.::

     rospack profile --zombie-only | xargs rm -rf


 NOTE: be sure to check the output before deleting any files!

.. program:: rospack plugins

rospack plugins --attrib=<attrib> [package]
-------------------------------------------

Examine packages that depend directly on the given package, extracting from each the name of the package followed by the value of an exported attribute with the name ``<attrib>``.  All matching exports are returned, newline-separated, e.g., if the manifest for a package "foo," located at ``/tmp/foo``, contains::

      <depend package="rosbuild"/>
      <export>
        <rosbuild cmake="${prefix}/cmake/foo.cmake/>
      </export>
      
then ``rospack plugins --attrib=cmake rosbuild`` will return (at least)::

      foo /tmp/foo/cmake/foo.cmake


.. cmdoption:: --top=<toppkg>

  If :option:`--top` is given, then in addition to depending directly on the given package, to be scanned for exports, a package must also be a dependency of ``<toppkg>``, or be ``<toppkg>`` itself.




rospack developers' guide
=========================

Dependencies
------------

rospack contains a copy of the TinyXML library.  Unit tests, instead
of using the copy available in 3rdparty.  For the same reason, unit
tests for rospack, which require gtest, are in a separate package,
called ``rospack_test``.

