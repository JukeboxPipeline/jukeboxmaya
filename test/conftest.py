"""This module contains all global fixtures"""

import os

import mock
import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_test():
    os.environ['JUKEBOX_TESTING'] = 'True'


def mock_maya_ui_cmds():
    """Mock the Maya Ui commands

    Be sure that maya.standalone is initialized before using this function

    :returns: None
    :rtype: None
    :raises: None
    """
    import maya.cmds as cmds
    cmds.setParent = mock.Mock()
    cmds.menu = mock.Mock(return_value="mockedmenu")
    cmds.menuItem = mock.Mock(return_value="mockedmenuitem")
    cmds.deleteUi = mock.Mock()


@pytest.fixture(scope="session", autouse=True)
def setup_mayastandalone():
    import maya.standalone
    maya.standalone.initialize()
    mock_maya_ui_cmds()
