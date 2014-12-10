import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya

from jukeboxcore.errors import PluginInitError, PluginUninitError


class JB_AssetNode(OpenMayaMPx.MPxNode):
    """A transform node for assets

    Used to group the dag content of assets
    """
    kNodeName = 'jb_asset'
    kPluginNodeId = OpenMaya.MTypeId(0x14B03)

    def __init__(self):
        super(JB_AssetNode, self).__init__()


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'David Zuber', '1.0', 'Any')
    try:
        plugin.registerNode(JB_AssetNode.kNodeName, JB_AssetNode.kPluginNodeId, JB_AssetNode.creator, JB_AssetNode.initialize)
    except:
        raise PluginInitError('Failed to register %s node' % JB_AssetNode.kNodeName)


def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(JB_AssetNode.kPluginNodeId)
    except:
        raise PluginUninitError('Failed to unregister %s node' % JB_AssetNode.kNodeName)
