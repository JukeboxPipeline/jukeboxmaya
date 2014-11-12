#!/usr/bin/env python
"""This launcher can run MayaPlugins in a maya standalone environment

It can also run the core standalone plugins but it is recommended to use the regular jukeboxcore launcher for that.
"""
import argparse
import sys
import traceback

import jukeboxcore.gui.main as guimain
from jukeboxcore import plugins as coreplugins
from jukeboxmaya import plugins as mayaplugins
from jukeboxmaya import main


class Launcher(object):
    """Provides commands and handles argument parsing
    """

    def __init__(self, ):
        """Initialize parsers

        :raises: None
        """
        super(Launcher, self).__init__()
        self.parser = self.setup_core_parser()
        self.subparsers = self.setup_cmd_subparsers(self.parser)
        launchp = self.subparsers.add_parser("launch",
                                             help="Launches maya addons for jukebox.")
        listp = self.subparsers.add_parser("list",
                                           help="List all addons that can be launched with the launch command.")
        self.setup_launch_parser(launchp)
        self.setup_list_parser(listp)

    def setup_core_parser(self, ):
        """Setup the core parser

        :returns: the parser
        :rtype: :class:`argparse.ArgumentParser`
        :raises: None
        """
        parser = argparse.ArgumentParser()
        return parser

    def setup_cmd_subparsers(self, parser):
        """Add a subparser for commands to the given parser

        :param parser: the argument parser to setup
        :type parser: :class:`argparse.ArgumentParser`
        :returns: the subparser action object
        :rtype: action object
        :raises: None
        """
        subparsers = parser.add_subparsers(title="commands",
                                           help="available commands")
        return subparsers

    def setup_launch_parser(self, parser):
        """Setup the given parser for the launch command

        :param parser: the argument parser to setup
        :type parser: :class:`argparse.ArgumentParser`
        :returns: None
        :rtype: None
        :raises: None
        """
        parser.set_defaults(func=self.launch)
        parser.add_argument("addon", help="The jukebox addon to launch. The addon should be a standalone plugin.")

    def launch(self, args, unknown):
        """Launch something according to the provided arguments

        :param args: arguments from the launch parser
        :type args: Namespace
        :param unknown: list of unknown arguments
        :type unknown: list
        :returns: None
        :rtype: None
        :raises: SystemExit
        """
        pm = mayaplugins.MayaPluginManager.get()
        addon = pm.get_plugin(args.addon)
        isgui = isinstance(addon, coreplugins.JB_StandaloneGuiPlugin)
        print "Launching %s..." % args.addon
        addon.run()
        if isgui:
            app = guimain.get_qapp()
            sys.exit(app.exec_())

    def setup_list_parser(self, parser):
        """Setup the given parser for the list command

        :param parser: the argument parser to setup
        :type parser: :class:`argparse.ArgumentParser`
        :returns: None
        :rtype: None
        :raises: None
        """
        parser.set_defaults(func=self.list)

    def list(self, args, unknown):
        """List all addons that can be launched

        :param args: arguments from the launch parser
        :type args: Namespace
        :param unknown: list of unknown arguments
        :type unknown: list
        :returns: None
        :rtype: None
        :raises: None
        """
        pm = mayaplugins.MayaPluginManager.get()
        plugs = pm.get_all_plugins()
        if not plugs:
            print "No standalone addons found!"
            return
        print "Addons:"
        for p in plugs:
            if isinstance(p, coreplugins.JB_StandalonePlugin):
                print "\t%s" % p.__class__.__name__

    def parse_args(self, args=None):
        """Parse the given arguments

        All commands should support executing a function,
        so you can use the arg Namespace like this::

          launcher = Launcher()
          args, unknown = launcher.parse_args()
          args.func(args, unknown) # execute the command

        :param args: arguments to pass
        :type args:
        :returns: the parsed arguments and all unknown arguments
        :rtype: (Namespace, list)
        :raises: None
        """
        if args is None:
            args = sys.argv[1:]
        return self.parser.parse_known_args(args)


def main_func(args=None):
    """Main funcion when executing this module as script

    :param args: commandline arguments
    :type args: list
    :returns: None
    :rtype: None
    :raises: None
    """
    # we have to initialize a gui even if we dont need one right now.
    # as soon as you call maya.standalone.initialize(), a QApplication
    # with type Tty is created. This is the type for conosle apps.
    # Because i have not found a way to replace that, we just init the gui.
    guimain.init_gui()

    main.init()
    launcher = Launcher()
    parsed, unknown = launcher.parse_args(args)
    parsed.func(parsed, unknown)


if __name__ == '__main__':
    try:
        main_func()
    except Exception:
        print traceback.format_exc()
        raw_input("Unexpected Exception. Press enter to exit...")
