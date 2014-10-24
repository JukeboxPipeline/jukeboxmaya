=========
Unittests
=========

For a general introduction on unittesting please read the :ref:`jukeboxcore:unittest` documentation of jukeboxcore.
This chapter will explain the special test setup that is used, so maya can be integrated into the test environment.

---------------
Maya Standalone
---------------

Maya can be started in standalone mode. This is similar to the mayabatch process. The major drawback is, that all maya ui commands
do not work. There is a workaround as you will see :ref:`here <mocking>`.
Inside the test dir is a file called ``conftest.py``. It bundles different fixtures for the session. One of the fixture is to
setup maya standalone. The fixture will be executed at the beginnin of the test session.
Afterwards it is possible to import maya.cmds and use the commands.

Because you test environment probably does not know anything about maya, there is a special testrunner script called ``testrunner.py``,
which executes pytest after setting up the environment. It will find the maya installation on your machine and locate all neccessary dircetories,
that have to be on the pythonpath. So you need Maya 2015 installed in order to test the code.

.. _mocking:

-------
Mocking
-------

Because all maya ui commands do not work, we have to mock them. In ``conftest.py`` is a function that will be responsible for mocking
the commands. If you need some maya ui command that has not been mocked, add a mock in the function.
