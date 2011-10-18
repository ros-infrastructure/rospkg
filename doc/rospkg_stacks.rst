ROS stack access
================

.. currentmodule:: rospkg

The :class:`RosStack` classes provides APIs similar to the
``rosstack`` command-line tool distributed with ROS.  Like
``rosstack``, it provides information about stack dependency
information, filesystem locations, and manifest access. The Python API
is more efficient than shelling out to ``rosstack`` as it provides
caching and other optimizations for repeated querying.

.. data:: STACK_FILE

   Name of stack manifest file, i.e. 'stack.xml'.

.. class:: RosStack([ros_paths=None])

   Query information about ROS stacks on the local filesystem. This
   includes information about dependencies, retrieving stack
   :class:`Manifest` instances, and determining the contents of
   stacks.  

   ``RosStack`` can be initialized with the default environment, or
   its environment configuration can be overridden with alternate
   ROS path settings.

   NOTE: for performance reasons, ``RosStack`` caches information about
   stacks.

   NOTE 2: ``RosStack`` is not thread-safe.

   :param ros_paths: Ordered list of paths to search for
     resources. If `None` (default), use environment ROS path.
            
   .. method:: get_ros_paths() -> [str]

      Get ROS paths of this instance

   .. attribute:: ros_paths

      Get ROS paths of this instance

   .. method:: get_manifest(name) -> Manifest

      Get the :class:`Manifest` of the specified package.

      :param name: package name, ``str``
      :raises: :exc:`InvalidManifest`
    
   .. method:: list() -> [str]

      List stacks.

      :returns: complete list of package names in ROS environment

   .. method:: get_path(name) -> str

      :param name: stack name, ``str``
      :returns: filesystem path of stack
      :raises: :exc:`ResourceNotFound`
        
   .. method::  get_depends(name, [implicit=True]) -> [str]

      Get explicit and implicit dependencies of a stack.

      :param name: stack name, ``str``
      :param implicit: include implicit (recursive) dependencies, ``bool``
      :returns: list of names of dependencies.
      :raises: :exc:`InvalidManifest`        

   .. method::  get_depends_on(name, [implicit=True]) -> [str]

      Get list of stacks that depend on a stack.  If implicit is
      ``True``, this includes implicit (recursive) dependency
      relationships.

      :param name: stack name, ``str``
      :param implicit: include implicit (recursive) dependencies, ``bool``

      :returns: list of names of dependencies, ``[str]``
      :raises: :exc:`InvalidManifest`

   .. method:: packages_of(stack) -> [str]

      :returns: name of packages that are part of stack
      :raises: :exc:`ResourceNotFound` if stack cannot be located

   .. method:: get_stack_version(stack) -> str

      :param env: override environment variable dictionary
      :returns: version number of stack, or None if stack is unversioned.

.. function:: expand_to_packages(names, rospack, rosstack) -> ([str], [str])

    Expand names into a list of packages. Names can either be of packages or stacks.

    :param names: list of names of stacks or packages, ``[str]``
    :param rospack: :class:`RosPack` instance
    :param rosstack: :class:`RosStack` instance
    :returns: ([packages], [not_found]). ``expand_packages()`` returns
      two lists. The first is of packages names. The second is a list
      of names for which no matching stack or package was found. Lists
      may have duplicates.

.. function:: get_stack_version_by_dir(stack_dir) -> str

    Get stack version where stack_dir points to root directory of stack.
    
    :param env: override environment variable dictionary
    :returns: version number of stack, or None if stack is unversioned.
