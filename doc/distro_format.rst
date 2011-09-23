.. _distro_format:

rosdistro file format
=====================

rosdistro is a file format for managing `ROS Distribution release
<http://www.ros.org/wiki/Distributions>`_ and the ROS stacks they
contain. This file format is used as input to a variety of tools in
the ROS build and release toolchain, from stack release tools to
rosdoc.  The file format itself is a YAML-based description of a
collection of ROS stacks.

There are two roles of information in the rosdistro file:

 - *Building*: What versions of stacks are included in the distribution release
 - *Continuous integration and release*: Source control information of stacks in the release

.. contents:: Table of Contents
   :depth: 3


Examples
--------

 - `cturtle.rosdistro <https://code.ros.org/svn/release/trunk/distros/cturtle.rosdistro>`_
 - `electric.rosdistro <https://code.ros.org/svn/release/trunk/distros/electric.rosdistro>`_

Main Sections
-------------

The rosdistro document is a YAML mapping. This mapping has several main sections:

 `_rules`
   Top-level, named rules for stacks. Rules describe the URLs where stacks can be found in source control, ``{rule-name: {source-control-rules}}``.

   Example::

        _rules:
          alufr-ros-pkg:
            repo: alufr-ros-pkg
            svn:
              dev: https://alufr-ros-pkg.googlecode.com/svn/trunk/$STACK_NAME
              distro-tag: https://alufr-ros-pkg.googlecode.com/svn/tags/distros/$RELEASE_NAME/stacks/$STACK_NAME
              release-tag: https://alufr-ros-pkg.googlecode.com/svn/tags/stacks/$STACK_NAME/$STACK_NAME-$STACK_VERSION

 `release`
   Name of this release, ``string``

   Example::

       release: electric

 `variants`
   This section lists the variants (aka debian metapackages) that are described by this file. 

   *Type*: ordered sequence of mappings, ``{distribution-name: [stack-names]}``

   Example::

        variants:
        - ros-base:
            stacks: [ros, ros_comm, common_rosdeps]
        
 `stacks`
   This section lists release information about the stacks that are included in the distribution. This information ranges from the version number of the release to URLs that are used for source control.   

   NOTE: the `_uri_rules` key can appear at any level in this tree of mappings. 
   
   *Type*: unordered list of mappings ``{stack-name: {stack-properties}}``

   Example::

        stacks:
          _rules: ros-pkg-trunk
          arbotix: {_rules: vanadium-ros-pkg, version: 0.6.0}
        
 `version`

   *DEPRECATED*: Version number for this file. Version numbers may be used by tools, such as the debian package builder, to determine whether or not to generate new output. You can use the `$Revision: $` `svn:keyword` to track the SVN revision Id of the file.

   *Type*: ``int`` or special ``$Revision: VERSION $`` string.

_rules
~~~~~~

`_rules` are URL format strings that are used for determining the location of source code related to a stack.


variants
~~~~~~~~

The `variants` section lists groupings of stacks that you wish to
install together. They map directly to debian metapackages. In
addition to providing a list of stack names, variants may also specify
that they extend another variant.


Example::

    variants:
    - core:
        stacks: [ros, rx]
    - extended:
        extends: core
        stacks: [common, common_msgs, geometry]
    
stacks
~~~~~~

Each key in the `stacks` section describes information about a particular stack, e.g.::

      mystack: {version: 0.7.3}

In this example, the stack is named ``mystack``. It has a version 0.7.3 release.

A stack may also contain a ``_rules`` key, which overrides any higher-level ``_rules`` values.


Version Control _rules
----------------------

Repo _rule
~~~~~~~~~~

TODO: reorg this comment.

There should be a rule stating the repo name:

 ``repo: ros-pkg``

SVN _rules
~~~~~~~~~~

*Required keys*

 ``dev``
    URL of your development branch. This often refers to a code branch, like ``trunk``.

 ``release-tag``
    URL for version-specific release tag to create (e.g. ``tags/ros-1.2.1``). Release tags are generally for ''immutable'' references to code. The ``release-tag`` is generally used for building binaries, i.e. debian packages. This allows us to rollback releases in the debian system if there is a problem.

 ``distro-tag``
    URL for the distribution release tag to create. This is a moving tag that allows people to track releases for a specific distribution release (e.g. ``tags/cturtle``). The ``distro-tag`` is generally used for source-based installs. They allow users to ``svn up`` and get newer updates.


*Optional keys*

 We define three more rules that are necessary if your repository uses separate URLs for anonymous access.

 ``anon-dev``
    *anonymously readable* URL of your development branch
 ``anon-distro-tag``
    *anonymously readable* URL for the distribution release tag to create. This is a moving tag that allows people to track releases for a specific distribution release (e.g. ``tags/cturtle``).
 ``anon-release-tag``
    *anonymously readable* URL for version-specific release tag to create (e.g. ``tags/ros-1.2.1``).

