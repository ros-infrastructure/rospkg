Environment Variables
=====================

The following are environment variables that are observed by the ROS
packaging system. This listing does not include environment variables
for the ROS communication middleware (e.g. :envvar:`ROS_MASTER_URI`,
:envvar:`ROS_HOSTNAME`).

Essential
---------

.. data:: ROS_PACKAGE_PATH

   Path(s) to ROS packages and stacks to include in the build and
   runtime environment.  :envvar:`ROS_PACKAGE_PATH` can be composed of
   one or more paths separated by your standard OS path separator
   (e.g. ':' on Unix-like systems).  If there are multiple packages or
   stacks with the same name, ROS will choose the one that appears on
   :envvar:`ROS_PACKAGE_PATH` first.  

.. data:: ROS_ROOT

   This is a *required* environment variable, but it is only provided
   for backwards compatibility.  Historically, it is the path to the
   ROS stack.  For ROS Fuerte and later, it is the path to a
   backwards-compatibility support directory.


Optional
--------

.. data:: ROS_HOME

   Override path to :envvar:`ROS_HOME`, which is where log files and
   other user-specific assets are stored.  By default this is
   `~/.ros/`.

.. data:: ROS_LOG_DIR

   Override path to directory where log files are written.  By default this
   is :envvar:`ROS_HOME`/log. 

.. data:: ROS_TEST_RESULTS_DIR

   Override path to directory where teset results are written.  By default this is
   is :envvar:`ROS_HOME`/test_results.
   
.. data:: ROS_DISTRO

   .. versionadded:: Fuerte

   Override name of the currently active ROS distribution.  By default, this value is
   read from :envvar:`ROS_ETC_DIR`/distro. 

.. data:: ROS_ETC_DIR

   .. versionadded:: Fuerte

   Override path to `/etc/ros` directory.

