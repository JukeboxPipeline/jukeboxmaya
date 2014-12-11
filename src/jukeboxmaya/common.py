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
