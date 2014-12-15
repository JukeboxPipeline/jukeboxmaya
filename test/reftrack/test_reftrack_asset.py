import os

import pytest



@pytest.mark.parametrize("refobj", [("a", "b", "c", "d", None, "asdf")])
def test_is_replaceable(refobj, typinter):
    # assert always returns True
    assert typinter.is_replaceable(refobj) is True
