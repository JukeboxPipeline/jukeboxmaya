import os
import sys

os.environ['JUKEBOX_TESTING'] = 'True'

from jukeboxcore import ostool


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
    mayabin = osinter.get_maya_bin()
    sys.path.append(mayasite)

    os.environ['MAYA_LOCATION'] = mayaloc
    #This is not documented but necessary. At least on windows.
    os.environ["PATH"] = os.pathsep.join((os.environ.get("PATH", ""), mayabin))
    # run maya standalone
    import maya.standalone
    maya.standalone.initialize(name=name)


start_maya_standalone()
