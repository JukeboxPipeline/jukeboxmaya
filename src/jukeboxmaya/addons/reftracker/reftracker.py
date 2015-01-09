from jukeboxcore.gui.widgets.reftrackwin import ReftrackWin
from jukeboxmaya.reftrack.refobjinter import MayaRefobjInterface
from jukeboxmaya.gui.main import maya_main_window
from jukeboxmaya.plugins import JB_MayaPlugin
from jukeboxmaya.menu import MenuManager


class Reftracker(JB_MayaPlugin):
    """A plugin for the reference workflow"""

    author = "David Zuber"
    copyright = "2015"
    version = "0.1"
    description = "Reference workflow for maya."

    def init(self, ):
        """Initialize the plugin. Do nothing.

        This function gets called when the plugin is loaded by the plugin manager.

        :returns:
        :rtype:
        :raises:
        """
        self.win = None
        self.inter = MayaRefobjInterface()

    def uninit(self, ):
        """Uninitialize the plugin. Do nothing

        This function gets called when the plugin is unloaded by the plugin manager.

        :returns:
        :rtype:
        :raises:
        """
        pass

    def init_ui(self, ):
        """Create the menu \"Reftracker\" under \"Jukebox\" to start the plugin and setup the ReftrackWin

        :returns: None
        :rtype: None
        :raises: None
        """
        self.mm = MenuManager.get()
        p = self.mm.menus['Jukebox']
        self.menu = self.mm.create_menu("Reftracker", p, command=self.run)

    def uninit_ui(self):
        """Delete the \"Genesis\" menu

        :returns: None
        :rtype: None
        :raises: None
        """
        self.mm.delete_menu(self.menu)

    def run(self, *args, **kwargs):
        """Start genesis

        :returns: None
        :rtype: None
        :raises: None
        """
        if self.win:
            self.win.deleteLater()
        mayawin = maya_main_window()
        self.win = ReftrackWin(self.inter, parent=mayawin)
        self.win.destroyed.connect(self.win_destroyed)
        self.win.show()
        self.win.wrap_scene()

    def win_destroyed(self, *args, **kwargs):
        """Set the internal reference to the window to None, because the window has been destroyed

        :returns: None
        :rtype: None
        :raises: None
        """
        self.win = None
