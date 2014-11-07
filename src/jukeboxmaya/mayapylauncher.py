#!/usr/bin/env python
"""This module provides a way to launch a new mayapy process.

:func:`mayapy_launcher` is supposed to call the regular jukeboxmaya launcher
but with tha maya python intepreter. It will setup the necessary environment and
transver all arguments to the launcher who handles argparsing etc.

You can also call the :func:`mayapy_launcher` via console_scripts and gui_scripts entry points of setuptools.
To use execute::

  $ jukeboxmayapy -h

or for guiscripts::

  $ jukeboxmayapyw -h

You can also execute this script directly!
"""


import os
import subprocess
import sys

from jukeboxcore import ostool


def setup_environment():
    """Set up neccessary environment variables

    This appends all path of sys.path to the python path
    so mayapy will find all installed modules.
    We have to make sure, that we use maya libs instead of
    libs of the virtual env. So we insert all the libs for mayapy
    first.

    :returns: None
    :rtype: None
    :raises: None
    """
    osinter = ostool.get_interface()
    pypath = osinter.get_maya_envpath()
    for p in sys.path:
        pypath = os.pathsep.join((pypath, p))
    os.environ['PYTHONPATH'] = pypath


def execute_mayapy(args, wait=True):
    """Execute mayapython with the given arguments, capture and return the output

    :param args: arguments for the maya python intepreter
    :type args: list
    :param wait: If True, waits for the process to finish and returns the returncode.
                 If False, just returns the process
    :type wait: bool
    :returns: if wait is True, the returncode, else the process
    :rtype: int|:class:`subprocess.Popen`
    :raises: None
    """
    osinter = ostool.get_interface()
    mayapy = osinter.get_maya_python()
    allargs = [mayapy]
    allargs.extend(args)
    print "Executing mayapy with: %s" % allargs
    mayapyprocess = subprocess.Popen(allargs)
    if wait:
        rc = mayapyprocess.wait()
        print "Process mayapy finished!"
        return rc
    else:
        return mayapyprocess


def mayapy_launcher(args=None, wait=True):
    """Start a new subprocess with mayapy and call the :func:`jukeboxmaya.launcher.main_func`.

    So this can be used when launching jukeboxmaya from an external intepreter but
    you want to actually use the mayapy intepreter instead (because it\'s less buggy).

    :param args: arguments for the launcher. If None, sys.argv[1:] is used
    :type args: list
    :param wait: If True, waits for the process to finish and returns the returncode.
                 If False, just returns the process
    :type wait: bool
    :returns: if wait is True, the returncode, else the process
    :rtype: int|:class:`subprocess.Popen`
    """
    if args is None:
        args = sys.argv[1:]
    arguments = ["-m",  "jukeboxmaya.launcher"]
    arguments.extend(args)
    setup_environment()
    return execute_mayapy(arguments, wait)


if __name__ == '__main__':
    rc = mayapy_launcher()
    sys.exit(rc)
