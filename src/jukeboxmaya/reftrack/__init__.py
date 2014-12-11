"""Package for the reference workflow in maya."""


def get_namespace(refobj, refobjinter):
    """Return a suitable name for a namespace for the given reftrack node

    Returns the name of the shot/asset with a "_1" suffix.
    When you create the namespace the number will automatically be incremented by Maya.

    :param refobj: the reftrack node
    :type refobj: str
    :param refobjinter: the refobjinterface for the reftrack node
    :type refobjinter: :class:`jukeboxmaya.reftrack.refobjinter.MayaRefobjInterface`
    :returns: a namespace suggestion
    :rtype: str
    :raises: None
    """
    taskfile = refobjinter.get_taskfile(refobj)
    element = taskfile.task.element
    name = element.name
    return name + "_1"


def get_groupname(refobj, refobjinter):
    """Return a suitable name for a groupname for the given reftrack node

    :param refobj: the reftrack node
    :type refobj: str
    :param refobjinter: the refobjinterface for the reftrack node
    :type refobjinter: :class:`jukeboxmaya.reftrack.refobjinter.MayaRefobjInterface`
    :returns: None
    :rtype: None
    :raises: None
    """
    taskfile = refobjinter.get_taskfile(refobj)
    element = taskfile.task.element
    name = element.name
    return name + "_grp"
