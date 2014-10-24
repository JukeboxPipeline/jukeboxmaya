from jukeboxcore import errors
from jukeboxmaya.menu import MenuManager


def test_menu_manager():
    """Test menu manager"""
    mm = MenuManager.get()
    mm.delete_all_menus()
    jm = mm.create_menu('Jukebox')
    stuffm = mm.create_menu('Stuff', jm)
    nestedm = mm.create_menu('Nested Stuff', stuffm)
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
