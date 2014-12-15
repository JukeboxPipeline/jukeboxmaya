"""Package for the reference workflow in maya."""


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
