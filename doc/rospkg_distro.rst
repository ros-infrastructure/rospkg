rospkg.distro Python library
============================

.. currentmodule:: rospkg.distro

This submodule provides the :class:`Distro` class, which provides an
API for processing :ref:`rosdistro files <distro_format>`.

.. contents:: Table of Contents
   :depth: 2


Data model
----------

The top level representation is a :class:`Distro` instance, which contains :class:`Variant` and :class:`DistroStack` instances.  :class:`DistroStack` instances have a :class:`VcsConfig` (:class:`SvnConfig`, :class:`GitConfig`, :class:`BzrConfig`, :class:`HgConfig`), which represents the source control information for the stack.::

    Distro
      - Variant
      - DistroStack
         - VcsConfig 
    

Exceptions
----------

.. autoclass:: InvalidDistro


Utility functions
-----------------

.. method:: distro_uri(distro_name)

    Get distro URI of main ROS distribution files.
    
    :param distro_name: name of distro, e.g. 'diamondback'
    :returns: the SVN/HTTP URL of the specified distro.  This function should only be used
      with the main distros.

.. method:: load_distro(source_uri) -> Distro

    Load :class:`Distro` instance from *source_uri*.

    Example::

        from rospkg.distro import load_distro, distro_uri
        d = load_distro(distro_uri('electric'))

    :param source_uri: source URI of distro file, or path to distro
      file.  Filename has precedence in resolution.

    :raises: :exc:`InvalidDistro` if distro file is invalid
    :raises: :exc:`rospkg.ResourceNotFound` if file at *source_uri* is not found


.. method:: expand_rule(rule, stack_name, stack_ver, release_name) -> str

    Replace variables in VCS config rule value with specified values

.. method:: distro_to_rosinstall(distro, branch, [variant_name=None, [implicit=True, [released_only=True, [anonymous=True]]]])

    :param branch: branch to convert for
    :param variant_name: if not None, only include stacks in the specified variant.
    :param implicit: if variant_name is provided, include full (recursive) dependencies of variant, default True
    :param released_only: only included released stacks, default True.
    :param anonymous: create for anonymous access rules

    :raises: :exc:`KeyError` if branch is invalid or if distro is mis-configured



Model
-----

.. class:: DistroStack(stack_name, stack_version, release_name, rules)

    Stores information about a stack release

    :param stack_name: Name of stack
    :param stack_version: Version number of stack.
    :param release_name: name of distribution release.  Necessary for rule expansion.
    :param rules: raw ``_rules`` data.  Will be converted into appropriate vcs config instance.

    .. attribute:: stack_name

      Name of stack.

    .. attribute:: stack_version

      Version number of stack.

    .. attribute:: release_name

      Name of distribution release.  Necessary for rule expansion.

    .. attribute:: vcs_config

      :class:`VcsConfig` instance representing the ``_rules`` for this stack.

.. class:: Variant(variant_name, extends, stack_names, stack_names_implicit)

    A variant defines a specific set of stacks ("metapackage", in Debian
    parlance). For example, "base", "pr2". These variants can extend
    another variant.

    :param variant_name: name of variant to load from distro file, ``str``
    :param stack_names_implicit: full list of stacks implicitly included in this variant, ``[str]``
    :param raw_data: raw rosdistro data for this variant

    .. method:: get_stack_names([implicit=True]) -> [str]

       Get list of all stack names in this variant.

       :param implicit: If ``True``, includes names of stacks in
         parent variants.  Otherwise, include only stacks explicitly
         named in this variant. (default ``True``).
       
    .. attribute:: stack_names
    
       List of all stack names in this variant, including implicit stacks.   
    

.. class:: Distro(stacks, variants, release_name, version, raw_data)

    Store information in a rosdistro file.

    :param stacks: dictionary mapping stack names to :class:`DistroStack` instances
    :param variants: dictionary mapping variant names to :class:`Variant` instances
    :param release_name: name of release, e.g. 'diamondback'
    :param version: version number of release
    :param raw_data: raw dictionary representation of a distro

    .. method:: get_stacks([released=False]) -> {str: DistroStack}

        :param released: only included released stacks
        :returns: dictionary of stack names to :class:`DistroStack` instances in this distro.


    .. attribute:: stacks

        Dictionary of stack names mapped to :class:`DistroStack` instances in this distro.

    .. attribute:: released_stacks

        Dictionary of released stack names mapped to :class:`DistroStack` instances in this distro.

    .. attribute:: variants

        Dictionary of variant names mapped to :class:`Variant` instances in this distro.


Source control information
--------------------------

.. autoclass:: VcsConfig
   :members:


.. autoclass:: DvcsConfig
   :members:
    
.. autoclass:: GitConfig

.. autoclass:: HgConfig

.. autoclass:: BzrConfig

.. autoclass:: SvnConfig()

.. method:: get_vcs_configs() -> {str: VcsConfig}

    :returns: Dictionary of supported :class:`VcsConfig` instances.
      Key is the VCS type name, e.g. 'svn'. 


.. method:: load_vcs_config(rules, rule_eval) -> VcsConfig

    Factory for creating :class:`VcsConfig` subclass based on
    rosdistro _rules data.

    :param rules: rosdistro rules data
    :param rules_eval: Function to apply to rule values, e.g. to
      convert variables.  ``fn(str)->str``
    :returns: :class:`VcsConfig` subclass instance with interpreted rules data.
