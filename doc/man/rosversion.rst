:orphan:

rosversion manual page
======================

Synopsis
--------

**rosversion** <*stack*> | *-d*

Description
-----------

The **rosversion** command prints version information for ROS stacks
and can also print the name of the active ROS distribution.

rosversion takes in a single ROS stack name as an argument, or a
**-d** option with no arguments to print the distribution version
instead.  If the version number for a stack is not known,
"<unversioned>" will be printed instead.

Options
-------

**-d**

  Print codename for current ROS distribution. 

