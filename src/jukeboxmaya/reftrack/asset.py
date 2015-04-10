"""Implementation of :class:`jukeboxcore.reftrack.ReftypeInterface` for Assets."""
from collections import defaultdict
from functools import partial

import maya.cmds as cmds

from jukeboxcore import djadapter
from jukeboxcore.filesys import JB_File
from jukeboxcore.reftrack import ReftypeInterface, ReftrackAction
from jukeboxcore.filesys import TaskFileInfo
from jukeboxcore.gui import djitemdata
from jukeboxcore.gui.main import get_icon
from jukeboxcore.gui.treemodel import TreeModel, TreeItem, ListItemData
from jukeboxcore.gui.filesysitemdata import TaskFileInfoItemData
from jukeboxmaya import common
from jukeboxmaya import reftrack


def select_dp_nodes(reftrack):
    """Select all dag nodes of the given reftrack

    :param reftrack: The reftrack to select the dagnodes for
    :type reftrack: :class:`jukeboxcore.reftrack.Reftrack`
    :returns: None
    :rtype: None
    :raises: None
    """
    refobj = reftrack.get_refobj()
    if not refobj:
        return
    parentns = common.get_namespace(refobj)
    ns = cmds.getAttr("%s.namespace" % refobj)
    fullns = ":".join((parentns.rstrip(":"), ns.lstrip(":")))
    c = cmds.namespaceInfo(fullns, listOnlyDependencyNodes=True, dagPath=True, recurse=True)
    cmds.select(c, replace=True)


