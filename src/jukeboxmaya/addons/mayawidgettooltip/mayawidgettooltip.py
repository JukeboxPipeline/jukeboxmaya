from PySide import QtGui

from jukeboxmaya.gui import main
from jukeboxcore.gui.widgets.tooltip import JB_WindowToolTip
from jukeboxmaya.plugins import JB_MayaPlugin


class MayaWidgetToolTip(JB_MayaPlugin):
    """A maya plugin that installs a JB_ToolTip at the sidebar

    """

    author = "David Zuber"
    copyright = "2014"
    version =  "0.1"
    description = "ToolTip for selecting open windows"

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
        """Create the tooltip in the sidebar

        :returns: None
        :rtype: None
        :raises: None
        """
        self.sidebar = self.get_maya_sidebar()
        self.lay = self.sidebar.layout()
        self.tool_pb = QtGui.QPushButton("JB Wins")
        self.tooltip = JB_WindowToolTip()
        self.tooltip.install_tooltip(self.tool_pb)
        self.lay.addWidget(self.tool_pb)
        self.tool_pb.clicked.connect(self.tooltip.show)

    def uninit_ui(self):
        """Delete the tooltip

        :returns: None
        :rtype: None
        :raises: None
        """
        self.lay.removeWidget(self.tool_pb)
        self.tooltip.deleteLater()
        self.tool_pb.deleteLater()

    def get_maya_sidebar(self, ):
        """Return the wrapped maya sidebar

        :returns: the wrapped sidebar
        :rtype: QObject
        :raises: None
        """
        lay = main.wrap_maya_ui('MayaWindow|toolBar7|MainToolboxLayout|frameLayout5|flowLayout2')
        return lay
