ROS environment variable access
===============================

The environment APIs of :mod:`rospkg` provide convenient access to ROS
package-related environment variables, including methods that provide
default values when environment variable overrides are not active.

.. data:: ROS_PACKAGE_PATH

   Name of :envvar:`ROS_PACKAGE_PATH` environment variable.

.. data:: ROS_ROOT

   Name of :envvar:`ROS_ROOT` environment variable.

.. data:: ROS_HOME

   Name of :envvar:`ROS_HOME` environment variable.   

.. data:: ROS_LOG_DIR

   Name of :envvar:`ROS_LOG_DIR` environment variable.

.. data:: ROS_TEST_RESULTS_DIR

   Name of :envvar:`ROS_TEST_RESULTS_DIR` environment variable.

.. method:: get_ros_paths([env=None]) -> [str]

   Get an ordered list of ROS paths to search for ROS packages,
   stacks, and other resources.  This is generally computed from
   :envvar:`ROS_ROOT` and :envvar:`ROS_PACKAGE_PATH`.

   :param env: override environment dictionary

.. method:: get_ros_root([env=None]) -> str

   Get the current :envvar:`ROS_ROOT`.  NOTE: it is preferable to call
   :meth:`get_ros_paths()` instead of directly querying ROS
   environment variable values.

   :param env: override environment dictionary

.. method:: get_ros_package_path([env=None])

   Get the current :envvar:`ROS_PACKAGE_PATH`. NOTE: it is preferable to call
   :meth:`get_ros_paths()` instead of directly querying ROS
   environment variable values.

   :param env: (optional) environment override.

.. method:: get_ros_home([env=None]) -> str

   Get directory location of ``.ros`` directory (aka ``ROS_HOME``).
   possible locations for this. The :envvar:`ROS_HOME` environment
   variable has priority. If :envvar:`ROS_HOME` is not set,
   ``$HOME/.ros/log`` is used.

   :param env: override environment dictionary
   :return: path to use use for log file directory
    
.. method:: get_log_dir([env=None]) -> str

   Get directory to use for writing log files. There are multiple
   possible locations for this. The :envvar:`ROS_LOG_DIR` environment
   variable has priority. If that is not set, then
   :envvar:`ROS_HOME`/log is used. If :envvar:`ROS_HOME` is not set,
   ``$HOME/.ros/log`` is used.

   :param env: override environment dictionary
   :return: path to use use for log file directory

.. method:: get_test_results_dir(env=None) -> str

   Get directory to use for writing test result files. There are multiple
   possible locations for this. The :envvar:`ROS_TEST_RESULTS_DIR` environment variable
   has priority. If that is set, :envvar:`ROS_TEST_RESULTS_DIR` is returned.
   If :envvar:`ROS_TEST_RESULTS_DIR` is not set, then :envvar:`ROS_HOME`/test_results is used. If
   :envvar:`ROS_HOME` is not set, ``$HOME/.ros/test_results`` is used.

   :param env: override environment dictionary
   :return: path to use use for log file directory

.. method:: on_ros_path(p, [env=None]) -> bool

   Check to see if filesystem path is on paths specified in ROS
   environment (:envvar:`ROS_ROOT`, :envvar:`ROS_PACKAGE_PATH`).

   :param p: path, ``str``
   :return: True if p is on the ROS path (ROS_ROOT, ROS_PACKAGE_PATH)
