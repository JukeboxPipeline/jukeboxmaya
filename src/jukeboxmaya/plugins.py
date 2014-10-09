from jukeboxcore.plugins import JB_Plugin, PluginManager, JB_CorePlugin
from jukeboxmaya.constants import BUILTIN_PLUGIN_PATH


class JB_MayaPlugin(JB_Plugin):
    """Maya plugin class

    maya plugins are only loaded in maya via the MayaPluginManager.
    If a plugin requires the functionality of maya or any other maya plugin, subclass
    from this one.

    For subclassing: you have to implement **init** and **uninit**!
    """
    pass


class MayaPluginManager(PluginManager):
    """ A plugin manager that supports JB_CorePlugins and JB_MayaPlugins """

    supportedTypes = (JB_CorePlugin, JB_MayaPlugin)

    builtinpluginpath = BUILTIN_PLUGIN_PATH
