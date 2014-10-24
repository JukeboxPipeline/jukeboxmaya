import os

import maya.cmds as cmds
try:
    import shiboken
except ImportError:
    from PySide import shiboken

from jukeboxcore.log import get_logger
log = get_logger(__name__)

from jukeboxcore import djadapter
from jukeboxmaya.menu import MenuManager
from jukeboxmaya.mayaplugins import jbscene
from jukeboxmaya.plugins import JB_MayaPlugin, MayaPluginManager


class MayaGenesis(JB_MayaPlugin):
    """A maya plugin for saving and opening shots and assets.

    This will create a menu entry \"Genesis\" under \"Jukebox\".
    You can start the plugin with that menu entry.
    """

    required = ('Genesis',)

    author = "David Zuber"
    copyright = "2014"
    version =  "0.1"
    description = "A tool for saving and opening shots and assets."

    def init(self, ):
        """Create the menu \"Genesis\" under \"Jukebox\" to start the plugin and setup the GenesisWin

        :returns: None
        :rtype: None
        :raises: None
        """
        self.gw = None
        pm = MayaPluginManager.get()
        genesis =  pm.get_plugin("Genesis")
        self.GenesisWin = self.subclass_genesis(genesis.GenesisWin)

        self.mm = MenuManager.get()
        p = self.mm.menus['Jukebox']
        self.menu = self.mm.create_menu("Genesis", p, command=self.run)

    def uninit(self):
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
        if self.gw and shiboken.isValid(self.gw):
            self.gw.deleteLater()
        self.gw = self.GenesisWin()
        self.gw.show()

    def subclass_genesis(self, genesisclass):
        """Subclass the given genesis class and implement all abstract methods

        :param genesisclass: the GenesisWin class to subclass
        :type genesisclass: :class:`GenesisWin`
        :returns: the subclass
        :rtype: subclass of :class:`GenesisWin`
        :raises: None
        """
        class MayaGenesisWin(genesisclass):
            """Implementation of Genesis for maya
            """

            def open_shot(self, taskfile):
                """Open the given taskfile

                :param taskfile: the taskfile for the shot
                :type taskfile: :class:`djadapter.models.TaskFile`
                :returns: True if opening was successful
                :rtype: bool
                :raises: none
                """
                return self.open_file(taskfile)

            def save_shot(self, jbfile, tf):
                """Save the shot to the location of jbfile

                :param jbfile: the jbfile that can be used to query the location
                :type jbfile: :class:`jukebox.core.filesys.JB_File`
                :param tf: the taskfile that is saved
                :type tf: :class:`djadapter.models.TaskFile`
                :returns: None
                :rtype: None
                :raises: None
                """
                self.update_scene_node(tf)
                self.save_file(jbfile)

            def open_asset(self, taskfile):
                """Open the given taskfile

                :param taskfile: the taskfile for the asset
                :type taskfile: :class:`djadapter.models.TaskFile`
                :returns: True if opening was successful
                :rtype: bool
                :raises: None
                """
                return self.open_file(taskfile)

            def save_asset(self, jbfile, tf):
                """Save the asset to the location of jbfile

                :param jbfile: the jbfile that can be used to query the location
                :type jbfile: :class:`jukebox.core.filesys.JB_File`
                :param tf: the taskfile that is saved
                :type tf: :class:`djadapter.models.TaskFile`
                :returns: None
                :rtype: None
                :raises: NotImplementedError
                """
                self.update_scene_node(tf)
                self.save_file(jbfile)

            def save_file(self, jbfile):
                """Physically save current scene to jbfile\'s location

                :param jbfile: the jbfile that can be used to query the location
                :type jbfile: :class:`jukebox.core.filesys.JB_File`
                :returns: None
                :rtype: None
                :raises: None
                """
                p = jbfile.get_fullpath()
                p = os.path.expanduser(p)
                typ = 'mayaBinary'
                if jbfile.get_ext() == 'ma':
                    typ = 'mayaAscii'
                cmds.file(rename = p)
                cmds.file(save=True, defaultExtensions=False, type=typ)

            def open_file(self, taskfile):
                """Open the given jbfile in maya

                :param taskfile: the taskfile for the asset
                :type taskfile: :class:`djadapter.models.TaskFile`
                :returns: True if opening was successful
                :rtype: bool
                :raises: None
                """
                r = self.check_modified()
                if r is False:
                    return False
                cmds.file(taskfile.path, open=True, force=True)
                return True

            def get_current_file(self, ):
                """Return the taskfile that is currently open or None if no taskfile is open

                :returns: the open taskfile or None if no taskfile is open
                :rtype: :class:`djadapter.models.TaskFile` | None
                :raises: None
                """
                node = jbscene.get_current_scene_node()
                if not node:
                    return
                tfid = cmds.getAttr('%s.taskfile_id' % node)
                try:
                    return djadapter.taskfiles.get(id=tfid)
                except djadapter.models.TaskFile.DoesNotExist:
                    log.error("No taskfile with id %s was found. Get current scene failed. Check your jb_sceneNode \'%s\'." % (tfid, node))
                    return

            def get_scene_node(self, ):
                """Return the current scenen node or create one if it does not exist

                :returns: Name of the scene node
                :rtype: str
                :raises: None
                """
                node = jbscene.get_current_scene_node()
                if node is None:
                    cmds.namespace(set=':')
                    node = cmds.createNode('jb_sceneNode')
                return node

            def update_scene_node(self, tf):
                """Update the current scene node

                :param tf: the taskfile that is saved
                :type tf: :class:`djadapter.models.TaskFile`
                :returns: None
                :rtype: None
                :raises: None
                """
                node = self.get_scene_node()
                cmds.setAttr('%s.taskfile_id' % node, lock=False)
                cmds.setAttr('%s.taskfile_id' % node, tf.id)
                cmds.setAttr('%s.taskfile_id' % node, lock=True)

            def check_modified(self, ):
                """Check if the current scene was modified and ask the user to continue

                This might save the scene if the user accepts to save before continuing.

                :returns: True if the user accepted to continue.
                :rtype: bool
                :raises: None
                """
                if not cmds.file(q=1, modified=1):
                    return True
                curfile = cmds.file(q=1, sceneName=1)
                r = cmds.confirmDialog( title='Save Changes', message='Save changes to %s?' % curfile,
                                       button=['Save', 'Don\'t Save' ,'Cancel'],
                                       defaultButton='Save', cancelButton='Cancel',
                                       dismissString='Cancel')
                if r == 'Cancel':
                    return False
                if r == 'Save':
                    cmds.file(save=True, force=True)
                return True

        MayaGenesisWin.set_filetype(djadapter.FILETYPES['mayamainscene'],)
        return MayaGenesisWin
