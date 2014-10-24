import maya.OpenMayaUI as apiUI

from jukeboxcore.gui.main import wrap


def wrap_maya_ui(mayaname):
    """    Given the name of a Maya UI element of any type,
    return the corresponding QWidget or QAction.
    If the object does not exist, returns None

    :param mayaname: the maya ui element
    :type mayaname: str
    :returns: the wraped object
    :rtype: QObject | None
    :raises: None
    """
    ptr = apiUI.MQtUtil.findControl(mayaname)
    if ptr is None:
        ptr = apiUI.MQtUtil.findLayout(mayaname)
    if ptr is None:
        ptr = apiUI.MQtUtil.findMenuItem(mayaname)
    if ptr is not None:
        return wrap(long(ptr))
