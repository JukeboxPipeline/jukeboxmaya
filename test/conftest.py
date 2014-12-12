"""This module contains all global fixtures"""

import os

import pytest
import maya.cmds as cmds

import jukeboxmaya.main


@pytest.fixture(scope="session", autouse=True)
def setup_test(request):
    os.environ['JUKEBOX_TESTING'] = 'True'
    jukeboxmaya.main.init()

    # somehow, initializing maya standalone introduces a bug with the coverage
    # coverage warns that the trace function was changed
    # further more it creates a second collector. somehow the collectors
    # are nested wron and we have to inverse the list so they can be closed
    # in the right order.
    # i really do not know exactly what causes the problem
    # mayabe maya does some wierd threading, multiprocessing stuff or
    # really changes the trace function. i don't know, but as soon
    # as maya standalone gets initialized the coverage produces bugs
    # so for now, we add this hacky fix.
    # I read that using --timid for coverage might solve the problem, but it does not
    # somehow the warning only shows up with tox. i don't know why though. maybe just the
    # way the capture log works differently
    def fin():
        from coverage import collector
        colls =  collector.Collector._collectors
        if len(colls) == 2:
            collector.Collector._collectors = list(reversed(colls))
    request.addfinalizer(fin)


@pytest.fixture(scope="function")
def new_scene():
    """Start with a new scene"""
    cmds.file(force=True, new=True)
