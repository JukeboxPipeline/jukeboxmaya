import mock

from jukeboxcore import errors
from jukeboxmaya.menu import MenuManager


@mock.patch('jukeboxmaya.menu.cmds.setParent')
@mock.patch('jukeboxmaya.menu.cmds.menu')
@mock.patch('jukeboxmaya.menu.cmds.menuItem')
@mock.patch('jukeboxmaya.menu.cmds.deleteUI')
def test_menu_manager(new_delete, new_menuitem, new_menu, new_setparent):
    """Test menu manager"""
    new_menu.return_value = "mockedmenu"

    mm = MenuManager.get()
    mm.delete_all_menus()
    new_delete.reset_mock()
    jm = mm.create_menu('Jukebox')
    new_menu.assert_called_with(label='Jukebox')
    new_menuitem.return_value = "mockedmenuitem1"
    stuffm = mm.create_menu('Stuff', jm)
    new_menuitem.assert_called_with(label='Stuff', parent='mockedmenu')
    new_menuitem.return_value = "mockedmenuitem2"
    nestedm = mm.create_menu('Nested Stuff', stuffm)
    new_menuitem.assert_called_with(label='Nested Stuff', parent='mockedmenuitem1')
    try:
        mm.create_menu('Nested Stuff', stuffm)
    except errors.MenuExistsError:
        pass
    else:
        raise AssertionError('Creating the same menu twice should raise an exception!')
    assert mm.menus['Jukebox'] is jm
    assert jm['Stuff'] is stuffm
    assert stuffm['Nested Stuff'] is nestedm
    mm.delete_menu(stuffm)
    assert 'Nested Stuff' not in stuffm
    mm.delete_all_menus()

    deletecalls = [mock.call("mockedmenuitem2"), mock.call("mockedmenuitem1"), mock.call("mockedmenu")]
    new_delete.assert_has_calls(deletecalls)
