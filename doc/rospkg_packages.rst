ROS package access
==================

.. currentmodule:: rospkg

The :class:`RosPack` class provides APIs similar to the ``rospack``
command-line tool distributed with ROS.  Like ``rospack``, its
provides information about package and stack dependency information,
filesystem locations, and manifest access. The Python API is more
efficient than shelling out to ``rospack`` as provides caching and
other optimizations for repeated querying.

.. data:: MANIFEST_FILE

   Name of package manifest file, i.e. 'manifest.xml'.

.. class:: RosPack([ros_root=None, [ros_package_path=None]])

   Query information about ROS packages on the local filesystem. This
   includes information about dependencies, retrieving stack
   :class:`Manifest` instances, and determining the parent stack of a
   package.  

   ``RosPack`` can be initialized with the default environment, or
   its environment configuration can be overridden with alternate
   :envvar:`ROS_ROOT` and :envvar:`ROS_PACKAGE_PATH` settings.

   NOTE 1: for performance reasons, ``RosPack`` caches information about
   packages

   NOTE 2: ``RosPack`` is not thread-safe.

   Example::

        rp = RosPack()
        packages = rp.list_packages()
        path = rp.get_path('rospy')
        depends = rp.get_depends('roscpp')
        depends1 = rp.get_depends('roscpp', implicit=False)
    
   :param ros_root: override :envvar:`ROS_ROOT`.
   :param ros_package_path: override :envvar:`ROS_PACKAGE_PATH`.  To
     specify no :envvar:`ROS_PACKAGE_PATH`, use the empty string.  An
     assignment of None will use the default path.

   .. method:: get_ros_root() -> str

      Get the :envvar:`ROS_ROOT` configuration of this instance.

   .. method:: get_ros_package_path() -> str

      Get the :envvar:`ROS_PACKAGE_PATH` configuration of this instance.
        
   .. attribute:: ros_root

      Get the :envvar:`ROS_ROOT` configuration of this instance. Read-only.

   .. attribute:: ros_package_path

      Get the :envvar:`ROS_PACKAGE_PATH` configuration of this instance. Read-only.

   .. method:: get_manifest(name) -> Manifest

      Get the :class:`Manifest` of the specified package.

      :param name: package name, ``str``
      :raises: :exc:`InvalidManifest`
    
   .. method:: list() -> [str]

      List packages.

      :returns: complete list of package names in ROS environment

   .. method:: get_path(name) -> str

      :param name: package name, ``str``
      :returns: filesystem path of package
      :raises: :exc:`ResourceNotFound`
        
   .. method::  get_depends(name, [implicit=True]) -> [str]

      Get explicit and implicit dependencies of a package.

      :param name: package name, ``str``
      :param implicit: include implicit (recursive) dependencies, ``bool``
      :returns: list of names of dependencies.
      :raises: :exc:`InvalidManifest`        

   .. method:: get_rosdeps(package, [implicit=True]) -> [str]

      Collect rosdeps of specified package into a dictionary.
        
      :param package: package name, ``str``
      :param implicit: include implicit (recursive) rosdeps, ``bool``
      :returns: list of rosdep names.
        
   .. method:: stack_of(package) -> str
   
      :param package: package name, ``str``
      :returns: name of stack that *package* is in, or ``None`` if *package* is not part of a stack
      :raises: :exc:`ResourceNotFound`: if *package* cannot be located
