.. _stacks:

ROS stacks
============

:ref:`Packages <packages>` can be organized into ROS *stacks*. Whereas
the goal of packages is to create and compile minimal collections of
code for easy *reuse*, the goal of stacks is to simplify the process
of code *sharing*. Stacks are the primary mechanism in ROS for
distributing software. Each stack has an associated version and can
declare dependencies on other stacks. These dependencies also declare
a version number, which provides greater stability in development.

Stacks collect packages that collectively provide functionality, such
as a navigation stack or a manipulation stack. 

Stacks are easy to create by hand. A stack is simply a directory
descended from :envvar:`ROS_ROOT` or :envvar:`ROS_PACKAGE_PATH` that
has a :ref:`stack.xml <stack_manifest_file>` file in it. Any packages
in this directory are considered to be part of the stack.

For release purposes, a ``CMakeLists.txt`` should also be put into the
root of the stack.  The `roscreate-stack
<http://ros.org/wiki/roscreate>`_ tool can generate this file
automatically.

Please see the :ref:`stack manifest <stack_manifest_file>` section for
documentation on how to write `stack.xml` files.

Unary stacks
------------

A *unary stack* is simply a stack that is also a package.  

*Advanced*: This is described in greater detail in `REP 109
<http://www.ros.org/reps/rep-0109.html>`_.

Command-line Tools
------------------

`rosstack <http://www.ros.org/wiki/rosstack>`_ is the primary ROS tool
for interacting with ROS stacks. It is the stack-level analogue of the
`rospack <http://www.ros.org/wiki/rospack>`_ tool for packages.

`roscreate-stack <http://ros.org/wiki/roscreate>`_ helps automate the
process of creating a stack, including generating a valid
``stack.xml`` file with correct dependencies.

There are also extensions to common Unix shells that provide
additional functionality to help you navigate and use packages. The
most commonly used of these is `rosbash
<http://ros.org/wiki/rosbash>`_, which provides ROS-variants of common
Unix shell commands for Bash and other shells. The most commonly used
of these is ``roscd``, which performs a ``cd`` to the directory of a
package or stack, e.g.

::

    roscd navigation

