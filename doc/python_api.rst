rospkg documentation
====================

.. module:: rospkg
.. moduleauthor:: Ken Conley <kwc@willowgarage.com>

The :mod:`rospkg` Python module provides basic utilities for querying
information about ROS packages, stacks, and distributions.  There are
several basic APIs: :doc:`ROS environment <environment>`,
:class:`RosPack`/:class:`RosStack`, :doc:`OS detection
<os_detect>`, and :doc:`distributions <rospkg_distro>`. 

The environment APIs enable access to environment settings that define
the ROS package/stack filesystem configuration.  The :class:`RosPack`
and :class:`RosStack` APIs are similar to the ``rospack`` and
``rosstack`` command-line tools and provide information about
dependency, location, and other package/stack metadata.  The
:class:`Manifest` class provides access to a specific package/stack's
manifest information. NOTE: the :class:`Manifest` class API is still
volatile.  Where possible, use the relevant
:class:`RosPack`/:class:`RosStack` APIs to access manifest-related
information instead (e.g. dependency relationships).

The :mod:`rospkg.distro` sub-module provides access to ROS
distribution files, which describe collections of ROS stacks releases.
This API is module is still unstable and mainly supports internal
tools.

.. toctree::
   :maxdepth: 2

   rospkg_packages
   rospkg_stacks
   rospkg_environment
   os_detect
   rospkg_distro
   
Example::

    import rospkg

    ros_root = rospkg.get_ros_root()
    
    r = rospkg.RosPack()
    depends = r.get_depends('roscpp')
    path = r.get_path('rospy')
    

Common API
----------

.. exception:: ResourceNotFound

   Requested resource (e.g. package/stack) could not be found.

.. attribute:: __version__

   Version of this module.

Installation
------------

rospkg is available on pypi and can be installed via ``pip``
::

    pip install -U rospkg

or ``easy_install``:

::

    easy_install -U rospkg

Using rospkg
------------

The :mod:`rospkg` module is meant to be used as a normal Python
module.  After it has been installed, you can ``import`` it normally
and do not need to declare as a ROS package dependency.


Advanced: rospkg developers/contributors
----------------------------------------

.. toctree::
   :maxdepth: 2

   developers_guide


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

