import pytest
import maya.cmds as cmds

from jukeboxmaya.reftrack import refobjinter


@pytest.fixture(scope="function")
def mrefobjinter():
    "Return a fresh MayaRefobjInterface"
    return refobjinter.MayaRefobjInterface()


@pytest.fixture(scope="function")
def reftrack_nodes(new_scene):
    """Create three reftrack nodes

    jb_reftrack1, jb_reftrack1, jb_reftrack1
    """
    n = []
    n.append(cmds.createNode("jb_reftrack", name="jb_reftrack1"))
    n.append(cmds.createNode("jb_reftrack", name="jb_reftrack2"))
    n.append(cmds.createNode("jb_reftrack", name="jb_reftrack3"))
    return n


@pytest.mark.parametrize("nodename", ["jb_reftrack1", "jb_reftrack2", "jb_reftrack3", pytest.mark.xfail("jb_noreftrack")])
def test_exists(nodename, reftrack_nodes, mrefobjinter):
    assert mrefobjinter.exists(nodename) is True


@pytest.fixture(scope="function")
def parent_reftrack(reftrack_nodes):
    """Parent jb_reftrack1 to jb_reftrack2, and jb_reftrack2 to jb_reftrack3"""
    cmds.connectAttr("%s.parent" % reftrack_nodes[1], "%s.children" % reftrack_nodes[0], nextAvailable=True)
    cmds.connectAttr("%s.parent" % reftrack_nodes[2], "%s.children" % reftrack_nodes[1], nextAvailable=True)
    return reftrack_nodes


@pytest.mark.parametrize("nodename, parent",
                         [("jb_reftrack1", None),
                          ("jb_reftrack2", "jb_reftrack1"),
                          ("jb_reftrack3", "jb_reftrack2")])
def test_get_parent(nodename, parent, parent_reftrack, mrefobjinter):
    assert mrefobjinter.get_parent(nodename) == parent


def test_set_parent(reftrack_nodes, mrefobjinter):
    mrefobjinter.set_parent(reftrack_nodes[1], reftrack_nodes[0])
    assert cmds.listConnections("%s.parent" % reftrack_nodes[1], source=False) == [reftrack_nodes[0]]
    mrefobjinter.set_parent(reftrack_nodes[1], None)
    assert cmds.listConnections("%s.parent" % reftrack_nodes[1], source=False) is None
    mrefobjinter.set_parent(reftrack_nodes[1], reftrack_nodes[0])
    mrefobjinter.set_parent(reftrack_nodes[2], reftrack_nodes[1])
    assert cmds.listConnections("%s.parent" % reftrack_nodes[2], source=False) == [reftrack_nodes[1]]
    mrefobjinter.set_parent(reftrack_nodes[0], None)
    assert cmds.listConnections("%s.parent" % reftrack_nodes[0], source=False) is None
    mrefobjinter.set_parent(reftrack_nodes[2], reftrack_nodes[0])
    assert cmds.listConnections("%s.children" % reftrack_nodes[0], destination=False) == [reftrack_nodes[1], reftrack_nodes[2]]
    assert cmds.listConnections("%s.children" % reftrack_nodes[1], destination=False) is None


def test_get_children(reftrack_nodes, mrefobjinter):
    mrefobjinter.set_parent(reftrack_nodes[1], reftrack_nodes[0])
    mrefobjinter.set_parent(reftrack_nodes[2], reftrack_nodes[0])
    assert mrefobjinter.get_children(reftrack_nodes[0]) == [reftrack_nodes[1], reftrack_nodes[2]]
    assert mrefobjinter.get_children(reftrack_nodes[1]) == []
    assert mrefobjinter.get_children(reftrack_nodes[2]) == []
    mrefobjinter.set_parent(reftrack_nodes[2], reftrack_nodes[1])
    assert mrefobjinter.get_children(reftrack_nodes[0]) == [reftrack_nodes[1]]
    assert mrefobjinter.get_children(reftrack_nodes[1]) == [reftrack_nodes[2]]
    assert mrefobjinter.get_children(reftrack_nodes[2]) == []
