import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya

from jukeboxcore.errors import PluginInitError, PluginUninitError


class JB_SceneNode(OpenMayaMPx.MPxNode):
    kNodeName = 'jb_sceneNode'
    kPluginNodeId = OpenMaya.MTypeId(0x14B01)

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)


def creator():
    return OpenMayaMPx.asMPxPtr(JB_SceneNode())


def initialize():
    #tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()

    JB_SceneNode.taskfile_id = nAttr.create('taskfile_id', 'tfid', OpenMaya.MFnNumericData.kInt)
    JB_SceneNode.addAttribute(JB_SceneNode.taskfile_id)


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'David Zuber', '1.0', 'Any')
    try:
        plugin.registerNode(JB_SceneNode.kNodeName, JB_SceneNode.kPluginNodeId, creator, initialize)
    except:
        raise PluginInitError('Failed to register %s node' % JB_SceneNode.kNodeName)


def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(JB_SceneNode.kPluginNodeId)
    except:
        raise PluginUninitError('Failed to unregister %s node' % JB_SceneNode.kNodeName)
