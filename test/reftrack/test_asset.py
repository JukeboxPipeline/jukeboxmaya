import os

import pytest
import maya.cmds as cmds

from jukeboxcore.filesys import TaskFileInfo, JB_File


@pytest.mark.parametrize("refobj", [("a", "b", "c", "d", None, "asdf")])
def test_is_replaceable(refobj, assettypinter):
    # assert always returns True
    assert assettypinter.is_replaceable(refobj) is True


@pytest.fixture(scope="function")
def taskfile_with_dagnodes(request, djprj, mrefobjinter):
    cmds.file(new=True, force=True)
    """Create a scene with a scenenode for djprj.assettaskfiles[0] and
    a dag transform node "testdagnode".
    """
    cmds.createNode("transform", name="testdagnode")
    tf = djprj.assettaskfiles[0]
    scenenode = cmds.createNode("jb_sceneNode")
    cmds.setAttr("%s.taskfile_id" % scenenode, tf.pk)
    tfi = TaskFileInfo(task=tf.task, version=tf.version, releasetype=tf.releasetype,
                               descriptor=tf.descriptor, typ=tf.typ)
    jb = JB_File(tfi)
    jb.create_directory()
    f = cmds.file(rename=jb.get_fullpath())
    cmds.file(save=True, type='mayaBinary')

    def fin():
        os.remove(f)

    request.addfinalizer(fin)
    return f


@pytest.fixture(scope="function")
def taskfile_with_dagnodes2(request, djprj, mrefobjinter):
    cmds.file(new=True, force=True)
    """Create a scene with a scenenode for djprj.assettaskfiles[1] and
    a dag transform node "othertestnode".
    """
    cmds.createNode("transform", name="othertestnode")
    tf = djprj.assettaskfiles[1]
    scenenode = cmds.createNode("jb_sceneNode")
    cmds.setAttr("%s.taskfile_id" % scenenode, tf.pk)
    tfi = TaskFileInfo(task=tf.task, version=tf.version, releasetype=tf.releasetype,
                               descriptor=tf.descriptor, typ=tf.typ)
    jb = JB_File(tfi)
    jb.create_directory()
    f = cmds.file(rename=jb.get_fullpath())
    cmds.file(save=True, type='mayaBinary')

    def fin():
        os.remove(f)

    request.addfinalizer(fin)
    return f


@pytest.fixture(scope="function")
def taskfile_without_dagnodes(request, djprj, mrefobjinter):
    """Create a scene with a scenenode for djprj.assettaskfiles[0].
    """
    cmds.file(new=True, force=True)
    tf = djprj.assettaskfiles[0]
    scenenode = cmds.createNode("jb_sceneNode")
    cmds.setAttr("%s.taskfile_id" % scenenode, tf.pk)
    tfi = TaskFileInfo(task=tf.task, version=tf.version, releasetype=tf.releasetype,
                               descriptor=tf.descriptor, typ=tf.typ)
    jb = JB_File(tfi)
    jb.create_directory()
    f = cmds.file(rename=jb.get_fullpath())
    cmds.file(save=True, type='mayaBinary')

    def fin():
        os.remove(f)

    request.addfinalizer(fin)
    return f


def test_reference_with_dag(taskfile_with_dagnodes, djprj, assettypinter, mrefobjinter):
    cmds.file(new=True, force=True)
    cmds.namespace(add="foo")
    cmds.namespace(set="foo")
    assert cmds.namespaceInfo(absoluteName=True) == ":foo"

    tf = djprj.assettaskfiles[0]
    tfi = TaskFileInfo(task=tf.task, version=tf.version, releasetype=tf.releasetype,
                               descriptor=tf.descriptor, typ=tf.typ)
    refobj = mrefobjinter.create(typ="Asset")
    assettypinter.reference(refobj, tfi)

    # assert namespace is still the same
    assert cmds.namespaceInfo(absoluteName=True) == ":foo"
    refnode = cmds.referenceQuery(taskfile_with_dagnodes, referenceNode=True)
    ns = cmds.referenceQuery(refnode, namespace=True)
    ns = cmds.namespaceInfo(ns, fullName=True)
    assert "%s:testdagnode" % ns in cmds.namespaceInfo(ns, listOnlyDependencyNodes=True)
    assert cmds.listRelatives("%s:testdagnode" % ns, parent=True, type="jb_asset")

    # reference2
    refobj2 = mrefobjinter.create(typ="Asset")
    assettypinter.reference(refobj2, tfi)

    # assert namespace is still the same
    assert cmds.namespaceInfo(absoluteName=True) == ":foo"
    refnode2 = cmds.referenceQuery(taskfile_with_dagnodes + "{1}", referenceNode=True)
    ns2 = cmds.referenceQuery(refnode2, namespace=True)
    ns2 = cmds.namespaceInfo(ns2, fullName=True)
    assert refnode2 != refnode
    assert ns2 != ns
    assert "%s:testdagnode" % ns2 in cmds.namespaceInfo(ns2, listOnlyDependencyNodes=True)
    assert cmds.listRelatives("%s:testdagnode" % ns2, parent=True, type="jb_asset")


