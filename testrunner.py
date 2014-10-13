#!/usr/bin/env python
"""This script runs all tests for jukebox-maya with the maya python interpreter

Because using an external interpreter causes all kind of problems, this script
runs the tests with mayapy.
This script will execute pytest with the given commandline arguments.
"""
import argparse
import os
import subprocess
import sys

from jukeboxcore import ostool


def setup_argparse():
    """Set up the argument parser and return it

    :returns: the parser
    :rtype: :class:`argparse.ArgumentParser`
    :raises: None
    """
    parser = argparse.ArgumentParser(
        description="Run tests with the maya python intepreter.\
        py.test is used for running the tests. All options will be\
        propagated to py.test.")
    return parser


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


def execute_mayapy(args):
    """Execute mayapython with the given arguments, capture and return the output

    :param args: arguments for the maya python intepreter
    :type args: list
    :returns: the returncode and the captured output
    :rtype: int, string
    :raises: None
    """
    osinter = ostool.get_interface()
    mayapy = osinter.get_maya_python()
    allargs = [mayapy]
    allargs.extend(args)
    print "Executing mayapy. This might take a while. Arguments used: %s" % allargs
    mayapyprocess = subprocess.Popen(allargs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (out, err) = mayapyprocess.communicate()
    mayapyprocess.wait()  # make sure returncode is set!
    print "Process mayapy finished!"
    return mayapyprocess.returncode, out


def main(argv=sys.argv[1:]):
    """Parse commandline arguments and run the tests

    :param argv:
    :type argv:
    :returns: None
    :rtype: None
    :raises: None
    """
    parser = setup_argparse()
    args = ["-m", "pytest"]
    options = parser.parse_known_args(argv)[1]
    args.extend(options)
    setup_environment()
    rc, output = execute_mayapy(args)
    # print one line at a time, so it is less unlikely to run
    # out of space. if the line is really long, this will fail
    # with an IOError.
    for l in output.split("\n"):
        print l
    sys.exit(rc)


if __name__ == '__main__':
    main()
