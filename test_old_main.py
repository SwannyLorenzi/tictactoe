import pytest

from old_main import *


@pytest.mark.parametrize("idx,expected", [(0, (1, 1)), (1, (2, 1)), (3, (1, 2))])
def test_get_xy(idx, expected):
    assert get_xy(idx) == expected


def test_has_idx():
    assert has_idx('X', ['X'], 0)
