Overview
========

There are two main concepts in the ROS packaging system: *packages* and *stacks*.  *Packages* are the main unit for organizing and building software in ROS. A package may contain runtime processes (e.g. ROS nodes), a library, datasets, configuration files, or anything else that is usefully organized together. *Stacks* are collections of packages that provide aggregate functionality, such as a "navigation stack." Stacks are also how ROS software is released and have associated version numbers. 

So, packages are the smallest unit in which ROS software is *built*; stacks are the smallest unit in which ROS software is *released*.

Packages and stacks each have associated manifests: ``manifest.xml`` for packages and ``stack.xml`` for stacks.

You can continue reading the sections below to find out more about these concepts and files.

.. toctree::
   :maxdepth: 2

   packages
   stacks
   manifests
   stack_manifests
