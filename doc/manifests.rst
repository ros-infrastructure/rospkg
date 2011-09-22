Manifest files
==============

A ROS *manifest* (``manifest.xml``) is a minimal specification about your ROS package and supports a wide variety of tools, from compilation to documentation to distribution. In addition to providing a minimal specification of metadata about your package, an important role of manifests is to declare dependencies in a language-neutral and operating-system-neutral manner. The presence of a ``manifest.xml`` file in a directory is significant: any directory within your ROS package path that contains a ``manifest.xml`` file is considered to be a package (NOTE: packages cannot contain packages). 

The bare minimum manifest file is much like a README file, stating who wrote your package and what license it is under. The license is important as packages are means by which ROS code is distributed. The most common manifest files also include :ref:`\<depend\> <depend_tag>` and :ref:`\<export\> <export_tag>` tags, which help manage the installation and use of a package. 

The :ref:`\<depend\> <depend_tag>` tag points to another ROS package that must be installed. It can have a variety of meanings depending on the contents of the package is it pointing to. For example, for rospy code, a depend declares that the other package should be added to the :envvar:`PYTHONPATH`. For roslaunch files, a depend may indicate that this package includes roslaunch files from the other package.

The :ref:`\<export\> <export_tag>` tag describes language-specific build and runtime flags that should be used by any package that depends on your package. For a package containing roscpp code, an export tag may declare header files and libraries that should be picked by any package that depends on it.


Uses
----

*Indexing*

    If a ``manifest.xml`` is present, the directory is assumed to be a ROS package, and the name of the package is the same as the name of the directory.  Additionally, properties like the author, license, and description provide important metadata for an indexer.

*Documentation*

    As part of the DRY (Don't Repeat Yourself) principle, manifest information is oftena automatically imported into documentation, such as header information on ROS.org wiki pages, as well as in Doxygen documentation.

*Compilation*

    The ``<depend>`` tags of manifests are used to order ROS packages for compilation.  Also, the ``<export>`` section of manifests is frequently used by libraries like roscpp and rosjava to export properties to their respective build systems, as well as by rospy to configure :envvar:`PYTHONPATH`.  

*Deployment and Release*

    In addition to declaring dependencies between ROS packages, manifests can declare system dependencies (e.g. on the Boost library).  This information is used to release and deploy code to other machines.


XML Reference
-------------

Please see the :ref:`manifest.xml tags reference <manifest_xml>`.

Example
-------

::

    <package>
      <description brief="one line of text">
        long description goes here, 
        <em>XHTML is allowed</em>
      </description>
      <author>Alice/alice@somewhere.bar, Bob/bob@nowhere.foo</author>
      <license>BSD</license>
      <url>http://pr.willowgarage.com/</url>
      <logo>http://pr.willowgarage.com/blog/photos/sensor_head1_500.jpg</logo>
    
      <depend package="pkgname"/>
      <depend package="common"/>
      <rosdep name="python" />
      <versioncontrol type="svn" url="https://playerstage.svn.sourceforge.net/svnroot/playerstage/code/player/trunk"/>
      <export>
        <cpp cflags="-I${prefix}/include" lflags="-L${prefix}/lib -lros"/>
        <cpp os="osx" cflags="-I${prefix}/include" lflags="-L${prefix}/lib -Wl,-rpath,-L${prefix}lib -lrosthread -framework CoreServices"/>
      </export>
    
    </package>


Types of Dependencies
---------------------

The most common type of dependency that is expressed by a manifest is a dependency on another [[Packages|package]], which is expressed by the :ref:`\<depend\> <depend_tag>` tag. As explained earlier, the exact meaning of this dependency depends on the code involved and may either mean a compile-time dependency or runtime dependency.

A manifest can also declare dependencies on thirdparty software provided by the operating system, which is expressed by the :ref:`\<rosdep\> <rosdep_tag>`. For example, your package may need boost::


    <rosdep name="boost" />


By declaring this, users can now use the `rosdep <http://ros.org/wiki/rosdep>`_ tool to install boost. ``rosdep`` will examine their operating system, find the appropriate package manager and package name, and install it.

Tools
-----

`rospack <http://ros.org/wiki/rospack>`_ parses and retrieves information from ``manifest.xml`` files. For example, ``rospack depends package-name`` will tell you all of the dependencies of ``package-name`` (use ``depends1`` to retrieve the direct dependencies).

Library Support
---------------

See the :class:`rospkg.RosPack` and :class:`rospkg.RosStack` for Python APIs to retrieve and parse manifest files.
