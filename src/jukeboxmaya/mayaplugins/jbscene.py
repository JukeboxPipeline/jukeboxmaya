import maya.cmds as cmds
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya

from jukeboxcore.errors import PluginInitError, PluginUninitError


class JB_SceneNode(OpenMayaMPx.MPxNode):
    """A scene description node

    Stores pipeline relevant information about the current scene. Used to identify a scene.
    """
    kNodeName = 'jb_sceneNode'
    kPluginNodeId = OpenMaya.MTypeId(0x14B01)

    def __init__(self):
        super(JB_SceneNode, self).__init__()

    @classmethod
    def initialize(cls):
        nAttr = OpenMaya.MFnNumericAttribute()
        msgAttr = OpenMaya.MFnMessageAttribute()

        cls.taskfile_id = nAttr.create('taskfile_id', 'tfid', OpenMaya.MFnNumericData.kInt)
        cls.addAttribute(cls.taskfile_id)

        # reftrack link
        cls.reftrack_attr = msgAttr.create("reftrack", "rt")
        msgAttr.setReadable(False)
        cls.addAttribute(cls.reftrack_attr)

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(cls())


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'David Zuber', '1.0', 'Any')
    try:
        plugin.registerNode(JB_SceneNode.kNodeName, JB_SceneNode.kPluginNodeId, JB_SceneNode.creator, JB_SceneNode.initialize)
    except:
        raise PluginInitError('Failed to register %s node' % JB_SceneNode.kNodeName)


def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(JB_SceneNode.kPluginNodeId)
    except:
        raise PluginUninitError('Failed to unregister %s node' % JB_SceneNode.kNodeName)


def get_current_scene_node():
    """Return the name of the jb_sceneNode, that describes the current scene or None if there is no scene node.

    :returns: the full name of the node or none, if there is no scene node
    :rtype: str | None
    :raises: None
    """
    c = cmds.namespaceInfo(':', listOnlyDependencyNodes=True, absoluteName=True)
    l = cmds.ls(c, type='jb_sceneNode', absoluteName=True)
    if not l:
        return
    else:
        for n in sorted(l):
            if not cmds.listConnections("%s.reftrack" % n, d=False):
                return n
