from PySide import QtGui

from jukeboxmaya.menu import MenuManager
from jukeboxcore.djadapter import FILETYPES
from jukeboxcore.action import ActionUnit, ActionCollection
from jukeboxcore.release import ReleaseActions
from jukeboxcore.gui.widgets.releasewin import ReleaseWin
from jukeboxmaya.plugins import JB_MayaStandaloneGuiPlugin
from jukeboxmaya.mayapylauncher import mayapy_launcher
from jukeboxmaya.commands import open_scene, save_scene, import_all_references, update_scenenode
from jukeboxmaya.gui.main import maya_main_window


class OptionWidget(QtGui.QWidget):
    """A option widget for the release window.

    The user can specify if he wants to import all references.
    """

    def __init__(self, parent=None, f=0):
        """

        :param parent:
        :type parent:
        :param f:
        :type f:
        :raises: None
        """
        super(OptionWidget, self).__init__(parent, f)
        self.setup_ui()

    def setup_ui(self, ):
        """Create all ui elements and layouts

        :returns: None
        :rtype: None
        :raises: None
        """
        self.main_vbox = QtGui.QVBoxLayout(self)
        self.import_all_references_cb = QtGui.QCheckBox("Import references")
        self.main_vbox.addWidget(self.import_all_references_cb)

    def import_references(self, ):
        """Return wheter the user specified, that he wants to import references

        :returns: True, if references should be imported
        :rtype: bool
        :raises: None
        """
        return self.import_all_references_cb.isChecked()


class SceneReleaseActions(ReleaseActions):
    """Release actions for releasing a scene

    Uses the :class:`OptionWidget` for user options.
    """

    def __init__(self, ):
        """

        :raises: None
        """
        super(SceneReleaseActions, self).__init__()
        self._option_widget = OptionWidget()

    def get_checks(self, ):
        """Get the sanity check actions for a releaes depending on the selected options

        :returns: the cleanup actions
        :rtype: :class:`jukeboxcore.action.ActionCollection`
        :raises: None
        """
        return ActionCollection([])

    def get_cleanups(self, ):
        """Get the cleanup actions for a releaes depending on the selected options

        :returns: the cleanup actions
        :rtype: :class:`jukeboxcore.action.ActionCollection`
        :raises: None
        """
        cleanups = []
        open_unit = ActionUnit(name="Open",
                               description="Open the maya scene.",
                               actionfunc=open_scene)
        cleanups.append(open_unit)
        if self._option_widget.import_references():
            import_unit = ActionUnit(name="Import references",
                                     description="Import all references in the scene.",
                                     actionfunc=import_all_references,
                                     depsuccess=[open_unit])
            cleanups.append(import_unit)
        update_scenenode_unit = ActionUnit(name="Update Scene Node",
                                           description="Change the id from the jbscene node from work to releasefile.",
                                           actionfunc=update_scenenode,
                                           depsuccess=[open_unit])
        cleanups.append(update_scenenode_unit)
        save_unit = ActionUnit(name="Save",
                               description="Save the scene.",
                               actionfunc=save_scene,
                               depsuccess=[update_scenenode_unit])
        cleanups.append(save_unit)
        return ActionCollection(cleanups)

    def option_widget(self, ):
        """Return the option widget of this instance

        :returns: the option widget
        :rtype: :class:`OptionWidget`
        :raises: None
        """
        return self._option_widget


class MayaSceneRelease(JB_MayaStandaloneGuiPlugin):
    """A plugin that can release a maya scene

    This can be used as a standalone plugin.
    """

    author = "David Zuber"
    copyright = "2014"
    version = "0.1"
    description = "Release Maya scenes"

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
        """Create the menu Release under Jukebox menu.

        :returns: None
        :rtype: None
        :raises: None
        """
        self.mm = MenuManager.get()
        p = self.mm.menus['Jukebox']
        self.menu = self.mm.create_menu("Release", p, command=self.run_external)

    def uninit_ui(self, ):
        """Delete the Release menu

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
        mayapy_launcher(["launch", "MayaSceneRelease"], wait=False)

    def run(self, ):
        """Start the configeditor

        :returns: None
        :rtype: None
        :raises: None
        """
        ra = SceneReleaseActions()
        mayawin = maya_main_window()
        self.rw = ReleaseWin(FILETYPES["mayamainscene"], parent=mayawin)
        self.rw.set_release_actions(ra)
        self.rw.show()
