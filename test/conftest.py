"""This module contains all global fixtures"""

import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_test():
    os.environ['JUKEBOX_TESTING'] = 'True'


@pytest.fixture(scope="session", autouse=True)
def setup_mayastandalone():
    import maya.standalone
    maya.standalone.initialize()
