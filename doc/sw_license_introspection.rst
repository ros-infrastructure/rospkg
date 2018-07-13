Software license introspection
=======================

.. module:: rospkg.sw_license
    :synopsis: Software license introspection for ROS and system packages.

The :mod:`rospkg.sw_license` module provides a feature to list up software
license for all ROS packages in the dependency chain. It also provides some utilities
regarding software license.

Commandline tools
-----------------

Command line script ``sw_licenses`` provides a single point of entry for APIs regarding software license.

Introspect software license for a given package and packages it depends on
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Syntax::

    sw_licenses %PKG_NAME%

Example::

    sw_licenses rviz
    :
    Path of the output file: /tmp/licenses_rviz-1.11.18.yml

    cat /tmp/licenses_rviz-1.11.18.yml
    :
    BSD:
    - rosconsole
    - rosparam
    - catkin
    :
    BSD, Creative Commons:
    - rviz
    unknown:
    - python-rospkg
    - python-catkin-pkg
    - python-rosdep



.. autoclass:: OsNotDetected

.. class:: OsDetect(os_list)

   Detects the current operating system.  This class will iterate
   over registered classes to lookup the active OS and version.  The
   list of detectors can be overridden in the constructor; otherwise
   it will default to :class:`OsDetector` classes provided by this
   library.


    .. attribute:: default_os_list

        List of currently registered detectors.  Must not be modified directly.
    
    .. staticmethod:: register_default(os_name, os_detector)

        Register detector to be used with all future instances of
        :class:`OsDetect`.  The new detector will have precedence over
        any previously registered detectors associated with *os_name*.
        
    .. method:: detect_os() -> tuple

        :returns: (os_name, os_version, os_codename), ``(str, str, str)``
        :raises: :exc:`OsNotDetected` if OS could not be detected

    .. method:: get_detector([name]) -> OsDetector

        Get detector used for specified OS name, or the detector for this OS if name is ``None``.

        :raises: :exc:`KeyError`
        
    .. method:: add_detector(name, detector)

        Add detector to list of detectors used by this instance.
        *detector* will override any previous detectors associated
        with *name*.

        :param name: OS name that detector matches
        :param detector: :class:`OsDetector` instance

    .. method:: get_os() -> OsDetector

        Get :class:`OsDetector` for this operating system.
        
        :raises: :exc:`OsNotDetected` if OS could not be detected

    .. method:: get_name() -> str

        :returns: Name of current operating system.  See ``OS_*``
          definitions in this module for possible values.
        :raises: :exc:`OsNotDetected` if OS could not be detected

    .. method:: get_version() -> str

        :returns: Version of current operating system
        :raises: :exc:`OsNotDetected` if OS could not be detected

    .. method:: get_codename() -> str

        :returns: Codename of current operating system if available,
          or empty string if OS does not provide codename.
        :raises: :exc:`OsNotDetected` if OS could not be detected



.. autoclass:: OsDetector
   :members:



OS name definitions
-------------------

.. data:: OS_ARCH

   Name used for Arch Linux OS.

.. data:: OS_CYGWIN

   Name used for Cygwin OS.

.. data:: OS_DEBIAN

   Name used for Debian OS.

.. data:: OS_FREEBSD

   Name used for FreeBSD OS.

.. data:: OS_GENTOO

   Name used for Gentoo.

.. data:: OS_MINT

   Name used for Mint OS.

.. data:: OS_OPENSUSE

   Name used for OpenSUSE OS.

.. data:: OS_OSX

   Name used for OS X.

.. data:: OS_RHEL

   Name used for Red Hat Enterprise Linux.

.. data:: OS_SLACKWARE

   Name used for Slackware.

.. data:: OS_UBUNTU

   Name used for Ubuntu OS.


Linux helper methods
--------------------

.. method:: lsb_get_os() -> str

    Linux: wrapper around lsb_release to get the current OS
    
.. method:: lsb_get_codename() -> str

    Linux: wrapper around lsb_release to get the current OS codename
    
.. method:: lsb_get_version() -> str

    Linux: wrapper around lsb_release to get the current OS version

.. method:: uname_get_machine() -> str

    Linux: wrapper around uname to determine if OS is 64-bit


