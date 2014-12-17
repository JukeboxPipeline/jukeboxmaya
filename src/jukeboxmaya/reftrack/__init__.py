"""Package for the reference workflow in maya."""
import maya.cmds as cmds

from jukeboxmaya import common


def get_namespace(taskfileinfo):
    """Return a suitable name for a namespace for the taskfileinfo

    Returns the name of the shot/asset with a "_1" suffix.
    When you create the namespace the number will automatically be incremented by Maya.

    :param taskfileinfo: the taskfile info for the file that needs a namespace
    :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
    :returns: a namespace suggestion
    :rtype: str
    :raises: None
    """
    element = taskfileinfo.task.element
    name = element.name
    return name + "_1"


def get_groupname(taskfileinfo):
    """Return a suitable name for a groupname for the given taskfileinfo.

    :param taskfileinfo: the taskfile info for the file that needs a group when importing/referencing
    :type taskfileinfo: :class:`jukeboxcore.filesys.TaskFileInfo`
    :returns: None
    :rtype: None
    :raises: None
    """
    element = taskfileinfo.task.element
    name = element.name
    return name + "_grp"


def group_content(content, namespace, grpname, grpnodetype):
    """Group the given content in the given namespace under a node of type
    grpnodetype with the name grpname

    :param content: the nodes to group
    :type content: :class:`list`
    :param namespace: the namespace to use
    :type namespace: str | None
    :param grpname: the name of the new grpnode
    :type grpname: str
    :param grpnodetype: the nodetype for the grpnode
    :type grpnodetype: str
    :returns: the created group node
    :rtype: str
    :raises: None
    """
    with common.preserve_namespace(namespace):
        grpnode = cmds.createNode(grpnodetype, name=grpname) # create grp node
        cmds.group(content, uag=grpnode) # group content
    return grpnode
