rospkg documentation
====================

.. moduleauthor:: Ken Conley <kwc@willowgarage.com>

Contents:

.. toctree::
   :maxdepth: 2

   packages
   environment

The :mod:`rospkg` module provides basic utilities for querying
information about ROS packages and stacks.  There are several basic
APIs: environment, :class:`RosPack`/:class:`RosStack`, and
:class:`Manifest`.  The environment APIs enable access to environment
settings that defines the ROS package/stack filesystem configuration.
The :class:`RosPack` and :class:`RosStack` APIs are similar to the
``rospack`` and ``rosstack`` command-line tools and provide
information about dependency, location, and other package/stack
metadata.  The :class:`Manifest` class provides access to a specific
package/stack's manifest information.

Example::

    import rospkg

    ros_root = rospkg.get_ros_root()
    
    r = rospkg.RosPack()
    m = r.get_manifest('roscpp')


In order to support a bootstrap role, the :mod:`rospkg` module is not
part of a ROS package itself.  It should not be declared as a ROS
dependency.  Instead, it is installed via ``pip``, ``easy_install``,
``apt-get`` or other standard installation mechanisms.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

