"""This module contains all global fixtures"""

import os

import pytest


@pytest.fixture(scope="session")
def setup_test():
    os.environ['JUKEBOX_TESTING'] = 'True'
