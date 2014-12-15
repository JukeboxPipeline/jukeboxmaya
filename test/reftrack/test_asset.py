import os

import pytest
import maya.cmds as cmds

from jukeboxcore.filesys import TaskFileInfo, JB_File


@pytest.mark.parametrize("refobj", [("a", "b", "c", "d", None, "asdf")])
def test_is_replaceable(refobj, typinter):
    # assert always returns True
    assert typinter.is_replaceable(refobj) is True


@pytest.fixture(scope="function")
def taskfile_with_reftrack(request, new_scene, djprj):
    tf = djprj.assettaskfiles[0]
    tfi = TaskFileInfo(task=tf.task, version=tf.version, releasetype=tf.releasetype,
                               descriptor=tf.descriptor, typ=tf.typ)
    jb = JB_File(tfi)
    f = cmds.file(rename=jb.get_fullpath())
    cmds.file(save=True, type='mayaBinary')

    def fin():
        os.remove(f)

    request.addfinalizer(fin)
    return f
