.. _manifest_xml:

Package manifest XML tags reference
===================================

Manifests always have the filename ``manifest.xml``.

Manifests must use `valid XML syntax <http://www.w3schools.com/xml/xml_syntax.asp>`_, including escaping special characters such as ``<``, ``>``, and ``&`` when they are used inside strings (use ``&lt;``, ``&gt;``, and ``&amp;``, respectively).

.. contents:: Table of Contents
   :depth: 2

Required Tags
-------------

The required set of tags in a ``manifest.xml`` file is very minimal and only provides the most basic metadata about your package, including what it is, who wrote it, and who can use it. 

 * :ref:`\<package\> <package_tag>`
 * :ref:`\<description\> <manifest_description_tag>`
 * :ref:`\<description|<manifest_description_tag>`
 * :ref:`\<license|<manifest_license_tag>`
 * :ref:`\<author\> <manifest_author_tag>`

Optional Tags
-------------

The most common optional tags are :ref:`\<depend\> <manifest_depend_tag>` and
:ref:`\<url\> <manifest_url_tag>`. We strongly recommend the use of the
``<url>`` tag to point users to a website where they can find out
more information about your stack. This website is most commonly a
wiki page on ros.org.


 * :ref:`\<depend\> <manifest_depend_tag>`
 * :ref:`\<rosdep\> <manifest_rosdep_tag>`
 * :ref:`\<url\> <manifest_url_tag>`
 * :ref:`\<review\> <manifest_review_tag>`
 * :ref:`\<export\> <manifest_export_tag>`
 * :ref:`\<versioncontrol\> <versioncontrol_tag>`

.. _package_tag:

<package>
---------

This is the top-level tag in a manifest.

Elements
''''''''

 * :ref:`\<description\> <manifest_description_tag>`
 * :ref:`\<license\> <manifest_license_tag>`
 * :ref:`\<author\> <manifest_author_tag>`
 * :ref:`\<url\> <manifest_url_tag>`
 * :ref:`\<depend\> <manifest_depend_tag>`
 * :ref:`\<rosdep\> <manifest_rosdep_tag>`
 * :ref:`\<export\> <manifest_export_tag>`
 * :ref:`\<review\> <manifest_review_tag>`
 * :ref:`\<versioncontrol\> <versioncontrol_tag>`

.. _manifest_description_tag:

<description>
-------------

Text
''''

Description of your package. It may be multi-line and include XHTML. 

Attributes
''''''''''

 ``brief="brief text"`` *(optional)*
   One-line summary of your Package. Useful for UI displays where the package name isn't sufficiently descriptive.

Example
'''''''

::

    <description brief="ROS for Python">
       Python implementation of the ROS master/node APIs and client library.
    </description>


.. _manifest_license_tag:

<license>
---------

Text
''''

Name of license for this package, e.g. BSD, GPL, LGPL. In order to assist machine readability, only include the license name in this tag. For any explanatory text about licensing caveats, please use the ``<description>`` tag. 

Most common open-source licenses are described on the `OSI website <http://www.opensource.org/licenses/alphabetical>`_.

Commonly used license strings:

 - Apache 2.0
 - BSD
 - Boost Software License
 - GPLv2
 - GPLv3
 - LGPLv2.1
 - LGPLv3
 - MIT 
 - Mozilla Public License Version 1.1
 - ZLib
 - wxWindows


Attributes
''''''''''

 ``url="license url"`` *(optional)*
  For lesser-known licenses, it is helpful to add this attribute with a link to the text of the license.

Example
'''''''

::

    <license>BSD</license>

  
.. _manifest_author_tag:

<author>
--------

Text
''''

Name and contact information for the package.  If there are multiple authors, use a comma-separated list in a single author tag.

Example
'''''''

::

    <author>Alyssa P. Hacker/aphacker@willowgarage.com, Norman Contributor/norcon@example.com</author>


.. _manifest_depend_tag:

<depend>
--------

Declare a ROS package that this package depends on.

Attributes
''''''''''

 ``package="ros_package_name"``
  Name of ROS package dependency.

Example
'''''''

::

    <depend package="pkgname"/>

.. _manifest_rosdep_tag:

<rosdep>
--------

Declare an external dependency that this package requires and can be installed via `rosdep <http://ros.org/wiki/rosdep>`_. These external dependencies are generally libraries that can be installed by OS package managers, like ``apt``.

Attributes
''''''''''

 ``name="rosdep_dependency"``
  Name of rosdep dependency.

Example
'''''''

::

    <rosdep name="boost"/>


.. _manifest_url_tag:

<url> tag
---------

Text
''''

Web site for your package. This is important for guiding users to your online documentation.

Example
'''''''

::

    <url>http://ros.org/wiki/rospy</url>

.. _versioncontrol_tag:

.. _manifest_export_tag:

<export>
--------

The ``<export> ... </export>`` portion of the manifest declares
various flags and settings that a package wishes to export to support
tools, such as CMake. This section is extensible by individual tools
and these properties can be extracted from the command-line using the
`rospack <http://ros.org/wiki/rospack>`_ tool.

