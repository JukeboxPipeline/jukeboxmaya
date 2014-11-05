import abc

from jukeboxcore.plugins import JB_Plugin, JB_StandalonePlugin, JB_StandaloneGuiPlugin, PluginManager
from jukeboxmaya.constants import BUILTIN_PLUGIN_PATH


class JB_MayaPlugin(JB_Plugin):
    """Maya plugin class

    maya plugins are only loaded in maya via the MayaPluginManager.
    If a plugin requires the functionality of maya or any other maya plugin, subclass
    from this one.

    For subclassing: you have to implement **init** and **uninit**!
    """
    pass


class JB_MayaStandalonePlugin(JB_StandalonePlugin):
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


class JB_MayaStandaloneGuiPlugin(JB_StandaloneGuiPlugin):
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

    builtinpluginpath = BUILTIN_PLUGIN_PATH
