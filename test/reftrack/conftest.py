import os

import pytest
import maya.cmds as cmds

from jukeboxmaya.reftrack import refobjinter
from jukeboxmaya.reftrack import asset


@pytest.fixture(scope="function")
def mrefobjinter():
    "Return a fresh MayaRefobjInterface"
    return refobjinter.MayaRefobjInterface()


@pytest.fixture(scope="function")
def assettypinter(mrefobjinter):
    "Return a fresh AssetReftypeInterface"
    return asset.AssetReftypeInterface(mrefobjinter)


@pytest.fixture(scope="function")
def reftrack_nodes(new_scene):
    """Create three reftrack nodes

    jb_reftrack1 - type None
    jb_reftrack2 - type Asset
    jb_reftrack3 - type Alembic
    """
    n = []
    n.append(cmds.createNode("jb_reftrack", name="jb_reftrack1"))
    n.append(cmds.createNode("jb_reftrack", name="jb_reftrack2"))
    n.append(cmds.createNode("jb_reftrack", name="jb_reftrack3"))
    cmds.setAttr("%s.type" % n[1], 1)
    cmds.setAttr("%s.type" % n[2], 2)
    for node in n:
        cmds.lockNode(node, lock=True)
    return n


@pytest.fixture(scope="function")
def parent_reftrack(reftrack_nodes):
    """Parent jb_reftrack1 to jb_reftrack2, and jb_reftrack2 to jb_reftrack3"""
    cmds.connectAttr("%s.parent" % reftrack_nodes[1], "%s.children" % reftrack_nodes[0], nextAvailable=True)
    cmds.connectAttr("%s.parent" % reftrack_nodes[2], "%s.children" % reftrack_nodes[1], nextAvailable=True)
    return reftrack_nodes


@pytest.fixture(scope="function")
def file_with_reftrack(request, tmpdir, parent_reftrack):
    """Return a filename to a scene with the reftracks from parent_reftrack fixture."""
    fn = tmpdir.join("test1.mb")
    f = cmds.file(rename=fn.dirname)
    cmds.file(save=True, type='mayaBinary')

    def fin():
        os.remove(f)

    request.addfinalizer(fin)
    return f


@pytest.fixture(scope="function")
def ref_file_with_reftrack(file_with_reftrack):
    """Reference the file from file_with_reftrack fixture into the scene with namespace 'ref1'.
    Return the reference node."""
    cmds.file(new=True, force=True)
    reffile = cmds.file(file_with_reftrack, reference=True, namespace="ref1")
    return cmds.referenceQuery(reffile, referenceNode=True)  # get reference node
