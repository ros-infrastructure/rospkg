OS detection
============

.. currentmodule:: rospkg.os_detect

OS detection is a critical capability of many ROS tools in the ROS
build toolchain.  The :module:`rospkg.os_detect` module provides and
extendable library for detecting various operating systems.  It is
focused on detecting operating systems used with ROS.

Currently supported OSes:

- Arch Linux
- Cygwin
- Debian
- Fedora
- FreeBSD
- Gentoo
- Mandriva Linux
- Mint
- OS X
- Red Hat Linux
- Ubuntu


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

.. data:: OS_MANDRIVA

   Name used for Mandriva Linux.

.. data:: OS_OPENSUSE

   Name used for OpenSUSE OS.

.. data:: OS_OSX

   Name used for OS X.

.. data:: OS_RHEL

   Name used for Red Hat Enterprise Linux.

.. data:: OS_UBUNTU

   Name used for Ubuntu OS.


.. class:: OsNotDetected

   Exception to indicate failure to detect operating system.

.. class:: OsDetect(os_list)

   Detects the current operating system.  This class will iterate
   over registered classes to lookup the active OS and version.  The
   list of detectors can be overridden in the constructor; otherwise
   it will default to :class:`OsDetector` classes provided by this
   library.


    .. attribute:: default_os_list

        List currently registered detectors.  Must not be modified directly.
    

    .. staticmethod:: register_default(os_name, os_detector)

        Add :class:`OsDetector` to the default list of detectors.    
        
    .. method:: detect_os() -> (str, str)

        :returns: (os_name, os_version)
        :raises: :exc:`OsNotDetected` if OS could not be detected

    .. method:: get_detector(name) -> :class:`OsDetector`

        Get detector used for specified OS name.

        :raises: :exc:`KeyError`
        
    .. method:: get_os() -> :class:`OsDetector`

        Get :class:`OsDetector` for this operating system.
        
        :raises: :exc:`OsNotDetected` if OS could not be detected

    .. method:: get_name() -> str

        :returns: Name of current operating system.  See ``OS_``
          definitions in this module for possible values.
        :raises: :exc:`OsNotDetected` if OS could not be detected

    .. method:: get_version() -> str

        :returns: Version of current operating system
        :raises: :exc:`OsNotDetected` if OS could not be detected


.. class:: OsDetector

   Generic API for detecting a specific OS.  

    .. method:: is_os() -> bool

        ::returns: if the specific OS which this class is designed to
        detect is present.  Only one version of this class should
        return for any version.

    .. method:: get_version() -> str

        ::returns: standardized version for this OS. (ala Ubuntu Hardy Heron = "8.04")


.. method:: lsb_get_os() -> str

    Linux: wrapper around lsb_release to get the current OS
    
.. method:: def lsb_get_codename() -> str

    Linux: wrapper around lsb_release to get the current OS codename
    
.. method:: def lsb_get_version() -> str

    Linux: wrapper around lsb_release to get the current OS version

.. method:: def uname_get_machine() -> str

    Linux: wrapper around uname to determine if OS is 64-bit


