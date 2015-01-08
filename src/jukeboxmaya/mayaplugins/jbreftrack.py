import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya

from jukeboxcore.errors import PluginInitError, PluginUninitError


class JB_ReftrackNode(OpenMayaMPx.MPxNode):
    """A node to track references

    Stores the associated refernce node, typ (asset, cache, shader, cam, lightrig etc), children, and jb_scenenode.
    The reference node is used to track which reference node is responsible. Imported files do not have a connection to a ref node.
    The type is responsible for the actions that take place when referencing, deleting etc.
    Children are other reftrack nodes that should be deleted when reftrack is deleted.
    The scene node is used to track which file is actually imported/refernced.
    If the file is unloaded, there is no jb_scenenode but a reference node.
    """
    kNodeName = 'jb_reftrack'
    kPluginNodeId = OpenMaya.MTypeId(0x14B02)

    types = ["None", "Asset", "Alembic", "Shader", "Camera", "Lightrig"]
    """A list of possible types of references, like asset, cache, shader, camera, lightrig."""

    def __init__(self):
        super(JB_ReftrackNode, self).__init__()

    @classmethod
    def initialize(cls):
        enumAttr = OpenMaya.MFnEnumAttribute()
        msgAttr = OpenMaya.MFnMessageAttribute()
        typedAttr = OpenMaya.MFnTypedAttribute()
        nAttr = OpenMaya.MFnNumericAttribute()

        # typ enum attribute
        cls.typ_attr = enumAttr.create('type', 'typ', 0)
        enumAttr.setConnectable(False)
        for i, t in enumerate(cls.types):
            enumAttr.addField(t, i)
        cls.addAttribute(cls.typ_attr)

        # namespace attribute
        cls.ns_attr = typedAttr.create("namespace", "ns", OpenMaya.MFnData.kString)
        cls.addAttribute(cls.ns_attr)

        # ref node attribute
        cls.ref_attr = msgAttr.create("referencenode", "ref")
        msgAttr.setReadable(False)
        cls.addAttribute(cls.ref_attr)

        # parent attribute
        cls.parent_attr = msgAttr.create("parent", "p")
        msgAttr.setWritable(False)
        cls.addAttribute(cls.parent_attr)

        # children attribute
        cls.children_attr = msgAttr.create("children", "c")
        msgAttr.setReadable(False)
        msgAttr.setArray(True)
        msgAttr.setIndexMatters(False)
        cls.addAttribute(cls.children_attr)

        # the jb_scene node attribute
        cls.scenenode_attr = msgAttr.create("scenenode", "scene")
        msgAttr.setWritable(False)
        cls.addAttribute(cls.scenenode_attr)

        # the taskfile_id in case, we do not have a jb_scene node to connect to
        cls.taskfile_id = nAttr.create('taskfile_id', 'tfid', OpenMaya.MFnNumericData.kInt)
        cls.addAttribute(cls.taskfile_id)

        # the identifier attribute, we need to order the reftracks in the id permanently
        cls.identifier_attr = nAttr.create('identifier', 'id', OpenMaya.MFnNumericData.kInt, -1)
        cls.addAttribute(cls.identifier_attr)

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(cls())

    @classmethod
    def add_type(cls, typ):
        """Register a type for jb_reftrack nodes.

        A type specifies how the reference should be handled. For example the type shader will connect shaders
        with the parent when it the shaders are loaded.
        Default types are :data:`JB_ReftrackNode.types`.

        .. Note:: You have to add types before you initialize the plugin!

        :param typ: a new type specifier, e.g. \"asset\"
        :type typ: str
        :returns: None
        :rtype: None
        :raises: :class:`TypeError`
        """
        if not isinstance(typ, basestring):
            raise TypeError("The type should be a string. But is %s" % type(typ))
        cls.types.append(typ)


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'David Zuber', '1.0', 'Any')
    try:
        plugin.registerNode(JB_ReftrackNode.kNodeName, JB_ReftrackNode.kPluginNodeId, JB_ReftrackNode.creator, JB_ReftrackNode.initialize)
    except:
        raise PluginInitError('Failed to register %s node' % JB_ReftrackNode.kNodeName)


def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(JB_ReftrackNode.kPluginNodeId)
    except:
        raise PluginUninitError('Failed to unregister %s node' % JB_ReftrackNode.kNodeName)
