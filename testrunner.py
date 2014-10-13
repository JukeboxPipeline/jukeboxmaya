#!/usr/bin/env python
"""This script runs all tests for jukebox-maya with the maya python interpreter

Because using an external interpreter causes all kind of problems, this script
runs the tests with mayapy.exe
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
        py.test is used for running the tests.")
    return parser


def setup_environment():
    """Set up neccessary environment variables

    :returns: None
    :rtype: None
    :raises: None
    """
    print os.environ['PATH']
    pypath = ''
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
    print "Executing mayapy with: %s" % allargs
    mayapyprocess = subprocess.Popen(allargs, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (out, err) = mayapyprocess.communicate()
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
    print output
    sys.exit(rc)


if __name__ == '__main__':
    main()
