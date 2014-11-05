from jukeboxmaya.menu import MenuManager
from jukeboxcore.djadapter import FILETYPES
from jukeboxcore.gui.widgets.releasewin import ReleaseWin
from jukeboxmaya.plugins import JB_MayaStandaloneGuiPlugin
from jukeboxmaya.mayapylauncher import mayapy_launcher


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
        self.mm = MenuManager.get()
        p = self.mm.menus['Jukebox']
        self.menu = self.mm.create_menu("Release", p, command=self.run_external)

    def uninit(self, ):
        """Do nothing on uninit!

        :returns: None
        :rtype: None
        :raises: None
        """
        self.mm.delete_menu(self.menu)

    def run_external(self, *args, **kwargs):
        """Run the Releasewin in another process

        :returns: None
        :rtype: None
        :raises: None
        """
        mayapy_launcher(["launch", "MayaSceneRelease"])

    def run(self, ):
        """Start the configeditor

        :returns: None
        :rtype: None
        :raises: None
        """
        self.rw = ReleaseWin(FILETYPES["mayamainscene"])
        self.rw.show()
