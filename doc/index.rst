rospkg documentation
====================

.. module:: rospkg
.. moduleauthor:: Ken Conley <kwc@willowgarage.com>

The :mod:`rospkg` module provides basic utilities for querying
information about ROS packages and stacks.  There are several basic
APIs: :doc:`ROS environment <environment>`, :class:`RosPack`/:class:`RosStack`, and
:doc:`OS detection <os_detect>`.  The environment APIs enable access to environment
settings that defines the ROS package/stack filesystem configuration.
The :class:`RosPack` and :class:`RosStack` APIs are similar to the
``rospack`` and ``rosstack`` command-line tools and provide
information about dependency, location, and other package/stack
metadata.  The :class:`Manifest` class provides access to a specific
package/stack's manifest information.

.. toctree::
   :maxdepth: 2

   packages
   stacks
   environment
   os_detect

Example::

    import rospkg

    ros_root = rospkg.get_ros_root()
    
    r = rospkg.RosPack()
    depends = r.get_depends('roscpp')
    path = r.get_path('rospy')
    

Common API
==========

.. exception:: ResourceNotFound

   Requested resource (e.g. package/stack) could not be found.

Installation
============

rospkg is available on pypi and can be installed via ``pip``
::

    pip install rospkg

or ``easy_install``:

::

    easy_install rospkg

Using rospkg
============

The :mod:`rospkg` module is meant to be used as a normal Python
module.  After it has been installed, you can ``import`` it normally
and do not need to declare as a ROS package dependency.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

