ROS package and stack access
============================

The :class:`RosPack` and :class:`RosStack` classes provide APIs
similar to the ``rospack`` and ``rosstack`` command-line tools
distributed with ROS.  Like these tools, they provide information
about package and stack dependency information, filesystem locations,
and manifest access. These classes are more efficient than shelling
out to these tools as they provide caching and other optimizations for
repeated querying.

.. data:: MANIFEST_FILE

   Name of package manifest file, i.e. 'manifest.xml'.

.. data:: STACK_FILE

   Name of stack manifest file, i.e. 'stack.xml'.

.. exception:: ResourceNotFound

   Requested resource (e.g. package/stack) could not be found.

.. function:: list_by_path(manifest_name, path, cache) -> [str]

   List ROS stacks or packages within the specified *path*.

   The *cache* will be updated with the resource->path
   mappings. ``list_by_path()`` does NOT returned cached results;
   it only updates the cache.
    
   :param manifest_name: :data:`MANIFEST_FILE` or :data:`STACK_FILE`, ``str``
   :param path: path to list resources in, ``str``
   :param cache: path cache to update. Maps resource name to directory path. {str: str}
   :returns: complete list of resources in ROS environment.

.. class:: ManifestManager(manifest_name, cache_name, [ros_root=None, [ros_package_path=None]])

   Base class implementation for :class:`RosPack` and
   :class:`RosStack`.  NOTE: for performance reasons, ManifestManager
   caches information about packages.

   Subclasses are expected to use *manifest_name* and *cache_name* to customize behavior of ManifestManager.
        
   :param manifest_name: :data:`MANIFEST_FILE` or :data:`STACK_FILE`
   :param cache_name: "rospack_cache" or "rosstack_cache"
   :param ros_root: override :envvar:`ROS_ROOT`.
   :param ros_package_path: override :envvar:`ROS_PACKAGE_PATH`. To
     specify no :envvar:`ROS_PACKAGE_PATH`, use the empty string.
     An assignment of ``None`` will use the default path.
   
   .. method:: get_ros_root() -> str

      Get the :envvar:`ROS_ROOT` configuration of this instance.

   .. method:: get_ros_package_path() -> str

      Get the :envvar:`ROS_PACKAGE_PATH` configuration of this instance.
        
   .. attribute:: ros_root

      Get the :envvar:`ROS_ROOT` configuration of this instance. Read-only.

   .. attribute:: ros_package_path

      Get the :envvar:`ROS_PACKAGE_PATH` configuration of this instance. Read-only.

   .. method:: get_manifest(name) -> :class:`Manifest`

      Get the :class:`Manifest` of the specified resource.

      :param name: resource name, ``str``
      :raises: :exc:`InvalidManifest`
    
   .. method:: list() -> [str]

      List resources.

      :returns: complete list of package names in ROS environment

   .. method:: get_path(name) -> str

      :param name: resource name, ``str``
      :returns: filesystem path of resource
      :raises: :exc:`ResourceNotFound`
        
   .. method:: get_direct_depends(name) -> [str]

      Get the explicit dependencies of a resource.
        
      :param name: resource name, ``str``
      :returns: list of names of direct dependencies
      :raises: :exc:`ResourceNotFound`
      :raises: :exc:`InvalidManifest`

   .. method::  get_depends(name) -> [str]

      Get explicit and implicit dependencies of a resource.

      :param name: resource name, ``str``
      :returns: list of names of dependencies.
      :raises: :exc:`InvalidManifest`        
    
.. class:: RosPack([ros_root=None, [ros_package_path=None]])

   Query information about ROS packages on the local filesystem. This
   includes information about dependencies, retrieving stack
   :class:`Manifest` instances, and determining the parent stack of a
   package.  See parent class :class:`ManifestManager` for base API.

   ``RosPack`` can be initialized with the default environment, or
   its environment configuration can be overridden with alternate
   :envvar:`ROS_ROOT` and :envvar:`ROS_PACKAGE_PATH` settings.

   NOTE: for performance reasons, ``RosPack`` caches information about
   packages

   Example::

        rp = RosPack()
        packages = rp.list_packages()
        path = rp.get_path('rospy')
        depends = rp.get_depends('roscpp')
        depends1 = rp.get_direct_depends('roscpp')
    
   :param ros_root: override :envvar:`ROS_ROOT`.
   :param ros_package_path: override :envvar:`ROS_PACKAGE_PATH`.  To
     specify no :envvar:`ROS_PACKAGE_PATH`, use the empty string.  An
     assignment of None will use the default path.

   .. method:: get_rosdeps(package, [implicit=False]) -> [str]

      Collect rosdeps of specified package into a dictionary.
        
      :param package: package name, ``str``
      :param implicit: include implicit (recursive) rosdeps, ``bool``
      :returns: list of rosdep names.
        
   .. method:: stack_of(package) -> str
        :param package: package name, ``str``
        :returns: name of stack that package is in, or None if package is not part of a stack
        :raises: :exc:`ResourceNotFound`: if package cannot be located

.. class:: RosStack([ros_root=None, [ros_package_path=None]])

   Query information about ROS stacks on the local filesystem. This
   includes information about dependencies, retrieving stack
   :class:`Manifest` instances, and determining the contents of
   stacks.  See parent class :class:`ManifestManager` for base API.

   ``RosStack`` can be initialized with the default environment, or
   its environment configuration can be overridden with alternate
   :envvar:`ROS_ROOT` and :envvar:`ROS_PACKAGE_PATH` settings.

   NOTE: for performance reasons, ``RosPack`` caches information about
   packages.

   :param ros_root: (optional) override :envvar:`ROS_ROOT`.
   :param ros_package_path: (optional) override
     :envvar:`ROS_PACKAGE_PATH`.  To specify no
     :envvar:`ROS_PACKAGE_PATH`, use the empty string.  An assignment
     of ``None`` will use the default path.
            
   .. method:: packages_of(stack) -> [str]

      :returns: name of packages that are part of stack
      :raises: :exc:`ResourceNotFound` if stack cannot be located

   .. method:: get_stack_version(stack) -> str

      :param env: override environment variable dictionary
      :returns: version number of stack, or None if stack is unversioned.

.. function:: expand_to_packages(names, rospack, rosstack) -> ([str], [str])

    Expand names into a list of packages. Names can either be of packages or stacks.

    :param names: list of names of stacks or packages, ``[str]``
    :returns: ([packages], [not_found]). ``expand_packages()`` returns
      two lists. The first is of packages names. The second is a list
      of names for which no matching stack or package was found. Lists
      may have duplicates.

.. function:: get_stack_version_by_dir(stack_dir) -> str

    Get stack version where stack_dir points to root directory of stack.
    
    :param env: override environment variable dictionary
    :returns: version number of stack, or None if stack is unversioned.
