"""Bundles common functions for maya.

Befor you use maya with our pipeline, call mayainit at least once. Usually the launcher does that for you.
"""
import os

import maya.standalone
import maya.cmds as cmds

from jukeboxcore import main
import jukeboxmaya
from jukeboxmaya.constants import MAYA_PLUGIN_PATH, BUILTIN_PLUGIN_PATH
from jukeboxmaya.plugins import MayaPluginManager
from jukeboxmaya.menu import MenuManager


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


def init():
    """Initialize the pipeline in maya so everything works

    Init environment and load plugins.
    This also creates the initial Jukebox Menu entry.

    :returns: None
    :rtype: None
    :raises: None
    """
    main.init_environment()
    pluginpath = os.pathsep.join((os.environ.get('JUKEBOX_PLUGIN_PATH', ''), BUILTIN_PLUGIN_PATH))
    os.environ['JUKEBOX_PLUGIN_PATH'] = pluginpath
    try:
        maya.standalone.initialize()
        jukeboxmaya.STANDALONE_INITIALIZED = True
    except RuntimeError as e:
        jukeboxmaya.STANDALONE_INITIALIZED = False
        if str(e) == "maya.standalone may only be used from an external Python interpreter":
            mm = MenuManager.get()
            mm.create_menu("Jukebox", tearOff=True)
    # load plugins
    pmanager = MayaPluginManager.get()
    pmanager.load_plugins()
    load_mayaplugins()
