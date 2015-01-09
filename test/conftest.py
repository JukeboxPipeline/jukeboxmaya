"""This module contains all global fixtures"""

import os
import getpass
import tempfile


import pytest
import django
import maya.cmds as cmds


os.environ['JUKEBOX_TESTING'] = 'True'


@pytest.fixture(scope="session", autouse=True)
def setup_test(request):
    import jukeboxmaya.main
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
    def fix_collector():
        from coverage import collector
        colls =  collector.Collector._collectors
        if len(colls) == 2:
            collector.Collector._collectors = list(reversed(colls))

    def destroy_db():
        test_db = os.environ.get('TEST_DB', None)
        if test_db:
            django.db.connection.creation.destroy_test_db(test_db)

    request.addfinalizer(fix_collector)
    request.addfinalizer(destroy_db)


@pytest.fixture(scope="function")
def new_scene():
    """Start with a new scene"""
    cmds.file(force=True, new=True)


@pytest.fixture(scope='function')
def notestdb(request):
    """Set an environment variable to prevent creating a test database.
    Might be necessary for subprocesses."""
    os.environ['NO_TEST_DB'] = "True"

    def fin():
        os.environ['NO_TEST_DB'] = ""
    request.addfinalizer(fin)


@pytest.fixture(scope='session')
def user():
    from jukeboxcore.djadapter import users
    name = getpass.getuser()
    return users.create_user(username=name)


@pytest.fixture(scope='session')
def prjpath():
    """Return a path for the project of the prj fixture"""
    return os.path.join(tempfile.gettempdir(), "testpixarplants")


class DjangoProjectContainer(object):
    """A container that holds a all
    projects, sequences, shots, assettypes, assets, tasks and taskfiles.
    """

    def __init__(self, ):
        """
        :raises: None
        """
        self.prjs = []
        self.sequences = []
        self.shots = []
        self.atypes = []
        self.assets = []
        self.shotdepartments = []
        self.assetdepartments = []
        self.shottasks = []
        self.assettasks = []
        self.assettaskfiles = []
        self.shottaskfiles = []
        self.assettfis = []
        self.shottfis = []


@pytest.fixture(scope='session')
def djprj(user):
    from jukeboxcore import djadapter as dj
    from jukeboxcore.filesys import TaskFileInfo
    c = DjangoProjectContainer()
    prjpath = os.path.join(tempfile.gettempdir(), "avatar3")
    prj = dj.projects.create(name="Avatar3", short='av3', _path=prjpath, semester='SS14', scale="cm")
    c.prjs.append(prj)

    seqparams = [{'name': 'Seq01', 'description': 'smurfs dancing'},
                 {'name': 'Seq02', 'description': 'smurfs fighting cg crap'}]
    shotparams = [{'name': 'Shot01', 'description': 'smurfs face'},
                  {'name': 'Shot02', 'description': 'more smurfing'}]
    atypeparams = [{'name': 'coolprop', 'description': 'cooler props'},
                   {'name': 'coolchar', 'description': 'cooler characters'}]
    assetparams = [{'name': 'smurf', 'description': 'blue disney character'},
                   {'name': 'gijoe', 'description': 'the stereotypes!'}]
    adepparams = [{'name': 'Texturing', 'short': 'tex'},
                  {'name': 'Sculpting', 'short': 'scp'}]
    sdepparams = [{'name': 'Tracking', 'short': 'trck'},
                  {'name': 'Cleaning', 'short': 'cl'}]
    stfparams = [{'version': 1, 'releasetype': 'release', 'typ': dj.FILETYPES['mayamainscene'], 'descriptor': None},
                 {'version': 2, 'releasetype': 'release', 'typ': dj.FILETYPES['mayamainscene'], 'descriptor': None},
                 {'version': 3, 'releasetype': 'release', 'typ': dj.FILETYPES['mayamainscene'], 'descriptor': None},
                 {'version': 1, 'releasetype': 'work', 'typ': dj.FILETYPES['mayamainscene'], 'descriptor': 'desc1'}]
    atfparams = [{'version': 1, 'releasetype': 'release', 'typ': dj.FILETYPES['mayamainscene'], 'descriptor': None},
                 {'version': 2, 'releasetype': 'release', 'typ': dj.FILETYPES['mayamainscene'], 'descriptor': None},
                 {'version': 3, 'releasetype': 'release', 'typ': dj.FILETYPES['mayamainscene'], 'descriptor': None},
                 {'version': 1, 'releasetype': 'work', 'typ': dj.FILETYPES['mayamainscene'], 'descriptor': 'desc1'}]

    for adepparam in adepparams:
        dep = dj.departments.create(assetflag=True, **adepparam)
        c.assetdepartments.append(dep)
    for sdepparam in sdepparams:
        dep = dj.departments.create(assetflag=False, **sdepparam)
        c.shotdepartments.append(dep)

    for seqparam in seqparams:
        seq = dj.sequences.create(project=prj, **seqparam)
        c.sequences.append(seq)
        for shotparam in shotparams:
            shot = dj.shots.create(project=prj, sequence=seq, **shotparam)
            c.shots.append(shot)

    for atypeparam in atypeparams:
        atype = dj.atypes.create(**atypeparam)
        atype.projects.add(prj)
        atype.save()
        c.atypes.append(atype)
        for assetparam in assetparams:
            asset = dj.assets.create(project=prj, atype=atype, **assetparam)
            c.assets.append(asset)

    for dep in c.shotdepartments:
        for s in c.shots:
            task = dj.tasks.create(department=dep, project=prj, status='New', element=s)
            c.shottasks.append(task)
            for stfparam in stfparams:
                tfile = dj.taskfiles.create(task=task,
                                            user=user,
                                            path="%s%s%s%s%s%s" % (prj.name,
                                                                   s.sequence.name,
                                                                   s.name, dep.short,
                                                                   stfparam['releasetype'],
                                                                   stfparam['version']),
                                            **stfparam)
                c.shottaskfiles.append(tfile)
                tfileinfo = TaskFileInfo(task=tfile.task,
                                         version=tfile.version,
                                         releasetype=tfile.releasetype,
                                         typ=tfile.typ,
                                         descriptor=tfile.descriptor)
                c.shottfis.append(tfileinfo)
    for dep in c.assetdepartments:
        for a in c.assets:
            task = dj.tasks.create(department=dep, project=prj, status='New', element=a)
            c.assettasks.append(task)
            for atfparam in atfparams:
                tfile = dj.taskfiles.create(task=task,
                                            user=user,
                                            path="%s%s%s%s%s%s" % (prj.name,
                                                                   a.atype.name,
                                                                   a.name,
                                                                   dep.short,
                                                                   atfparam['releasetype'],
                                                                   atfparam['version']),
                                            **atfparam)
                c.assettaskfiles.append(tfile)
                tfileinfo = TaskFileInfo(task=tfile.task,
                                         version=tfile.version,
                                         releasetype=tfile.releasetype,
                                         typ=tfile.typ,
                                         descriptor=tfile.descriptor)
                c.assettfis.append(tfileinfo)

    for shot in c.shots:
        for asset in c.assets[:-2]:
            shot.assets.add(asset)

    return c
