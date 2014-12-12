import os

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


@pytest.mark.parametrize("nodename, typ",
                         [("jb_reftrack1", "None"),
                          ("jb_reftrack2", "Asset"),
                          ("jb_reftrack3", "Alembic")])
def test_get_typ(nodename, typ, reftrack_nodes, mrefobjinter):
    assert mrefobjinter.get_typ(nodename) == typ


@pytest.mark.parametrize("typ", ["None", "Asset", "Alembic"])
def test_set_typ(typ, reftrack_nodes, mrefobjinter):
    mrefobjinter.set_typ(reftrack_nodes[0], typ)
    assert mrefobjinter.get_typ(reftrack_nodes[0]) == typ


def test_create_refobj(new_scene, mrefobjinter):
    for i in range(10):
        print "Creating node", i
        n = mrefobjinter.create_refobj()
        assert cmds.objExists(n)


@pytest.fixture(scope="function")
def file_with_reftrack(request, tmpdir, parent_reftrack, mrefobjinter):
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


def test_referenced_by(ref_file_with_reftrack, mrefobjinter):
    n = []
    n.append(cmds.createNode("jb_reftrack", name="jb_reftrack1"))
    n.append(cmds.createNode("jb_reftrack", name="jb_reftrack2"))
    n.append(cmds.createNode("jb_reftrack", name="jb_reftrack3"))
    assert cmds.objExists("ref1:jb_reftrack1") is True
    for node in n:
        assert mrefobjinter.referenced_by(node) is None
        assert mrefobjinter.referenced_by("ref1:" + node) == ref_file_with_reftrack
    with pytest.raises(RuntimeError):
        mrefobjinter.referenced_by("asdfasdfasdf")


def test_delete_refobj(parent_reftrack, mrefobjinter):
    for n in parent_reftrack:
        mrefobjinter.delete_refobj(n)
        assert cmds.objExists(n) is False


def test_get_all_refobjs(ref_file_with_reftrack, mrefobjinter):
    cmds.createNode("jb_reftrack", name="jb_reftrack1")
    cmds.createNode("jb_reftrack", name="jb_reftrack2")
    cmds.createNode("jb_reftrack", name="jb_reftrack3")
    allnodes = mrefobjinter.get_all_refobjs()
    assert len(allnodes) == 6
    for n in ["jb_reftrack1", "jb_reftrack2", "jb_reftrack3", "ref1:jb_reftrack1", "ref1:jb_reftrack2", "ref1:jb_reftrack3"]:
        assert n in allnodes
