"""Implementation of :class:`jukeboxcore.reftrack.ReftypeInterface` for Assets."""
import maya.cmds as cmds

from jukeboxcore.filesys import JB_File
from jukeboxcore.reftrack import ReftypeInterface
from jukeboxmaya import common
from jukeboxmaya import reftrack


class AssetReftypeInterface(ReftypeInterface):
    """Interface for handling the content of released assets in the reference workflow.
    """

    def __init__(self, refobjinter):
        """Initialize a new AssetReftypeInterface that uses the given RefobjInterface

        :param refobjinter: the interface to handle the reftrack nodes
        :type refobjinter: :class:`jukeboxmaya.refobjinter.MayaRefobjInterface`
        :raises: None
        """
        super(AssetReftypeInterface, self).__init__(refobjinter)

    def is_replaceable(self, refobj):
        """Return whether the given reference of the refobject is replaceable or
        if it should just get deleted and loaded again.

        Returns True, because Maya can replace references.

        :param refobj: the refobject to query
        :type refobj: refobj
        :returns: True, if replaceable
        :rtype: bool
        :raises: NotImplementedError
        """
        return True

    def reference(self, refobj, taskfileinfo):
        """Reference the given taskfileinfo into the scene and return the created reference node

        The created reference node will be used on :meth:`RefobjInterface.set_reference` to
        set the reference on a reftrack node.
        Do not call :meth:`RefobjInterface.set_reference` yourself.

        This will also create a group node and group all dagnodes under a appropriate node.

        :param refobj: the reftrack node that will be linked to the reference
        :type refobj: str
        :param taskfileinfo: The taskfileinfo that holds the information for what to reference
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: the reference node that was created and should set on the appropriate reftrack node
        :rtype: str
        :raises: None
        """
        refobjinter = self.get_refobjinter()
        # work in root namespace
        with common.preserve_namespace(":"):
            jbfile = JB_File(taskfileinfo)
            filepath = jbfile.get_fullpath()
            ns_suggestion = reftrack.get_namespace(refobj, refobjinter)
            reffile = cmds.file(filepath, reference=True, namespace=ns_suggestion)
            node = cmds.referenceQuery(reffile, referenceNode=True)  # get reference node
            ns = cmds.referenceQuery(node, namespace=True)  # query the actual new namespace
            content = cmds.namespaceInfo(ns, listOnlyDependencyNodes=True, dagPath=True)  # get the content
            dagcontent = cmds.ls(content, dag=True, ap=True)  # get only the dagnodes so we can group them
            if not dagcontent:
                return node  # no need for a top group if there are not dagnodes to group
            # group the dagnodes
            with common.preserve_namespace(ns):
                grpname = reftrack.get_groupname(refobj, refobjinter)
                grpnode = cmds.createNode(grpname)  # create a group node
                cmds.group(dagcontent, uag=grpnode)  # group the contents
            return node
