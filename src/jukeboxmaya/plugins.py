import abc

from jukeboxcore.log import get_logger
log = get_logger(__name__)

import jukeboxmaya
from jukeboxcore.plugins import JB_Plugin, JB_StandalonePlugin, JB_StandaloneGuiPlugin, PluginManager
from jukeboxmaya.constants import BUILTIN_PLUGIN_PATH


class JB_MayaPlugin(JB_Plugin):
    """Maya plugin class

    maya plugins are only loaded in maya via the MayaPluginManager.
    If a plugin requires the functionality of maya or any other maya plugin, subclass
    from this one.

    For subclassing: you have to implement **init** and **uninit**!
    """

    def _load(self, ):
        """Loads the plugin

        :raises: errors.PluginInitError
        """
        super(JB_MayaPlugin, self)._load()
        try:
            if not jukeboxmaya.STANDALONE_INITIALIZED:
                self.init_ui()
        except Exception:
            log.exception("Load Ui failed!")

    def _unload(self, ):
        """Unloads the plugin

        :raises: errors.PluginUninitError
        """
        super(JB_MayaPlugin, self)._unload()
        try:
            if not jukeboxmaya.STANDALONE_INITIALIZED:
                self.uninit_ui()
        except Exception:
            log.exception("Unload Ui failed!")

    @abc.abstractmethod
    def init_ui(self, ):
        """Initialize the plugin in the maya ui (e.g. create a menu or put something in a toolbar/shelf).

        :returns: None
        :rtype: None
        :raises: None
        """
        pass

    @abc.abstractmethod
    def uninit_ui(self, ):
        """Uninitialize the ui in the maya ui (e.g. delete the menus/shelfes etc).

        :returns: None
        :rtype: None
        :raises: None
        """
        pass


class JB_MayaStandalonePlugin(JB_StandalonePlugin, JB_MayaPlugin):
    """Maya plugin for standalone addons.

    Standalone addons feature a special run method an
    can be run with the jukebox launcher.
    The launcher will first initialize maya standalone, then the plugin and then
    call the run method.

    For subclassing: you have to implement **init**, **unit** and **run**!
    """

    @abc.abstractmethod
    def run(self, ):
        """Start the plugin. This method is also called by
        the jukebox launcher.

        :returns: None
        :rtype: None
        :raises: None
        """
        pass


class JB_MayaStandaloneGuiPlugin(JB_StandaloneGuiPlugin, JB_MayaPlugin):
    """Maya plugin for standalone addons that also need a gui.

    Standalone addons feature a special run method an
    can be run with the jukebox launcher.
    The launcher will first initialize maya standalone, then the plugin and then
    call the run method.

    For subclassing: you have to implement **init**, **unit** and **run**!
    """
    pass


class MayaPluginManager(PluginManager):
    """ A plugin manager that supports JB_CorePlugins and JB_MayaPlugins """

    supportedTypes = PluginManager.supportedTypes
    supportedTypes.append(JB_MayaPlugin)
    supportedTypes.append(JB_MayaStandalonePlugin)
    supportedTypes.append(JB_MayaStandaloneGuiPlugin)
