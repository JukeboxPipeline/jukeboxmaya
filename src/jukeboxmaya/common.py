"""Module for common maya actions"""
from contextlib import contextmanager

import maya.cmds as cmds


@contextmanager
def use_root_ns():
    """Contextmanager that will set the namespace on root and on exit restore the current namespace

    :returns: None
    :rtype: None
    :raises: None
    """
    ns = cmds.namespaceInfo(an=True)
    try:
        cmds.namespace(set=":")
        yield
    finally:
        cmds.namespace(set=ns)


@contextmanager
def preserve_namespace():
    """Contextmanager that will restore the current namespace

    :returns: None
    :rtype: None
    :raises: None
    """
    ns = cmds.namespaceInfo(an=True)
    try:
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
