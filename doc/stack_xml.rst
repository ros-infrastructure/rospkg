.. _stack_xml:

Stack manifest XML tags reference
=================================

NOTE: Stack manifests always have the filename ``stack.xml``. 

Required Tags
-------------

The required set of tags in a ``stack.xml`` file is very minimal and
only provides the most basic metadata about your stack, including what
it is, who wrote it, and who can use it.

 * :ref:`\<stack\> <stack_tag>`
 * :ref:`\<description\> <stack_description_tag>`
 * :ref:`\<license\> <stack_license_tag>`
 * :ref:`\<author\> <stack_author_tag>`

Optional Tags
-------------

The most common optional tags are ``<depend>`` and ``<url>``. We strongly
recommend the use of the ``<url>`` tag to point users to a website where
they can find out more information about your stack. The website is
most commonly a wiki page on ROS.org so that users can easily edit and
update information about your stack.


 * :ref:`\<depend\> <stack_depend_tag>`
 * :ref:`\<url\> <stack_url_tag>`
 * :ref:`\<review\> <stack_review_tag>`
 * :ref:`\<version\> <stack_version_tag>` 

Example
-------

::

    <stack>
      <description brief="Common code for working with images">
        Common code for working with images in ROS.
      </description>
      <author>Maintained by Patrick Mihelich</author>
      <license>BSD</license>
      <review status="Doc reviewed" notes="2009/6/10"/>
      <url>http://ros.org/wiki/image_common</url>
      <depend stack="common_msgs" />
      <depend stack="common_rosdeps" />
      <depend stack="pluginlib" /> 
      <depend stack="ros" /> 
      <depend stack="ros_comm" /> 
    
    </stack>
    

.. _stack_tag:

<stack>
-------

The ``<stack>`` tag is the top-level tag in a stack manifest.

Elements
''''''''

 * :ref:`\<description\> <stack_description_tag>`
 * :ref:`\<license\> <stack_license_tag>`
 * :ref:`\<author\> <stack_author_tag>`
 * :ref:`\<url\> <stack_url_tag>`
 * :ref:`\<depend\> <stack_depend_tag>`
 * :ref:`\<review\> <stack_review_tag>`


.. _stack_description_tag:

<description>
-------------


Text
''''

Description of the stack. It may be multi-line and include XHTML. 

Example
'''''''

::

     <description brief="ROS for Python">
        Python implementation of the ROS master/node APIs and client library.
     </description>
    

Attributes
''''''''''

 ``brief="brief text"`` *(optional)*
  One-line summary of your stack. Useful for UI displays where the stack name isn't sufficiently descriptive.

.. _stack_license_tag:

<license>
---------

Text
''''

Name of license for this package, e.g. BSD, GPL, LGPL. In order to
assist machine readability, only include the license name in this
tag. For any explanatory text about licensing caveats, please use the
``<description>`` tag.

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


.. _stack_author_tag:

<author>
--------

Text
''''


Name and contact information for the person maintaining the stack.

Example
'''''''

::

    <author>Alyssa P. Hacker/aphacker@willowgarage.com</author>


.. _stack_depend_tag:

<depend>
--------

Declares a stack that this stack depends on.

Example
'''''''

::

    <depend stack="ros"/>


Attributes
''''''''''

 ``stack="stack_name"``
   Name of ROS stack dependency.

.. _stack_url_tag:

<url>
-----

Text
''''

Website for the stack. This is important for guiding users to online documentation.

Example
'''''''

::

    <url>http://ros.org/wiki/navigation</url>


.. _stack_review_tag:

<review>
--------

Status of the stack in the review process (Design, API, and Code
review). `QAProcess <http://ros.org/wiki/QAProcess>`_.  Stack that
have not yet been reviewed should be marked as "experimental".

Attributes
''''''''''


 ``status="status"``
   See `list of valid review statuses <http://ros.org/wiki/Review Status>`_.
 ``notes="notes on review status"`` *(optional)*
   Notes on review status, such as date of last review.


Example
'''''''

::

    <review status="experimental" notes="reviewed on 3/14/09" />


.. _stack_version_tag:

<version>
---------

.. versionadded: Electric

Text
''''

The version number of the stack.  

*IMPORTANT*:

 - This should only be used with stacks that follow the `release <http://ros.org/wiki/release>`_ process
 - Do *not* combine this with the ``rosbuild_make_distribution()`` CMake macro.  Use the ``<version>`` tag *or* the CMake macro, but not both.

Example
'''''''

::

    <version>1.2.7</version>

