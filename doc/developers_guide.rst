Developer's Guide
=================

Bug reports and feature requests
--------------------------------

- `Submit a bug report <https://code.ros.org/trac/ros/newticket?component=rospkg&type=defect&&rospkg>`_
- `Submit a feature request <https://code.ros.org/trac/ros/newticket?component=rospkg&type=enhancement&rospkg>`_

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

rospkg uses `Python nose <http://readthedocs.org/docs/nose/en/latest/>`_ 
for testing, which is a fairly simple and straightfoward test
framework.  You just have to write a function start with the name
``test`` and use normal ``assert`` statements for your tests.

You can run the tests, including coverage, as follows:

::

    cd rospkg
    nosetests test/*.py --with-coverage --cover-package=rospkg


Documentation
-------------

Sphinx is used to provide API documentation for rospkg.  The documents
are stored in the ``doc`` subdirectory.

