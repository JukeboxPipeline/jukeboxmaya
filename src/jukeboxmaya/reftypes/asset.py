"""Implementation of :class:`jukeboxcore.reftrack.ReftypeInterface` for Assets."""
import maya.cmds as cmds

from jukeboxcore.reftrack import ReftypeInterface


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
