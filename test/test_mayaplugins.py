from nose.tools import eq_

import maya.cmds as cmds

from jukeboxmaya.mayaplugins import jbscene


def test_jbsceneplugin():
    node = cmds.createNode('jb_sceneNode')
    cmds.setAttr("%s.taskfile_id" % node, 85)


def test_get_current_scene_node():
    cmds.file(new=True, f=True)
    cmds.namespace(add='somescene')
    cmds.namespace(set='somescene')
    cmds.createNode('jb_sceneNode')
    cmds.namespace(set=':')
    node2 = cmds.createNode('jb_sceneNode')
    cmds.namespace(set='somescene')
    eq_(jbscene.get_current_scene_node(), node2)
