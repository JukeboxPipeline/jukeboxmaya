""" This package bundles all functionality for Autodesk Maya.

Inside the maya3d module (the __init__.py) are functions, that can be executed, before maya is launched.
To make that possible, it is important not to import anything from maya3d from inside this __init__.py.
"""
import os
import sys

from jukebox.core import ostool
from jukebox.core.constants import MAYA_XBMLANGPATH


def init_maya_env():
    """ Set environment variables that are important for maya before and after launch.

    :returns: None
    :rtype: None
    :raises: None
    """
    # XBMLANGPATH for Maya to find Images and Icons there
    xbm = os.environ.get('XBMLANGPATH', None)
    if xbm is None:
        xbm = MAYA_XBMLANGPATH
    else:
        xbm = ';'.join((xbm, MAYA_XBMLANGPATH))
    os.environ['XBMLANGPATH'] = xbm


def start_maya_standalone(name='python'):
    """ Start a maya standalone instance. Somewhat equivalent to the batchmode

    Setup environment needed for maya standalone.
    Then initialize maya standalone.
    After this function has been called you can use the maya.cmds commands
    or the OpenMaya API. Please note that the usual batchmode restrictions apply!
    You cannot use any of the UI commands.

    :param name: Give your standalone app a name. Default is 'python'. This argument will be passed to the maya.standalone.initialize function call.
    :type name: str
    :returns: None
    :rtype: None
    :raises: None
    """
    # setup maya standalone
    osinter = ostool.get_interface()
    mayaloc = osinter.get_maya_location()
    mayasite = osinter.get_maya_sitepackage_dir()
    sys.path.append(mayasite)
    os.environ['MAYA_LOCATION'] = mayaloc

    # run maya standalone
    import maya.standalone
    maya.standalone.initialize(name=name)
