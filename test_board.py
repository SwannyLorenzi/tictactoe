import pytest

from board import Board


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
        # Given
        board = Board()

        # When
        board_str = str(board)

        # Then
        assert board_str == '''1:   | 2:   | 3:  
-----+------+-----
4:   | 5:   | 6:  
-----+------+-----
7:   | 8:   | 9:  '''

    def test_str_3x3_partially_filled(self):
        # Given
        board = Board()
        board.cells[0] = 'X'
        board.cells[4] = 'O'
        board.cells[2] = 'X'

        # When
        board_str = str(board)

        # Then
        assert board_str == '''1: X | 2:   | 3: X
-----+------+-----
4:   | 5: O | 6:  
-----+------+-----
7:   | 8:   | 9:  '''

    def test_str_3x3_totally_filled(self):
        # Given
        board = Board()
        board.cells = ['X', 'O', 'X', 'O', 'X', 'X', 'O', 'X', 'O']

        # When
        board_str = str(board)

        # Then
        assert board_str == '''1: X | 2: O | 3: X
-----+------+-----
4: O | 5: X | 6: X
-----+------+-----
7: O | 8: X | 9: O'''

    def test_str_4x3(self):
        # Given
        board = Board(width=4)

        # When
        board_str = str(board)

        # Then
        assert board_str == ''' 1:   |  2:   |  3:   |  4:  
------+-------+-------+------
 5:   |  6:   |  7:   |  8:  
------+-------+-------+------
 9:   | 10:   | 11:   | 12:  '''
