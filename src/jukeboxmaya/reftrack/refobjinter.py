"""Implementation of :class:`jukeboxcore.reftrack.RefobjInterface` for Maya.

We depend heavily on the :class:`JB_ReftrackNode`. It is used as the refobject.
These nodes can be connected to signal a parent child relationship. Via a connection to a scenenode/reference node we can query
the needed informations.
"""
import maya.cmds as cmds

from jukeboxcore import djadapter
from jukeboxcore.reftrack import RefobjInterface, Reftrack
from jukeboxmaya import common
from jukeboxmaya.mayaplugins import jbscene
from jukeboxmaya.mayaplugins.jbreftrack import JB_ReftrackNode
from jukeboxmaya.reftrack.asset import AssetReftypeInterface


class MayaRefobjInterface(RefobjInterface):
    """Interface to interact mainly with the :class:`JB_ReftrackNode`.

    To interact with the content of each entity, there is a special reftyp interface that
    is not only software specific but also handles only a certain type of entity.
    You can register additional type interfaces, so plugins can introduce their own entity types.
    See :data:`MayaRefobjInterface.types`. When subclassing you could replace it in your class with a
    dictionary of :class:`MayaReftypeInterface`. Or you can call :meth:`MayaRefobjInterface.register_type` at runtime.
    A type could be "Asset", "Alembic", "Camera" etc.
    """

    types = {'Asset': AssetReftypeInterface}
    """A dictionary that maps types of entities (strings) to the reftypinterface class"""

    def __init__(self, ):
        """Initialize a new refobjinterface.

        :raises: None
        """
        super(MayaRefobjInterface, self).__init__()

    def exists(self, refobj):
        """Check if the given :class:`JB_ReftrackNode` is still in the scene
        or if it has been deleted/dissapeared

        :param refobj: a reftrack node to query
        :type refobj: str
        :returns: True, if it still exists
        :rtype: :class:`bool`
        :raises: None
        """
        return cmds.objExists(refobj)

    def get_parent(self, refobj):
        """Return the parent of the given :class:`JB_ReftrackNode`.

        :param refobj: a reftrack node to query
        :type refobj: str
        :returns: the parent reftrack node
        :rtype: refobj | None
        :raises: None
        """
        c = cmds.listConnections("%s.parent" % refobj, source=False)
        return c[0] if c else None

    def set_parent(self, child, parent):
        """Set the parent of the child reftrack node

        :param child: the child reftrack node
        :type child: str
        :param parent: the parent reftrack node
        :type parent: str
        :returns: None
        :rtype: None
        :raises: None
        """
        parents = cmds.listConnections("%s.parent" % child, plugs=True, source=True)
        if parents:
            # there is only one parent at a time
            cmds.disconnectAttr("%s.parent" % child, "%s" % parents[0])
        if parent:
            cmds.connectAttr("%s.parent" % child, "%s.children" % parent, force=True, nextAvailable=True)

    def get_children(self, refobj):
        """Get the children reftrack nodes of the given node

        It is the reverse query of :meth:`RefobjInterface.get_parent`

        :param refobj: the parent reftrack node
        :type refobj: str
        :returns: a list with children reftrack nodes
        :rtype: list
        :raises: None
        """
        children = cmds.listConnections("%s.children" % refobj, d=False)
        if not children:
            children = []
        return children

    def get_typ(self, refobj):
        """Return the entity type of the given reftrack node

        See: :data:`MayaRefobjInterface.types`.

        :param refobj: the reftrack node to query
        :type refobj: str
        :returns: the entity type
        :rtype: str
        :raises: ValueError
        """
        enum = cmds.getAttr("%s.type" % refobj)
        try:
            return JB_ReftrackNode.types[enum]
        except IndexError:
            raise ValueError("The type on the node %s could not be associated with an available type: %s" %
                             (refobj, JB_ReftrackNode.types))

    def set_typ(self, refobj, typ):
        """Set the type of the given refobj

        :param refobj: the reftrack node to edit
        :type refobj: refobj
        :param typ: the entity type
        :type typ: str
        :returns: None
        :rtype: None
        :raises: ValueError
        """
        try:
            enum = JB_ReftrackNode.types.index(typ)
        except ValueError:
            raise ValueError("The given type %s could not be found in available types: %" % (typ, JB_ReftrackNode.types))
        cmds.setAttr("%s.type" % refobj, enum)

    def get_id(self, refobj):
        """Return the identifier of the given refobject

        :param refobj: the refobj to query
        :type refobj: refobj
        :returns: the refobj id. Used to identify refobjects of the same parent, element and type in the UI
        :rtype: int
        :raises: None
        """
        return cmds.getAttr("%s.identifier" % refobj)

    def set_id(self, refobj, identifier):
        """Set the identifier on the given refobj

        :param refobj: the refobj to edit
        :type refobj: refobj
        :param identifier: the refobj id. Used to identify refobjects of the same parent, element and type in the UI
        :type identifier: int
        :returns: None
        :rtype: None
        :raises: None
        """
        cmds.setAttr("%s.identifier" %refobj, identifier)

    def create_refobj(self, ):
        """Create and return a new reftrack node

        :returns: the new reftrack node
        :rtype: str
        :raises: None
        """
        n = cmds.createNode("jb_reftrack")
        cmds.lockNode(n, lock=True)
        return n

    def referenced_by(self, refobj):
        """Return the reference that holds the given reftrack node.

        Returns None if it is imported/in the current scene.

        :param refobj: the reftrack node to query
        :type refobj: str
        :returns: the reference node that holds the given refobj
        :rtype: str | None
        :raises: None
        """
        try:
            ref = cmds.referenceQuery(refobj, referenceNode=True)
            return ref
        except RuntimeError as e:
            if str(e).endswith("' is not from a referenced file.\n"):
                return None
            else:
                raise e

    def delete(self, refobj):
        """Delete the given refobj and the contents of the entity

        :param refobj: the refobj to delete
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        super(MayaRefobjInterface, self).delete(refobj)

    def delete_refobj(self, refobj):
        """Delete the given reftrack node

        :param refobj: the node to delete
        :type refobj: str
        :returns: None
        :rtype: None
        :raises: None
        """
        with common.locknode(refobj, lock=False):
            cmds.delete(refobj)

    def get_all_refobjs(self, ):
        """Return all refobjs in the scene

        :returns: all refobjs in the scene
        :rtype: list
        :raises: None
        """
        return cmds.ls(type="jb_reftrack")

    def get_current_element(self, ):
        """Return the currently open Shot or Asset

        :returns: the currently open element
        :rtype: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot` | None
        :raises: :class:`djadapter.models.TaskFile.DoesNotExist`
        """
        n = jbscene.get_current_scene_node()
        if not n:
            return None
        tfid = cmds.getAttr("%s.taskfile_id" % n)
        try:
            tf = djadapter.taskfiles.get(pk=tfid)
            return tf.task.element
        except djadapter.models.TaskFile.DoesNotExist:
            raise djadapter.models.TaskFile.DoesNotExist("Could not find the taskfile that was set on the scene node. Id was %s" % tfid)

    def set_reference(self, refobj, reference):
        """Connect the given reftrack node with the given refernce node

        :param refobj: the reftrack node to update
        :type refobj: str
        :param reference: the reference node
        :type reference: str
        :returns: None
        :rtype: None
        :raises: None
        """
        refnodeattr = "%s.referencenode" % refobj
        if reference:
            cmds.connectAttr("%s.message" % reference, refnodeattr, force=True)
            ns = cmds.referenceQuery(reference, namespace=True)
            cmds.setAttr("%s.namespace" % refobj, ns, type="string")
        else:
            conns = cmds.listConnections(refnodeattr, plugs=True)
            if not conns:
                return
            for c in conns:
                cmds.disconnectAttr(c, refnodeattr)

    def get_reference(self, refobj):
        """Return the reference node that the reftrack node is connected to or None if it is imported.

        :param refobj: the reftrack node to query
        :type refobj: str
        :returns: the reference node
        :rtype: str | None
        :raises: None
        """
        c = cmds.listConnections("%s.referencenode" % refobj, d=False)
        return c[0] if c else None

    def get_status(self, refobj):
        """Return the status of the given reftrack node

        See: :data:`Reftrack.LOADED`, :data:`Reftrack.UNLOADED`, :data:`Reftrack.IMPORTED`.

        :param refobj: the reftrack node to query
        :type refobj: str
        :returns: the status of the given reftrack node
        :rtype: str
        :raises: None
        """
        reference = self.get_reference(refobj)
        return Reftrack.IMPORTED if not reference else Reftrack.LOADED if cmds.referenceQuery(reference, isLoaded=True) else Reftrack.UNLOADED

    def get_taskfile(self, refobj):
        """Return the taskfile that is loaded and represented by the refobj

        :param refobj: the reftrack node to query
        :type refobj: str
        :returns: The taskfile that is loaded in the scene
        :rtype: :class:`jukeboxcore.djadapter.TaskFile`
        :raises: None
        """
        tfid = cmds.getAttr("%s.taskfile_id" % refobj)
        try:
            return djadapter.taskfiles.get(pk=tfid)
        except djadapter.models.TaskFile.DoesNotExist:
            raise djadapter.models.TaskFile.DoesNotExist("Could not find the taskfile that was set on the node %s. Id was %s" % (refobj, tfid))

    def connect_reftrack_scenenode(self, refobj, scenenode):
        """Connect the given reftrack node with the given scene node

        :param refobj: the reftrack node to connect
        :type refobj: str
        :param scenenode: the jb_sceneNode to connect
        :type scenenode: str
        :returns: None
        :rtype: None
        :raises: None
        """
        conns = [("%s.scenenode" % refobj, "%s.reftrack" % scenenode),
                 ("%s.taskfile_id" % scenenode, "%s.taskfile_id" % refobj)]
        for src, dst in conns:
            if not cmds.isConnected(src, dst):
                cmds.connectAttr(src, dst, force=True)

    def fetch_action_restriction(self, reftrack, action):
        """Return wheter the given action is restricted for the given reftrack

        available actions are:

           ``reference``, ``load``, ``unload``, ``replace``, ``import_reference``, ``import_taskfile``, ``delete``

        If action is not available, True is returned.

        Replace and Delete is always restricted for nested references!

        :param reftrack: the reftrack to query
        :type reftrack: :class:`Reftrack`
        :param action: the action to check.
        :type action: str
        :returns: True, if the action is restricted
        :rtype: :class:`bool`
        :raises: None
        """
        if action == 'import_reference' and reftrack.status() == Reftrack.UNLOADED:
            return True
        if action in ('replace', 'delete', 'import_reference') and reftrack.status() in (Reftrack.LOADED, Reftrack.UNLOADED):
                tracknode = reftrack.get_refobj()
                restricted = cmds.referenceQuery(tracknode, isNodeReferenced=True)
                if restricted:
                    return True
        return super(MayaRefobjInterface, self).fetch_action_restriction(reftrack, action)
