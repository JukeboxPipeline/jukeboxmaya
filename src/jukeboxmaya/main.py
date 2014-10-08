"""Bundles common functions for maya.

Befor you use maya with our pipeline, call mayainit at least once. Usually the launcher does that for you.
"""
import os

import maya.cmds as cmds

from jukebox.core.constants import MAYA_PLUGIN_PATH
from jukebox.core.plugins import MayaPluginManager
from jukebox.maya3d.menu import MenuManager


def load_mayaplugins():
    """Loads the maya plugins (not jukebox plugins) of the pipeline

    :returns: None
    :rtype: None
    :raises: None
    """
    mpp = os.environ.get('MAYA_PLUG_IN_PATH')
    if mpp is not None:
        ';'.join([mpp, MAYA_PLUGIN_PATH])
    else:
        mpp = MAYA_PLUGIN_PATH

    # to simply load all plugins inside our plugin path, we override pluginpath temporarly
    os.environ['MAYA_PLUG_IN_PATH'] = MAYA_PLUGIN_PATH
    cmds.loadPlugin(allPlugins=True)
    # then we set the MAYA_PLUG_IN_PATH to the correct value
    # NOTE: this ignores the order of paths in MAYA_PLUG_IN_PATH completely
    os.environ['MAYA_PLUG_IN_PATH'] = mpp


def mayainit():
    """Initialize the pipeline in maya so everything works

    Include third party libs and load plugins.

    :returns: None
    :rtype: None
    :raises: None
    """
    mm = MenuManager.get()
    mm.create_menu("Jukebox", tearOff=True)
    # load plugins
    pmanager = MayaPluginManager.get()
    pmanager.load_plugins()
    load_mayaplugins()