def test_reference_without_dag(taskfile_without_dagnodes, djprj, assettypinter, mrefobjinter):
    cmds.file(new=True, force=True)
    cmds.namespace(add="foo")
    cmds.namespace(set="foo")
    assert cmds.namespaceInfo(absoluteName=True) == ":foo"

    tf = djprj.assettaskfiles[0]
    tfi = TaskFileInfo(task=tf.task, version=tf.version, releasetype=tf.releasetype,
                               descriptor=tf.descriptor, typ=tf.typ)
    refobj = mrefobjinter.create(typ="Asset")
    assettypinter.reference(refobj, tfi)

    # assert namespace is still the same
    assert cmds.namespaceInfo(absoluteName=True) == ":foo"
    refnode = cmds.referenceQuery(taskfile_without_dagnodes, referenceNode=True)
    ns = cmds.referenceQuery(refnode, namespace=True)
    ns = cmds.namespaceInfo(ns, fullName=True)
    # assert no group created
    content = cmds.namespaceInfo(ns, listOnlyDependencyNodes=True)
    assert not cmds.ls(content, type="jb_asset")

    # reference2
    refobj2 = mrefobjinter.create(typ="Asset")
    assettypinter.reference(refobj2, tfi)

    # assert namespace is still the same
    assert cmds.namespaceInfo(absoluteName=True) == ":foo"
    refnode2 = cmds.referenceQuery(taskfile_without_dagnodes + "{1}", referenceNode=True)
    ns2 = cmds.referenceQuery(refnode2, namespace=True)
    ns2 = cmds.namespaceInfo(ns2, fullName=True)
    assert refnode2 != refnode
    assert ns2 != ns
    # assert no group created
    content = cmds.namespaceInfo(ns, listOnlyDependencyNodes=True)
    assert not cmds.ls(content, type="jb_asset")


def test_load(taskfile_with_dagnodes, djprj, assettypinter, mrefobjinter):
    cmds.file(new=True, force=True)
    tf = djprj.assettaskfiles[0]
    tfi = TaskFileInfo(task=tf.task, version=tf.version, releasetype=tf.releasetype,
                               descriptor=tf.descriptor, typ=tf.typ)
    refobj = mrefobjinter.create(typ="Asset")
    assettypinter.reference(refobj, tfi)
    refnode = cmds.referenceQuery(taskfile_with_dagnodes, referenceNode=True)
    cmds.file(unloadReference=refnode)
    assert cmds.referenceQuery(refnode, isLoaded=True) is False
    assettypinter.load(refobj, refnode)
    assert cmds.referenceQuery(refnode, isLoaded=True) is True


def test_unload(taskfile_with_dagnodes, djprj, assettypinter, mrefobjinter):
    cmds.file(new=True, force=True)
    tf = djprj.assettaskfiles[0]
    tfi = TaskFileInfo(task=tf.task, version=tf.version, releasetype=tf.releasetype,
                               descriptor=tf.descriptor, typ=tf.typ)
    refobj = mrefobjinter.create(typ="Asset")
    assettypinter.reference(refobj, tfi)
    refnode = cmds.referenceQuery(taskfile_with_dagnodes, referenceNode=True)
    assert cmds.referenceQuery(refnode, isLoaded=True) is True
    assettypinter.unload(refobj, refnode)
    assert cmds.referenceQuery(refnode, isLoaded=True) is False


def test_replace(taskfile_with_dagnodes, taskfile_with_dagnodes2, djprj, assettypinter, mrefobjinter):
    cmds.file(new=True, force=True)
    tf = djprj.assettaskfiles[0]
    tfi = TaskFileInfo(task=tf.task, version=tf.version, releasetype=tf.releasetype,
                               descriptor=tf.descriptor, typ=tf.typ)
    refobj = mrefobjinter.create(typ="Asset")
    assettypinter.reference(refobj, tfi)
    refnode = cmds.referenceQuery(taskfile_with_dagnodes, referenceNode=True)
    ns = cmds.referenceQuery(refnode, namespace=True)
    ns = cmds.namespaceInfo(ns, fullName=True)
    assert "%s:testdagnode" % ns in cmds.ls(type="transform")
    assert "%s:othertestnode" % ns not in cmds.ls(type="transform")
    tf2 = djprj.assettaskfiles[1]
    tfi2 = TaskFileInfo(task=tf2.task, version=tf2.version, releasetype=tf2.releasetype,
                               descriptor=tf2.descriptor, typ=tf2.typ)
    assettypinter.replace(refobj, refnode, tfi2)
    assert "%s:othertestnode" % ns in cmds.ls(type="transform")
    assert "%s:testdagnode" % ns not in cmds.ls(type="transform")


def test_import_taskfile(taskfile_with_dagnodes, djprj, assettypinter, mrefobjinter):
    cmds.file(new=True, force=True)
    tf = djprj.assettaskfiles[0]
    tfi = TaskFileInfo(task=tf.task, version=tf.version, releasetype=tf.releasetype,
                               descriptor=tf.descriptor, typ=tf.typ)
    refobj = mrefobjinter.create(typ="Asset")
    assettypinter.reference(refobj, tfi)
    refnode = cmds.referenceQuery(taskfile_with_dagnodes, referenceNode=True)
    assert cmds.referenceQuery("smurf_1:testdagnode", isNodeReferenced=True) is True

    assettypinter.import_reference(refobj, refnode)

    assert cmds.referenceQuery("smurf_1:testdagnode", isNodeReferenced=True) is False
