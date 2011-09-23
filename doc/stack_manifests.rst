.. _stack_manifest_file:

Stack manifest files
====================

A ROS *stack manifest* (``stack.xml``) is a minimal specification for
ROS stacks.  Whereas a :ref:`package manifest.xml <manifests>`
provides information for building software, a stack manifest mainly
deals with distributing and installing software.

In addition to providing a metadata about a stack, an important role
of a ``stack.xml`` is to declare dependencies on other stacks. The
presence of a `stack.xml` file in a directory is significant: a
directory that contains a `stack.xml` file is considered to be a
stack, and any packages within it are considered to be part of that
stack (NOTE: stacks cannot contain stacks).

A bare minimum ``stack.xml`` file is much like a readme file, stating
who is responsible for the stack and what license it is under. The
license is important as it indicates who can use your
code. `stack.xml` files usually include `<depend>` tags, which declare
stacks that must be installed as pre-requisites.


Uses
----

*Indexing*

    If a ``stack.xml`` is present, the directory is assumed to be a ROS stack, and the name of the package is the same as the name of the directory.  Additionally, properties like the author, license, and description provide important metadata for an indexer.

*Documentation*

    As part of the DRY (Don't Repeat Yourself) principle, manifest information is oftena automatically imported into documentation, such as header information on ROS.org wiki pages, as well as in Doxygen documentation.

*Deployment and Release*

    Dependencies between ROS stacks are used to generate installation packages.

XML Reference
-------------

Please see the :ref:`stack.xml tags reference <stack_xml>`.


Example
-------

::

    <stack>
      <description brief="common code for personal robots">
        A set of code and messages that are widely useful to all robots. Things
        like generic robot messages (i.e., kinematics, transforms), a generic 
        transform library (tf), laser-scan utilities, etc.
      </description>
      <author>Maintained by Tully Foote</author>
      <license>BSD</license>
      <review status="unreviewed" notes=""/>
      <url>http://ros.org/wiki/common</url>
      <depend stack="ros"/>
    </stack>


Tools
-----

`rosstack <http://ros.org/wiki/rosstack>`_ parses and retrieves information from ``manifest.xml`` files. For example, ``rosstack depends stack-name`` will tell you all of the dependencies of ``stack-name`` (use ``depends1`` to retrieve the direct dependencies).

Library Support
---------------

See the :class:`rospkg.RosPack` and :class:`rospkg.RosStack` for Python APIs to retrieve and parse manifest files.

