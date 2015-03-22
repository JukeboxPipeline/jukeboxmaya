from jukeboxmaya.plugins import JB_MayaPlugin, MayaPluginManager
from jukeboxmaya.menu import MenuManager
from jukeboxmaya.gui.main import maya_main_window


class MayaMGMT(JB_MayaPlugin):
    """A maya plugin for the guerillamanagement tool.

    This will create a menu entry \"Projectmanagement\" under \"Jukebox\"!
    With this menu entry you can start the Plugin.
    """

    required = ('GuerillaMGMT',)

    author = "David Zuber"
    copyright = "2014"
    version = "0.1"
    description = "A tool for project management"

    def init(self, ):
        """Initialize the plugin. Do nothing.

        This function gets called when the plugin is loaded by the plugin manager.

        :returns:
        :rtype:
        :raises:
        """
        pass

    def uninit(self, ):
        """Uninitialize the plugin. Do nothing

        This function gets called when the plugin is unloaded by the plugin manager.

        :returns:
        :rtype:
        :raises:
        """
        pass

    def init_ui(self, ):
        """Create the menu \"Projectmanagement\" under \"Jukebox\" to start the plugin

        :returns: None
        :rtype: None
        :raises: None
        """
        self.mm = MenuManager.get()
        p = self.mm.menus['Jukebox']
        self.menu = self.mm.create_menu("Projectmanagement", p, command=self.run)

    def uninit_ui(self, ):
        """Delete the \"Projectmanagement\" menu

        :returns: None
        :rtype: None
        :raises: None
        """
        self.mm.delete_menu(self.menu)

    def run(self, *args, **kwargs):
        """Start the tool

        :returns: None
        :rtype: None
        :raises: None
        """
        pm = MayaPluginManager.get()
        guerilla =  pm.get_plugin("GuerillaMGMT")
        mayawin = maya_main_window()
        guerilla.run(parent=mayawin)