def select_dag_nodes(reftrack):
    """Select all dag nodes of the given reftrack

    :param reftrack: The reftrack to select the dagnodes for
    :type reftrack: :class:`jukeboxcore.reftrack.Reftrack`
    :returns: None
    :rtype: None
    :raises: None
    """
    refobj = reftrack.get_refobj()
    if not refobj:
        return
    parentns = common.get_namespace(refobj)
    ns = cmds.getAttr("%s.namespace" % refobj)
    fullns = ":".join((parentns.rstrip(":"), ns.lstrip(":")))
    c = cmds.namespaceInfo(fullns, listOnlyDependencyNodes=True, dagPath=True, recurse=True)
    dag = cmds.ls(c, dag=True, ap=True)
    cmds.select(dag, replace=True)


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

    def get_scenenode(self, nodes):
        """Get the scenenode in the given nodes

        There should only be one scenenode in nodes!

        :param nodes:
        :type nodes:
        :returns: None
        :rtype: None
        :raises: AssertionError
        """
        scenenodes = cmds.ls(nodes, type='jb_sceneNode')
        assert scenenodes, "Found no scene nodes!"
        return sorted(scenenodes)[0]

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
        # work in root namespace
        with common.preserve_namespace(":"):
            jbfile = JB_File(taskfileinfo)
            filepath = jbfile.get_fullpath()
            ns_suggestion = reftrack.get_namespace(taskfileinfo)
            newnodes = cmds.file(filepath, reference=True, namespace=ns_suggestion, returnNewNodes=True)
            # You could also use the filename returned by the file command to query the reference node.
            # Atm there is a but, that if you import the file before, the command fails.
            # So we get all new reference nodes and query the one that is not referenced
            for refnode in cmds.ls(newnodes, type='reference'):
                if not cmds.referenceQuery(refnode, isNodeReferenced=True):
                    node = refnode
                    break
            ns = cmds.referenceQuery(node, namespace=True)  # query the actual new namespace
            content = cmds.namespaceInfo(ns, listOnlyDependencyNodes=True, dagPath=True)  # get the content
            # connect reftrack with scenenode
            scenenode = self.get_scenenode(content)
            self.get_refobjinter().connect_reftrack_scenenode(refobj, scenenode)
            reccontent = cmds.namespaceInfo(ns, listOnlyDependencyNodes=True, dagPath=True, recurse=True)  # get the content + content of children
            dagcontent = cmds.ls(reccontent, ap=True, assemblies=True)  # get only the top level dagnodes so we can group them
            if not dagcontent:
                return node  # no need for a top group if there are not dagnodes to group
            # group the dagnodes
            grpname = reftrack.get_groupname(taskfileinfo)
            reftrack.group_content(dagcontent, ns, grpname, "jb_asset")
            return node

    def load(self, refobj, reference):
        """Load the given reference

        Load in this case means, that a reference is already in the scene
        but it is not in a loaded state.
        Loading the reference means, that the actual data will be read.

        :param refobj: the reftrack node that is linked to the reference
        :type refobj: str
        :param reference: the reference node
        :type refobj: str
        :returns: None
        :rtype: None
        :raises: None
        """
        cmds.file(loadReference=reference)

    def unload(self, refobj, reference):
        """Unload the given reference

        Unload in this case means, that a reference is stays in the scene
        but it is not in a loaded state.
        So there is a reference, but data is not read from it.

        :param refobj: the refobj that is linked to the reference
        :param reference: the reference object. E.g. in Maya a reference node
        :returns: None
        :rtype: None
        :raises: None
        """
        cmds.file(unloadReference=reference)

    def replace(self, refobj, reference, taskfileinfo):
        """Replace the given reference with the given taskfileinfo

        :param refobj: the refobj that is linked to the reference
        :param reference: the reference object. E.g. in Maya a reference node
        :param taskfileinfo: the taskfileinfo that will replace the old entity
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: None
        """
        jbfile = JB_File(taskfileinfo)
        filepath = jbfile.get_fullpath()
        cmds.file(filepath, loadReference=reference)
        ns = cmds.referenceQuery(reference, namespace=True)  # query the actual new namespace
        content = cmds.namespaceInfo(ns, listOnlyDependencyNodes=True, dagPath=True)  # get the content
        scenenode = self.get_scenenode(content) # get the scene node
        self.get_refobjinter().connect_reftrack_scenenode(refobj, scenenode)

    def delete(self, refobj):
        """Delete the content of the given refobj

        :param refobj: the refobj that represents the content that should be deleted
        :type refobj: refobj
        :returns: None
        :rtype: None
        :raises: None
        """
        refobjinter = self.get_refobjinter()
        reference = refobjinter.get_reference(refobj)
        if reference:
            fullns = cmds.referenceQuery(reference, namespace=True)
            cmds.file(removeReference=True, referenceNode=reference)
        else:
            parentns = common.get_namespace(refobj)
            ns = cmds.getAttr("%s.namespace" % refobj)
            fullns = ":".join((parentns.rstrip(":"), ns.lstrip(":")))
        cmds.namespace(removeNamespace=fullns, deleteNamespaceContent=True)

    def import_reference(self, refobj, reference):
        """Import the given reference

        The reference of the refobj will be set to None automatically afterwards with
        :meth:`RefobjInterface.set_reference`

        :param refobj: the refobj that is linked to the reference
        :param reference: the reference object. E.g. in Maya a reference node
        :returns: None
        :rtype: None
        :raises: None
        """
        cmds.file(importReference=True, referenceNode=reference)

    def import_taskfile(self, refobj, taskfileinfo):
        """Import the given taskfileinfo and update the refobj

        :param refobj: the refobject
        :type refobj: refobject
        :param taskfileinfo: the taskfileinfo to reference
        :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: None
        """
        # work in root namespace
        with common.preserve_namespace(":"):
            jbfile = JB_File(taskfileinfo)
            filepath = jbfile.get_fullpath()
            ns_suggestion = reftrack.get_namespace(taskfileinfo)
            nodes = cmds.file(filepath, i=True, namespace=ns_suggestion, returnNewNodes=True, preserveReferences=True)  # import
            assert nodes, 'Nothing was imported! this is unusual!'
            ns = common.get_top_namespace(nodes[0])  # get the actual namespace
            cmds.setAttr("%s.namespace" % refobj, ns, type="string")
            nscontent = cmds.namespaceInfo(ns, listOnlyDependencyNodes=True, dagPath=True)  # get the content
            scenenode = self.get_scenenode(nscontent)
            self.get_refobjinter().connect_reftrack_scenenode(refobj, scenenode)
            dagcontent = cmds.ls(nodes, ap=True, assemblies=True)  # get only the dagnodes so we can group them
            if not dagcontent:
                return  # no need for a top group if there are not dagnodes to group
            # group the dagnodes in the new namespace
            grpname = reftrack.get_groupname(taskfileinfo)
            reftrack.group_content(dagcontent, ns, grpname, "jb_asset")
            return

    def fetch_option_taskfileinfos(self, element):
        """Fetch the options for possible files to load, replace etc for the given element.

        Options from which to choose a file to load or replace.

        :param element: The element for which the options should be fetched.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: The options
        :rtype: list of :class:`TaskFileInfo`
        :raises: None
        """
        tfs = []
        for task in element.tasks.all():
            taskfiles = list(task.taskfile_set.filter(releasetype=djadapter.RELEASETYPES['release'],
                                                      typ=djadapter.FILETYPES['mayamainscene']))
            tfs.extend(taskfiles)
        tfis = [TaskFileInfo.create_from_taskfile(tf) for tf in tfs]
        return tfis

    def create_options_model(self, taskfileinfos):
        """Create a new treemodel that has the taskfileinfos as internal_data of the leaves.

        I recommend using :class:`jukeboxcore.gui.filesysitemdata.TaskFileInfoItemData` for the leaves.
        So a valid root item would be something like::

          rootdata = jukeboxcore.gui.treemodel.ListItemData(["Asset/Shot", "Task", "Descriptor", "Version", "Releasetype"])
          rootitem = jukeboxcore.gui.treemodel.TreeItem(rootdata)

        :returns: the option model with :class:`TaskFileInfo` as internal_data of the leaves.
        :rtype: :class:`jukeboxcore.gui.treemodel.TreeModel`
        :raises: None
        """
        rootdata = ListItemData(["Asset/Shot", "Task", "Descriptor", "Version", "Releasetype"])
        rootitem = TreeItem(rootdata)
        tasks = defaultdict(list)
        for tfi in taskfileinfos:
            tasks[tfi.task].append(tfi)
        for task, tfis in tasks.iteritems():
            taskdata = djitemdata.TaskItemData(task)
            taskitem = TreeItem(taskdata, rootitem)
            for tfi in tfis:
                tfidata = TaskFileInfoItemData(tfi)
                TreeItem(tfidata, taskitem)
        return TreeModel(rootitem)

    def get_option_labels(self, element):
        """Return labels for each level of the option model.

        The options returned by :meth:`RefobjInterface.fetch_options` is a treemodel
        with ``n`` levels. Each level should get a label to describe what is displays.

        Assets are organized in tasks and versions.

        :param element: The element for which the options should be fetched.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: label strings for all levels
        :rtype: list
        :raises: None
        """
        return ["Task", "Version"]

    def get_option_columns(self, element):
        """Return the column of the model to show for each level

        Because each level might be displayed in a combobox. So you might want to provide the column
        to show.

        :param element: The element for wich the options should be fetched.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: a list of columns
        :rtype: list
        :raises: None
        """
        return [0, 3]

    def get_suggestions(self, reftrack):
        """Return a list with possible children for this reftrack

        Each Reftrack may want different children. E.g. a Asset wants
        to suggest a shader for itself and all assets that are linked in
        to it in the database. Suggestions only apply for enities with status
        other than None.

        A suggestion is a tuple of typ and element. It will be used to create a newlen
        :class:`Reftrack`. The parent will be this instance, root and interface will
        of course be the same.

        This will delegate the call to the  appropriate :class:`ReftypeInterface`.
        So suggestions may vary for every typ and might depend on the
        status of the reftrack.

        :param reftrack: the reftrack which needs suggestions
        :type reftrack: :class:`Reftrack`
        :returns: list of suggestions, tuples of type and element.
        :rtype: list
        :raises: None
        """
        return []

    def get_scene_suggestions(self, current):
        """Return a list with elements for reftracks for the current scene with this type.

        For every element returned, the reftrack system will create a :class:`Reftrack` with the type
        of this interface, if it is not already in the scene.

        E.g. if you have a type that references whole scenes, you might suggest all
        linked assets for shots, and all liked assets plus the current element itself for assets.
        If you have a type like shader, that usually need a parent, you would return an empty list.
        Cameras might only make sense for shots and not for assets etc.

        Do not confuse this with :meth:`ReftypeInterface.get_suggestions`. It will gather suggestions
        for children of a :class:`Reftrack`.

        The standard implementation only returns an empty list!

        :param reftrack: the reftrack which needs suggestions
        :type reftrack: :class:`Reftrack`
        :returns: list of suggestions, tuples of type and element.
        :rtype: list
        :raises: None
        """
        l = []
        if isinstance(current, djadapter.models.Asset):
            l.append(current)
        l.extend(list(current.assets.all()))
        return l

    def is_available_for_scene(self, element):
        """Return True, if it should be possible to add a new reftrack with the given
        element and the type of the interface to the scene.

        Some types might only make sense for a shot or asset. Others should never be available, because
        you would only use them as children of other reftracks (e.g. a shader).

        :param element: the element that could be used in conjuction with the returned types to create new reftracks.
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :returns: True, if available
        :rtype: :class:`bool`
        :raises: None
        """
        return True

    def get_typ_icon(self, ):
        """Return a icon that should be used to identify the type in an UI

        :returns: a icon for this type
        :rtype: :class:`QtGui.QIcon` | None
        :raises: None
        """
        return get_icon("asset.png", asicon=True)

    def get_additional_actions(self, reftrack):
        """Return a list of additional actions you want to provide for the menu
        of the reftrack.

        E.e. you want to have a menu entry, that will select the entity in your programm.

        :param reftrack: the reftrack to return the actions for
        :type reftrack: :class:`Reftrack`
        :returns: A list of :class:`ReftrackAction`
        :rtype: list
        :raises: None
        """
        refobj = reftrack.get_refobj()
        select_dp_action = ReftrackAction("Select Nodes", partial(select_dp_nodes, reftrack=reftrack), enabled=bool(refobj))
        select_dag_action = ReftrackAction("Select DAG", partial(select_dag_nodes, reftrack=reftrack), enabled=bool(refobj))
        return [select_dp_action, select_dag_action]
