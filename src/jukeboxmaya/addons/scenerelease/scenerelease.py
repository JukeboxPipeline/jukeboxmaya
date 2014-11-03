from jukeboxcore.djadapter import FILETYPES
from jukeboxmaya.plugins import JB_MayaStandaloneGuiPlugin
from jukeboxcore.gui.widgets.releasewin import ReleaseWin


class MayaSceneRelease(JB_MayaStandaloneGuiPlugin):
    """A plugin that can release a maya scene

    This can be used as a standalone plugin.
    """

    author = "David Zuber"
    copyright = "2014"
    version = "0.1"
    description = "Release Maya scenes"

    def init(self, ):
        """Do nothing on init! Call run() if you want to start the configeditor

        :returns: None
        :rtype: None
        :raises: None
        """
        pass

    def uninit(self, ):
        """Do nothing on uninit!

        :returns: None
        :rtype: None
        :raises: None
        """
        pass

    def run(self, ):
        """Start the configeditor

        :returns: None
        :rtype: None
        :raises: None
        """
        self.rw = ReleaseWin(FILETYPES["mayamainscene"])
        self.rw.show()
