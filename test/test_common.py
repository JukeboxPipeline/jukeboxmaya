import pytest

from jukeboxmaya import common


@pytest.mark.parametrize("inp,expected", [
    ("|hallo1:wasgeht:asdfsa|:asdf:asdf|:hallo1:SAD", "hallo1"),
    ("|asdfsaf|asdf|hallo1:hallo", "hallo1"),
    ("adsfadsf|asdf:asdf|hallo1:hallo", "hallo1"),
    ("hallo1:halloasdfasdf_Asdf", "hallo1"),
    ("asdfjkl|ADSfafs:asdf:asd|hallo", ":"),
    ("|hallo1:buh:yeah", "hallo1"),
    ("|:hallo1:buh:yeah", "hallo1")
])
def test_get_top_namespace(inp, expected):
    assert common.get_top_namespace(inp) == expected


@pytest.mark.parametrize("inp,expected", [
    ("|hallo1:wasgeht:asdfsa|:asdf:asdf|:hallo1:SAD", ":hallo1"),
    ("|asdfsaf|asdf|hallo1:hallo", "hallo1"),
    ("adsfadsf|asdf:asdf|hallo1:hallo", "hallo1"),
    ("hallo1:halloasdfasdf_Asdf", "hallo1"),
    ("asdfjkl|ADSfafs:asdf:asd|hallo", ":"),
    ("|hallo1:buh:yeah", "hallo1:buh"),
    ("|:hallo1:buh:yeah", ":hallo1:buh"),
    ("|ab:cd|ef:gh:ij|kl:mn:op:qr", "kl:mn:op"),
    ("hallo", ":"),
    ("|hallo", ":"),
    ("|:hallo", ":")
])
def test_get_namespace(inp, expected):
    assert common.get_namespace(inp) == expected