Elements
''''''''

You are free to add your own XML elements to the ``<export>`` section
of a manifest. This is used by a variety of packages for functionality
such as plugins. Tags currently used include:

 * :ref:`\<cpp\> <cpp_tag>`
 * :ref:`\<python\> <python_tag>`
 * :ref:`\<rosdoc\> <rosdoc_tag>`
 * :ref:`\<roslang\> <roslang_tag>`
 * :ref:`\<roswtf\> <roswtf_tag>`


.. _cpp_tag:

export: <cpp>
-------------

Export flags to the make compiler. These flags are made available to
*users* of this package, not the package itself.  This is not the
place to put flags that you'll need in building your package.
Instead, encode those needs in the [[CMakeLists|CMakeLists.txt]] file,
using standard CMake macros, such as ``include_directories()`` and
``target_link_libraries()``.

Attributes
''''''''''

 ``cflags="${prefix}/include"``
   cflags export value.
 ``lflags="..."``
   lflags export value.
 ``os="osx"``
   Restricts settings to a particular OS.

Example
'''''''

::

    <cpp cflags="-I${prefix}/include" lflags="-L${prefix}/lib -Wl,-rpath,${prefix}/lib -lros"/>
    <cpp os="osx" cflags="-I${prefix}/include" lflags="-L${prefix}/lib -Wl,-rpath,${prefix}/lib -lrosthread -framework CoreServices"/>

Note the use of ``-Wl,-rpath,${prefix}/lib``.  This tells the linker to look in ``${prefix}/lib`` for shared libraries when running an executable.  This flag is necessary to allow the use of shared libraries that reside in a variety of directories, without requiring the user to modify :envvar:`LD_LIBRARY_PATH`.  Every time you add a ``-Lfoo`` option to your exported lflags, add a matching ``-Wl,-rpath,foo`` option.  The -Wl options can be chained together, e.g.: ``-Wl,-rpath,foo,-rpath,bar``.

.. _python_tag:

export: <python>
----------------

Export a path other than the default ``${prefix}/src`` to the :envvar:`PYTHONPATH`.

Attributes
''''''''''

 ``path="${prefix}/mydir"``
  Path to append to :envvar:`PYTHONPATH`.

Example
'''''''

::

    <python path="${prefix}/different_dir"/>


.. _rosdoc_tag:

export: <rosdoc>
----------------

Override settings in the `rosdoc <http://ros.org/wiki/rosdoc>`_ documentation generator. Currently this is used to disable auto-generated code documentation on the package. This is common for thirdparty packages, which have their own documentation. This tag enables packages to link to this external documentation.

Attributes
''''''''''

 ``external="http://link"`` *(optional)*
  URL to external documentation. rosdoc will not run a documentation tool (e.g. Doxygen) on this package.
 ``config="rosdoc.yaml"`` *(optional)*
  Name of rosdoc configuration file.

Examples
''''''''

External API documentation::

    <rosdoc external="http://external/documentation.html"/>


Using an external config file::

    <rosdoc builder="rosdoc.yaml"/>


Attributes
''''''''''

 ``excludes="build"`` *(optional)*
   Path to exclude (see Doxygen documentation on `EXCLUDES`).
 ``file-patterns="*.c *.cpp *.dox"`` *(optional)*
   Patterns for files to include (see Doxygen documentation on `FILE_PATTERNS`).

.. _roslang_tag:

export: <roslang>
-----------------

This tag should only be used by ROS client libraries, such as `roscpp <http://ros.org/wiki/roscpp>`_ and `rospy <http://ros.org/wiki/rospy>`_.

The ``<roslang>`` export specifies a CMake file that should be exported to the `rosbuild <http://ros.org/wiki/rosbuild>`_ system. The CMake rules will be exported to *every* ROS package, which is necessary for functionality such as message and service generation.

Attributes
''''''''''

 ``cmake="${prefix}/cmake/file.cmake"``
   CMake file.

Example
'''''''

::



    <roslang cmake="${prefix}/cmake/rospy.cmake"/>


.. _roswtf_tag:

export: <roswtf>
----------------

Declare a `roswtf <http://ros.org/wiki/roswtf>`_ plugin.

Attributes
''''''''''

 ``plugin="python.module"``
   Python modulename to export as a [[roswtf]] plugin.

Example
'''''''

::

    <roswtf plugin="tf.tfwtf" />


.. _manifest_review_tag:

<review>
--------

Status of the package in the review process (Design, API, and Code review). See `QAProcess <http://ros.org/wiki/QAProcess>`_.  Packages that have not yet been reviewed should be marked as "experimental".

Example
'''''''

::

    <review status="experimental" notes="reviewed on 3/14/09" />


Attributes
''''''''''

 ``status="status"``
   See `list of valid review statuses <http://ros.org/wiki/Review Status>`_.
 ``notes="notes on review status"`` *(optional)*
   Notes on review status, such as date of last review.

