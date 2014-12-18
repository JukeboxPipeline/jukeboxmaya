"""Module for common maya actions"""
from contextlib import contextmanager

import maya.cmds as cmds


@contextmanager
def preserve_namespace(newns=None):
    """Contextmanager that will restore the current namespace

    :param newns: a name of namespace that should be set in the beginning. the original namespace will be restored afterwards.
                  If None, does not set a namespace.
    :type newns: str | None
    :returns: None
    :rtype: None
    :raises: None
    """
    ns = cmds.namespaceInfo(an=True)
    try:
        cmds.namespace(set=newns)
        yield
    finally:
        cmds.namespace(set=ns)


@contextmanager
def preserve_selection():
    """Contextmanager that will restore the current selection

    :returns: None
    :rtype: None
    :raises: None
    """
    sl = cmds.ls(sl=True)
    try:
        yield
    finally:
        cmds.select(sl, replace=True)


def get_top_namespace(node):
    """Return the top namespace of the given node

    If the node has not namespace (only root), ":" is returned.
    Else the top namespace (after root) is returned

    :param node: the node to query
    :type node: str
    :returns: The top level namespace.
    :rtype: str
    :raises: None
    """
    name = node.rsplit("|", 1)[-1]  # get the node name, in case we get a dagpath
    name = name.lstrip(":")  # strip the root namespace
    if ":" not in name:  # if there is no namespace return root
        return ":"
    else:
        # get the top namespace
        return name.partition(":")[0]


def disconnect_node(node):
    """Disconnect all connections from node

    :param node: the node to disconnect
    :type node: str
    :returns: None
    :rtype: None
    :raises: None
    """
    destconns = cmds.listConnections(node, connections=True, plugs=True, source=False) or []
    srcconns = cmds.listConnections(node, connections=True, plugs=True, destination=False) or []
    for i in range(0, len(destconns), 2):
        source, dest = destconns[i], destconns[i+1]
        cmds.disconnectAttr(source, dest)
    for i in range(0, len(srcconns), 2):
        source, dest = srcconns[i+1], srcconns[i]
        cmds.disconnectAttr(source, dest)
