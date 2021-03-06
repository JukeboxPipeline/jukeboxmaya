import os

import pytest
import maya.cmds as cmds

from jukeboxcore import djadapter
from jukeboxcore.reftrack import Reftrack
from jukeboxmaya.reftrack import refobjinter


@pytest.mark.parametrize("nodename", ["jb_reftrack1", "jb_reftrack2", "jb_reftrack3", pytest.mark.xfail("jb_noreftrack")])
def test_exists(nodename, reftrack_nodes, mrefobjinter):
    assert mrefobjinter.exists(nodename) is True


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


def test_set_reference(ref_file_with_reftrack, mrefobjinter):
    n = cmds.createNode("jb_reftrack", name="jb_reftrack1")
    mrefobjinter.set_reference(n, ref_file_with_reftrack)
    assert cmds.listConnections("%s.referencenode" % n, d=False) == [ref_file_with_reftrack]

    mrefobjinter.set_reference(n, None)
    assert cmds.listConnections("%s.referencenode" % n, d=False) is None


def test_get_reference(ref_file_with_reftrack, mrefobjinter):
    n = cmds.createNode("jb_reftrack", name="jb_reftrack1")
    assert mrefobjinter.get_reference(n) is None
    mrefobjinter.set_reference(n, ref_file_with_reftrack)
    assert mrefobjinter.get_reference(n) == ref_file_with_reftrack


def test_get_status(ref_file_with_reftrack, mrefobjinter):
    n = cmds.createNode("jb_reftrack", name="jb_reftrack1")
    assert mrefobjinter.get_status(n) == Reftrack.IMPORTED
    mrefobjinter.set_reference(n, ref_file_with_reftrack)
    assert mrefobjinter.get_status(n) == Reftrack.LOADED
    cmds.file(unloadReference=ref_file_with_reftrack)
    assert mrefobjinter.get_status(n) == Reftrack.UNLOADED


def test_connect_scenenode(reftrack_nodes, mrefobjinter):
    sn = cmds.createNode("jb_sceneNode")
    cmds.setAttr("%s.taskfile_id" % sn, 1)
    mrefobjinter.connect_reftrack_scenenode(reftrack_nodes[0], sn)
    assert cmds.listConnections("%s.scenenode" % reftrack_nodes[0], source=False, plugs=True) == ["%s.reftrack" % sn]
    assert cmds.listConnections("%s.taskfile_id" % reftrack_nodes[0], destination=False, plugs=True) == ["%s.taskfile_id" % sn]


params = [("assettaskfiles", i) for i in range(0, 32, 4)]
params.extend([("shottaskfiles", i) for i in range(0, 32, 4)])


@pytest.mark.parametrize("attr,index", params)
def test_current_element(attr, index, new_scene, djprj, mrefobjinter):
    node = cmds.createNode("jb_sceneNode")
    tf = getattr(djprj, attr)[index]
    cmds.setAttr("%s.taskfile_id" % node, tf.pk)
    assert mrefobjinter.get_current_element() == tf.task.element


def test_current_element_raises(new_scene, mrefobjinter):
    node = cmds.createNode("jb_sceneNode")
    cmds.setAttr("%s.taskfile_id" % node, -123)
    with pytest.raises(djadapter.models.TaskFile.DoesNotExist):
        mrefobjinter.get_current_element()


@pytest.mark.parametrize("index", [i for i in range(0, 32, 4)])
def test_get_taskfile_connected(index, new_scene, djprj, mrefobjinter):
    scenenode = cmds.createNode("jb_sceneNode")
    tf = djprj.assettaskfiles[index]
    cmds.setAttr("%s.taskfile_id" % scenenode, tf.pk)
    refobj = cmds.createNode("jb_reftrack")
    mrefobjinter.connect_reftrack_scenenode(refobj, scenenode)
    mrefobjinter.get_taskfile(refobj)


@pytest.mark.parametrize("index", [i for i in range(0, 32, 4)])
def test_get_taskfile_unconnected(index, new_scene, djprj, mrefobjinter):
    tf = djprj.assettaskfiles[index]
    refobj = cmds.createNode("jb_reftrack")
    cmds.setAttr("%s.taskfile_id" % refobj, tf.pk)
    mrefobjinter.get_taskfile(refobj)
