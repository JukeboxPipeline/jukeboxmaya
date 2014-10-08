import os

import jukebox.maya3d.main


def test_mayainit():
    """ Init pipeline in maya

    :returns: None
    :rtype: None
    :raises: None
    """
    jpp = os.environ.get('JUKEBOX_PLUGIN_PATH', '')
    os.environ['JUKEBOX_PLUGIN_PATH'] = ';'.join((jpp, os.path.abspath("jukebox/tests/testplugins")))
    jukebox.maya3d.main.mayainit()
