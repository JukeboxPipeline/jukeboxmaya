#!/usr/bin/env python
"""This script runs all tests for jukebox-maya with the maya python interpreter

Because using an external interpreter causes all kind of problems, this script
runs the tests with mayapy.
This script will execute pytest with the given commandline arguments.
"""
import argparse
import sys

from jukeboxmaya import mayapylauncher


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
    mayapylauncher.setup_environment()
    rc = mayapylauncher.execute_mayapy(args)
    sys.exit(rc)


if __name__ == '__main__':
    main()
