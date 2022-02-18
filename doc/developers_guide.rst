Developer's Guide
=================

REP 114: rospkg standalone library
----------------------------------

The rospkg library is being developed using the ROS REP process.  It
was introduced in `REP 114: rospkg standalone library
<http://www.ros.org/reps/rep-0114.html>`_.  Please read REP 114 to
better understand the motivation and goals of the rospkg library.

Bug reports and feature requests
--------------------------------

- `Submit a bug report / a feature request <https://github.com/ros-infrastructure/rospkg/issues>`_

Getting the code
----------------

rospkg is hosted on GitHub.  To start developing for it, please create a fork:

https://github.com/ros-infrastructure/rospkg


Developing new OsDetectors
--------------------------

Developing a new :class:`OsDetector` is fairly straightforward.  There
are many examples in ``os_detect.py``.

If you contribute a :class:`OsDetector`, you *must* provide complete
unit test coverage.  For example, if your detector relies on parsing
``/etc/issue`` files, you must submit example ``/etc/issue`` files
along with tests that parse them correctly.

Test files for os detection should be placed in ``test/os_detect/os_name``.

If you submit a new detector, the documentation in
``doc/os_detect.rst`` must be updated as well.

Testing
-------

Setup

::

    pip install pytest
    pip install mock


rospkg uses `pytest <http://docs.pytest.org>`_ 
for testing, which is a fairly simple and straightfoward test
framework.  You just have to write a function start with the name
``test`` and use normal ``assert`` statements for your tests.

rospkg also uses `mock <http://www.voidspace.org.uk/python/mock/>`_ to
create mocks for testing.

You can run the tests, including coverage, as follows:

::

    cd rospkg
    pytest test --cov=rospkg


Documentation
-------------

Sphinx is used to provide API documentation for rospkg.  The documents
are stored in the ``doc`` subdirectory.

