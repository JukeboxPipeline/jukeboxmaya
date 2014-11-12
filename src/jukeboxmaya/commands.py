"""Wrappers around common maya commands.
These functions are inteded to be used in :class:`jukeboxcore.actions.ActionUnit`.
"""
import maya.cmds as cmds

from jukeboxcore.action import ActionStatus


def open_scene(f, kwargs=None):
    """Opens the given JB_File

    :param f: the file to open
    :type f: :class:`jukeboxcore.filesys.JB_File`
    :param kwargs: keyword arguments for the command maya.cmds file.
                   defaultflags that are always used:

                     :open: ``True``

                   e.g. to force the open command use ``{'force'=True}``.
    :type kwargs: dict|None
    :returns: An action status. The returnvalue of the actionstatus is the opened mayafile
    :rtype: :class:`ActionStatus`
    :raises: None
    """
    defaultkwargs = {'open':True}
    if kwargs is None:
        kwargs = {}
    kwargs.update(defaultkwargs)
    fp = f.get_fullpath()
    mayafile = cmds.file(fp, **kwargs)
    msg = "Successfully opened file %s with arguments: %s" % (fp, kwargs)
    return ActionStatus(ActionStatus.SUCCESS, msg, returnvalue=mayafile)


def save_scene(f, kwargs=None):
    """Save the current scene to the given JB_File

    .. Note:: This will rename the currently open scene.
              So if you save again afterwards, you will save to the location of
              the given JB_File. No files are renamed. This just uses::

                cmds.file(rename=f.get_fullpath())

    :param f: the file to save the current scene to
    :type f: :class:`jukeboxcore.filesys.JB_File`
    :param kwargs: keyword arguments for the command maya.cmds file.
                   defaultflags that are always used:

                     :save: ``True``

                   e.g. to force the save command use ``{'force'=True}``.
    :type kwargs: dict|None
    :returns: An action status. The returnvalue of the actionstatus is the saved mayafile
    :rtype: :class:`ActionStatus`
    :raises: None
    """
    defaultkwargs = {'save':True}
    if kwargs is None:
        kwargs = {}
    kwargs.update(defaultkwargs)
    fp = f.get_fullpath()
    cmds.file(rename=fp)
    mayafile = cmds.file(**kwargs)
    msg = "Successfully saved file %s with arguments: %s" % (fp, kwargs)
    return ActionStatus(ActionStatus.SUCCESS, msg, returnvalue=mayafile)


def import_all_references(arg, kwargs=None):
    """Import all references in the currently open scene

    :param arg: this argument is ignored. But thisway you can use this function in an ActionUnit more easily.
    :param kwargs: keyword arguments for the command maya.cmds file.
                   defaultflags that are always used:

                     :importReferences: ``True``

    :type kwargs: dict|None
    :returns: An action status. The returnvalue of the actionstatus are the imported references.
    :rtype: :class:`ActionStatus`
    :raises: None
    """
    defaultkwargs = {'importReferences':True}
    if kwargs is None:
        kwargs = {}
    kwargs.update(defaultkwargs)
    # list all reference files
    refs = cmds.ls(type='reference')
    imported = []
    # for each reference node, query the filename and import it.
    # Note: the filename may contain copy numbers, e.g. {1} if a file is referenced
    # multiple times.
    for i in refs:
        rFile = cmds.referenceQuery(i, f=True)
        imported.append(cmds.file(rFile, **kwargs))
    msg = "Successfully imported reference %s with arguments: %s" % (imported, kwargs)
    return ActionStatus(ActionStatus.SUCCESS, msg, returnvalue=imported)
