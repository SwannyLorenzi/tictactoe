import pytest

from board import Board


@pytest.fixture()
def board_partially_filled():
    board = Board()
    board.cells[0] = 'X'
    board.cells[4] = 'O'
    board.cells[2] = 'X'
    return board


@pytest.fixture()
def board_totally_filled():
    board = Board()
    board.cells = ['X', 'O', 'X', 'O', 'X', 'X', 'O', 'X', 'O']
    return board


@pytest.mark.parametrize('width,height', [(3, 3), (4, 4)])
class TestBoardInit:

    @pytest.fixture()
    def board(self, width, height):
        return Board(width, height)

    def test_board_width(self, board, width):
        assert board.width == width

    def test_board_height(self, board, height):
        assert board.height == height

    def test_board_cells(self, board, width, height):
        assert board.cells == [' '] * width * height


class TestBoardStr:

    def test_str_3x3(self):
        assert str(Board()) == '''1:   | 2:   | 3:  
-----+------+-----
4:   | 5:   | 6:  
-----+------+-----
7:   | 8:   | 9:  '''

    def test_str_3x3_partially_filled(self, board_partially_filled):
        assert str(board_partially_filled) == '''1: X | 2:   | 3: X
-----+------+-----
4:   | 5: O | 6:  
-----+------+-----
7:   | 8:   | 9:  '''

    def test_str_3x3_totally_filled(self, board_totally_filled):
        assert str(board_totally_filled) == '''1: X | 2: O | 3: X
-----+------+-----
4: O | 5: X | 6: X
-----+------+-----
7: O | 8: X | 9: O'''

    def test_str_4x3(self):
        assert str(Board(width=4)) == ''' 1:   |  2:   |  3:   |  4:  
------+-------+-------+------
 5:   |  6:   |  7:   |  8:  
------+-------+-------+------
 9:   | 10:   | 11:   | 12:  '''


class TestBoardIsFull:

    def test_is_full(self):
        assert Board().is_full() is False

    def test_is_full_partially_filled(self, board_partially_filled):
        assert board_partially_filled.is_full() is False

    def test_is_full_totally_filled(self, board_totally_filled):
        assert board_totally_filled.is_full() is True