You do not have to define these rules your repository provides anonymous access at the ``dev``/``distro-tag``/``release-tag`` URLs.


SVN example::

    svn: 
      anon-dev: http://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/trunk
      anon-distro-tag: http://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/tags/$RELEASE_NAME
      anon-release-tag: http://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/tags/$STACK_NAME-$STACK_VERSION
      dev: https://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/trunk
      distro-tag: https://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/tags/$RELEASE_NAME
      release-tag: https://svn.mech.kuleuven.be/repos/orocos/trunk/kul-ros-pkg/stacks/$STACK_NAME/tags/$STACK_NAME-$STACK_VERSION

Distributed VCS _rules (hg, git, bzr)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mercurial, Git, and Bazaar we use a standard set of keys for distributed VCS systems.

*Required keys*

 ``uri``
   The URI for the repo.  For example ``https://stack-nxt-robots.foote-ros-pkg.googlecode.com/hg``

 ``dev-branch``
   The name of the branch in which development is being focused for this distro, for example ``default`` in hg or ``master`` in git are common here. After branching for diamondback it may be ``1.3``

 ``distro-tag``
   The tag to pull which tracks the latest release in this distro often just ``$RELEASE_NAME``

 ``release-tag``
   The rule for how to generated numbered release tags.  Commonly just ``$STACK_NAME-$STACK_VERSION``


*Optional key*

 ``anon-uri``
   The URI for the repo that is used for anonymous access to your repo.  Not necessary if ``uri`` is valid for anonymous access.


Bazaar example::

      bzr: 
        anon-uri: lp:sr-ros-interface
        uri: bzr+ssh://bazaar.launchpad.net/~shadowrobot/sr-ros-interface
        dev-branch: stable
        distro-tag: $RELEASE_NAME
        release-tag: $STACK_NAME-$STACK_VERSION


Git example::

      git: 
        anon-uri: http://git.mech.kuleuven.be/robotics/rtt_ros_integration.git
        uri: git@git.mech.kuleuven.be:robotics/rtt_ros_integration.git
        dev-branch: master
        distro-tag: $RELEASE_NAME
        release-tag: $STACK_NAME-$STACK_VERSION


Mercurial example::

      hg: 
        uri: https://kforge.ros.org/simplecap/simple_capture
        dev-branch: default
        distro-tag: $RELEASE_NAME
        release-tag: $STACK_NAME-$STACK_VERSION



_rules Variables
~~~~~~~~~~~~~~~~

You can use several variables that make writing these rules easier and re-usable:

 ``$STACK_NAME``
   Name of stack.

 ``$STACK_VERSION``
   Version of stack.

 ``$DISTRO_NAME``
   Name of distribution release.

Top-level _rules
~~~~~~~~~~~~~~~~

Top-level rules are named configuration dictionaries that can be used
by stacks declarations.  Here is an example SVN rule that defines
releases for releasing stacks in `ros-pkg` that use `trunk` as the
development branch::


    _rules:
    
      [OTHER RULE DEFINITIONS]
    
      ros-pkg-trunk:
        svn: 
          dev: 'https://code.ros.org/svn/ros-pkg/stacks/$STACK_NAME/trunk'
          distro-tag: 'https://code.ros.org/svn/ros-pkg/stacks/$STACK_NAME/tags/$RELEASE_NAME'
          release-tag: 'https://code.ros.org/svn/ros-pkg/stacks/$STACK_NAME/tags/$STACK_NAME-$STACK_VERSION'


Stack _rules
~~~~~~~~~~~~

In most cases, stacks usually refer to named, top-level rules like so::

    stacks:
    
      [OTHER STACK DEFINITIONS]
    
      pr2_navigation:
        _rules: wg-ros-pkg-trunk
        version: 0.1.0
    
      [OTHER STACK DEFINITIONS]

In this case, the ``pr2_navigation`` stack will use the rules named ``wg-ros-pkg-trunk``, which must be declared in the top-level ``_rules`` section.

In some cases, individual stacks may wish to provide their own rules. If you are just doing a release off a temporary branch, or otherwise, this can be the easiest way of cleanly specifying new rules.

Example::

    stacks:
    
      [OTHER STACK DEFINITIONS]
    
      pr2_navigation:
        _rules: 
          svn:
            dev: 'https://code.ros.org/svn/wg-ros-pkg/stacks/$STACK_NAME/branches/cturtle_branch'
            distro-tag: 'https://code.ros.org/svn/wg-ros-pkg/stacks/$STACK_NAME/tags/$RELEASE_NAME'
            release-tag: 'https://code.ros.org/svn/wg-ros-pkg/stacks/$STACK_NAME/tags/$STACK_NAME-$STACK_VERSION'
        version: 0.1.4
    
