.. _packages:

ROS packages
============

Software in ROS is organized in *packages*. A package might contain a
library, a dataset, configuration files or anything else that
logically constitutes a useful module. The goal of these packages it
to provide this functionality in an easy-to-consume manner so that
software can be easily reused. In general, ROS packages follow a
"Goldilocks" principle: *enough functionality to be useful, but not too
much that the package is heavyweight and difficult to use from other
software*.

Packages are easy to create by hand or with tools like `roscreate-pkg
<http://www.ros.org/wiki/roscreate>`_. A ROS package is simply a
directory descended from :envvar:`ROS_ROOT` or
:envvar:`ROS_PACKAGE_PATH` that has a :ref:`manifest.xml
<manifest_file>` file in it. Packages may be organized together into
ROS [[Stacks|stacks]].

Please see the :ref:`package manifest files <manifest_file>` section
for documentation on how to read and write ``manifest.xml`` files.

Common Files and Directories
----------------------------

ROS packages tend to follow a common structure. Here are some of the directories and files you may notice.

 - ``bin/``: compiled binaries
 - ``include/package_name``: C++ include headers (make sure to export in the :ref:`package manifest <cpp_tag>`)
 - ``src/package_name/``: Source files, especially Python source that are exported to other packages.
 - ``scripts/``: executable scripts
 - ``CMakeLists.txt``: CMake build file (see `CMakeLists <http://ros.org/wiki/CMakeLists>`_)
 - ``manifest.xml``: :ref:`Package manifest <manifest_file>`

For C++ and Python developers, we strongly recommend that the
``package_name`` match namespaces/module names in your code so that
it's easy to locate what package provides your code.

Packages that are used with the ROS communication system may also have:

 - ``msg/``: `ROS message (msg) types <http://www.ros.org/wiki/msg>`_
 - ``srv/``: `ROS service (srv) types <http://www.ros.org/wiki/srv>`_

Command-line Tools
------------------

Packages are a very central concept to how files in ROS are organized,
so there are quite a few tools in ROS that help you manage them. This
includes:

 * `rospack <http://www.ros.org/wiki/rospack>`_: find and retrieve information about packages. The ROS build system also uses ``rospack`` to locate a package and build its dependencies.
 * `roscreate-pkg <http://www.ros.org/wiki/roscreate>`_: create a new package.
 * `rosmake <http://www.ros.org/wiki/rosmake>`_: build a package and its dependencies.
 * `rosdep <http://www.ros.org/wiki/rosdep>`_: install system dependencies of a package.

There are also extensions to common Unix shells that provide
additional functionality to help you navigate and use packages. The
most commonly used of these is `rosbash
<http://ros.org/wiki/rosbash>`_, which provides ROS-variants of common
Unix shell commands for Bash and other shells. The most commonly used
of these is ``roscd``, which performs a ``cd`` to the directory of a
package or stack, e.g.

::

    roscd roscpp_tutorials


