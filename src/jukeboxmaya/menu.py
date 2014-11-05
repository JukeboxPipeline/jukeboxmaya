""" Here are functions and classes for tasks related to menu creation in maya """
from weakref import WeakValueDictionary

import maya.cmds as cmds

from jukeboxcore.log import get_logger
log = get_logger(__name__)
from jukeboxcore import errors


class Menu(WeakValueDictionary):
    """ This represents a maya menu or menuitem that was created with cmds.menu/cmds.menuitem

    .. Important::

      Note that you should use the MenuManager for Menu creation!
      For creation, it is better to use :py:func:`jukebox.menu.MenuManager.create_menu`.

    Menu features several attributes that can be accesed via getters:

      :menustring: The string that is used in maya to identify the menu
      :parent: A reference to the parent Menu if the menuitem has one. A menu does not have a parent.
      :name: The name of the Menu. The name is used to identify the Menu. The children of one parent should have unique names.
      :kwargs: a dict with arguments used during creation.

    Menu is a subclass of WeakValueDictionary. Its values are the children menuitems. The keys are the name attributes of the Menu instance.
    If you set the parent of a child to None, it will also be deleted from Menu if there are no further references.
    We have to do this, to prevent circular references.

    Example::

      topm = Menu('topm', label='topm')
      sub1 = Menu('submenu1', parent=topm, label='submenu1', subMenu=True)
      sub2 = Menu('Divider', parent=sub1, divider=1, nolabel=1) # Divider should not have a label

      # evaluates to True
      sub2 is sub1['Divider']
      sub2.kwargs()['divider'] == 1
      # delete a submenu
      sub2._delete()
      sub2 = None  # delete reference to sub2
      sub1.has_key('Divider') == False  # sub2 is garbage collected and not part of sub1 anymore

    """

    def __init__(self, name, parent=None, nolabel=False, **kwargs):
        """ Creates a maya menu or menu item

        :param name: Used to access a menu via its parent. Unless the nolabel flag is set to True, the name will also become the label of the menu.
        :type name: str
        :param parent: Optional - The parent menu. If None, this will create a toplevel menu. If parent menu is a Menu instance, this will create a menu item. Default is None.
        :type parent: Menu|None
        :param nolabel: Optional - If nolabel=True, the label flag for the maya command will not be overwritten by name
        :type nolabel: bool
        :param kwargs: all keyword arguments used for the cmds.menu/cmds.menuitem command
        :type kwargs: named arguments
        :returns: None
        :rtype: None
        :raises: errors.MenuExistsError
        """
        WeakValueDictionary.__init__(self)
        self.__menustring = None
        self.__parent = parent
        self.__name = name
        self.__kwargs = kwargs
        if not nolabel:
            self.__kwargs['label'] = name
        if parent is not None:
            if name in parent:
                raise errors.MenuExistsError("A menu with this name: %s and parent: %s exists already!" % (name, parent))
            cmds.setParent(parent.menustring(), menu=1)
            self.__kwargs['parent'] = parent.menustring()
            self.__menustring = cmds.menuItem(**self.__kwargs)
            parent[name] = self
        else:
            cmds.setParent('MayaWindow')
            self.__menustring = cmds.menu(**self.__kwargs)

    def __str__(self, ):
        """ Return a nice readable description of menu

        :returns: a readable menudescription
        :rtype: str
        :raises: None
        """
        if self.__parent is not None:
            return "<\"%s\" Menu object, Parent: %s>" % (self.__name, self.__parent.name())
        else:
            return "<\"%s\" Menu object>" % self.__name

    def _delete(self, ):
        """ Delete the menu and remove it from parent

        Deletes all children, so they do not reference to this instance and it can be garbage collected.
        Sets parent to None, so parent is also garbage collectable

        This has proven to be very unreliable. so we delete the menu from the parent manually too.

        :returns: None
        :rtype: None
        :raises: None
        """
        for k in self.keys():
            try:
                self[k]._delete()
            except KeyError:
                pass
        if self.__parent is not None:
            del self.__parent[self.__name]
            self.__parent = None
        cmds.deleteUI(self.__menustring)

    def menustring(self, ):
        """ Return the string that is used by maya to identify the ui

        :returns: the string that is used by maya to identify the ui
        :rtype: st
        :raises: None
        """
        return self.__menustring

    def parent(self, ):
        """ Return the parent of the menu or None if this is a toplevel menu

        :returns: the parent menu or None
        :rtype: Menu|None
        :raises: None
        """
        return self.__parent

    def name(self, ):
        """ Return the name of the menu

        the name can be used in a parent as key to retrieve the instance again.

        :returns: name
        :rtype: str
        :raises: None
        """
        return self.__name

    def kwargs(self, ):
        """ Return the keyword arguments used in maya command for creation

        :returns: creation keyword arguments
        :rtype: dict
        :raises: None
        """
        return self.__kwargs


class MenuManager(object):
    """ A Manager for menus in maya.

    The toplevel menus are stored inside self.menus.
    All child menus are stored in those.

    .. Important:: Use MenuManager.get() to obtain the menumanager!
    """

    menumanager = None
    """ MenuManger instance when using MenuManager.get() """

    def __init__(self, ):
        """ Constructs a Menu Manager

        :returns: None
        :rtype: None
        :raises: None
        """
        self.menus = {}

    @classmethod
    def get(cls):
        """ Return a MenuManager Instance.

        This will always return the same instance. If the instance is not available
        it will be created and returned.

        :returns: always the same MenuManager
        :rtype: MenuManager
        :raises: None
        """
        if not cls.menumanager:
            cls.menumanager = cls()
        return cls.menumanager

    def create_menu(self, name, parent=None, **kwargs):
        """ Creates a maya menu or menu item

        :param name: Used to access a menu via its parent. Unless the nolabel flag is set to True, the name will also become the label of the menu.
        :type name: str
        :param parent: Optional - The parent menu. If None, this will create a toplevel menu. If parent menu is a Menu instance, this will create a menu item. Default is None.
        :type parent: Menu|None
        :param nolabel: Optional - If nolabel=True, the label flag for the maya command will not be overwritten by name
        :type nolabel: bool
        :param kwargs: all keyword arguments used for the cmds.menu/cmds.menuitem command
        :type kwargs: named arguments
        :returns: None
        :rtype: None
        :raises: errors.MenuExistsError
        """
        m = Menu(name, parent, **kwargs)
        if parent is None:
            self.menus[name] = m
        return m

    def delete_menu(self, menu):
        """ Delete the specified menu

        :param menu:
        :type menu:
        :returns:
        :rtype:
        :raises:
        """
        if menu.parent is None:
            del self.menus[menu.name()]
        menu._delete()

    def delete_all_menus(self, ):
        """ Delete all menues managed by this manager

        :returns: None
        :rtype: None
        :raises: None
        """
        for m in self.menus.itervalues():
            m._delete()
        self.menus.clear()
