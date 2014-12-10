"""Implementation of :class:`jukeboxcore.reftrack.ReftypeInterface` for Assets."""
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

