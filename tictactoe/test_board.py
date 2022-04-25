import pytest

from tictactoe.board import Board


@pytest.fixture()
def board_empty():
    return Board()


@pytest.fixture()
def board_draw():
    board = Board()
    board.cells = ['X', 'O', 'X', 'O', 'X', 'X', 'O', 'X', 'O']
    return board


@pytest.fixture()
def board_partial_horizontal():
    board = Board()
    board.cells[0] = 'X'
    board.cells[1] = 'X'
    return board


@pytest.fixture()
def board_winning_horizontal():
    board = Board()
    board.cells[0] = 'X'
    board.cells[1] = 'X'
    board.cells[2] = 'X'
    return board


@pytest.fixture()
def board_partial_vertical():
    board = Board()
    board.cells[0] = 'X'
    board.cells[3] = 'X'
    return board


@pytest.fixture()
def board_winning_vertical():
    board = Board()
    board.cells[0] = 'X'
    board.cells[3] = 'X'
    board.cells[6] = 'X'
    return board


@pytest.fixture()
def board_partial_backward_diagonal():
    board = Board()
    board.cells[0] = 'X'
    board.cells[4] = 'X'
    return board


@pytest.fixture()
def board_winning_backward_diagonal():
    board = Board()
    board.cells[0] = 'X'
    board.cells[4] = 'X'
    board.cells[8] = 'X'
    return board


@pytest.fixture()
def board_partial_forward_diagonal():
    board = Board()
    board.cells[2] = 'X'
    board.cells[4] = 'X'
    return board


@pytest.fixture()
def board_winning_forward_diagonal():
    board = Board()
    board.cells[2] = 'X'
    board.cells[4] = 'X'
    board.cells[6] = 'X'
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

    def test_str_3x3_partially_filled(self, board_winning_horizontal):
        assert str(board_winning_horizontal) == '''1: X | 2: X | 3: X
-----+------+-----
4:   | 5:   | 6:  
-----+------+-----
7:   | 8:   | 9:  '''

    def test_str_3x3_totally_filled(self, board_draw):
        assert str(board_draw) == '''1: X | 2: O | 3: X
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


class TestIsFull:

    def test_is_full(self):
        assert Board().is_full() is False

    def test_is_full_partially_filled(self, board_winning_horizontal):
        assert board_winning_horizontal.is_full() is False

    def test_is_full_totally_filled(self, board_draw):
        assert board_draw.is_full() is True


class TestPlaceChoice:

    def test_place_choice_on_board(self):
        # Given
        board = Board()
        cell = 1
        player = 'X'

        expected_cells = [*board.cells]
        expected_cells[cell - 1] = player

        # When
        board.place_choice(cell, player)

        # Then
        assert board.cells == expected_cells

    @pytest.mark.parametrize('cell', [0, 10, -1])
    def test_place_choice_outside_board(self, cell):
        # Given
        board = Board()
        player = 'X'

        expected_cells = [*board.cells]

        # When
        board.place_choice(cell, player)

        # Then
        assert board.cells == expected_cells


class TestNextCell:

    @pytest.mark.parametrize('cell, add_x, add_y, expected', [
        (1, 1, 0, 2), (1, 1, 1, 5), (1, 0, 1, 4), (2, -1, 1, 4),
        (3, 1, 0, -1), (3, 1, 1, -1), (7, 0, 1, -1), (1, -1, 1, -1),
    ])
    def test_next_cell(self, board_empty, cell, add_x, add_y, expected):
        # Given
        board = board_empty

        # When
        cell = board.next_cell(cell, add_x, add_y)

        # Then
        assert cell == expected


class TestHasMarkAt:

    @pytest.mark.parametrize('cell, player, expected', [
        (1, 'X', True), (1, 'O', False), (2, 'O', True), (0, 'O', False), (10, 'O', False)
    ])
    def test_marked_at(self, board_draw, cell, player, expected):
        assert board_draw.has_mark_at(cell, player) is expected


class TestCheckCells:

    def test_nb_marks_0(self, board_empty):
        assert board_empty.check_cells(1, 'X', add_x=1, add_y=1, nb_marks=0) is True

    @pytest.mark.parametrize('add_x, add_y, expected', [(1, 0, False), (1, 1, False), (0, 1, False), (-1, 1, False)])
    def test_board_empty(self, board_empty, add_x, add_y, expected):
        assert board_empty.check_cells(1, 'X', add_x, add_y, nb_marks=3) is expected

    @pytest.mark.parametrize('add_x, add_y, expected', [(1, 0, False), (1, 1, False), (0, 1, False), (-1, 1, False)])
    def test_board_draw(self, board_draw, add_x, add_y, expected):
        assert board_draw.check_cells(1, 'X', add_x, add_y, nb_marks=3) is expected

    @pytest.mark.parametrize('add_x, add_y, expected', [(1, 0, False), (1, 1, False), (0, 1, False), (-1, 1, False)])
    def test_partial_right(self, board_partial_horizontal, add_x, add_y, expected):
        assert board_partial_horizontal.check_cells(1, 'X', add_x, add_y, nb_marks=3) is expected

    @pytest.mark.parametrize('add_x, add_y, expected', [(1, 0, True), (1, 1, False), (0, 1, False), (-1, 1, False)])
    def test_winning_right(self, board_winning_horizontal, add_x, add_y, expected):
        assert board_winning_horizontal.check_cells(1, 'X', add_x, add_y, nb_marks=3) is expected

    @pytest.mark.parametrize('add_x, add_y, expected', [(1, 0, False), (1, 1, False), (0, 1, False), (-1, 1, False)])
    def test_partial_down_right(self, board_partial_backward_diagonal, add_x, add_y, expected):
        assert board_partial_backward_diagonal.check_cells(1, 'X', add_x, add_y, nb_marks=3) is expected

    @pytest.mark.parametrize('add_x, add_y, expected', [(1, 0, False), (1, 1, True), (0, 1, False), (-1, 1, False)])
    def test_winning_down_right(self, board_winning_backward_diagonal, add_x, add_y, expected):
        assert board_winning_backward_diagonal.check_cells(1, 'X', add_x, add_y, nb_marks=3) is expected

    @pytest.mark.parametrize('add_x, add_y, expected', [(1, 0, False), (1, 1, False), (0, 1, False), (-1, 1, False)])
    def test_partial_down(self, board_partial_vertical, add_x, add_y, expected):
        assert board_partial_vertical.check_cells(1, 'X', add_x, add_y, nb_marks=3) is expected

    @pytest.mark.parametrize('add_x, add_y, expected', [(1, 0, False), (1, 1, False), (0, 1, True), (-1, 1, False)])
    def test_winning_down(self, board_winning_vertical, add_x, add_y, expected):
        assert board_winning_vertical.check_cells(1, 'X', add_x, add_y, nb_marks=3) is expected

    @pytest.mark.parametrize('add_x, add_y, expected', [(1, 0, False), (1, 1, False), (0, 1, False), (-1, 1, False)])
    def test_partial_down_left(self, board_partial_forward_diagonal, add_x, add_y, expected):
        assert board_partial_forward_diagonal.check_cells(3, 'X', add_x, add_y, nb_marks=3) is expected

    @pytest.mark.parametrize('add_x, add_y, expected', [(1, 0, False), (1, 1, False), (0, 1, False), (-1, 1, True)])
    def test_winning_down_left(self, board_winning_forward_diagonal, add_x, add_y, expected):
        assert board_winning_forward_diagonal.check_cells(3, 'X', add_x, add_y, nb_marks=3) is expected


class TestCheckVictory:

    @pytest.mark.parametrize('board_fixture, player, expected', [
        ('board_empty', 'X', False), ('board_empty', 'O', False),
        ('board_draw', 'X', False), ('board_draw', 'O', False),
        ('board_partial_horizontal', 'X', False), ('board_partial_horizontal', 'O', False),
        ('board_winning_horizontal', 'X', True), ('board_winning_horizontal', 'O', False),
        ('board_partial_vertical', 'X', False), ('board_partial_vertical', 'O', False),
        ('board_winning_vertical', 'X', True), ('board_winning_vertical', 'O', False),
        ('board_partial_backward_diagonal', 'X', False), ('board_partial_backward_diagonal', 'O', False),
        ('board_winning_backward_diagonal', 'X', True), ('board_winning_backward_diagonal', 'O', False),
        ('board_partial_forward_diagonal', 'X', False), ('board_partial_forward_diagonal', 'O', False),
        ('board_winning_forward_diagonal', 'X', True), ('board_winning_forward_diagonal', 'O', False),
    ])
    def test_check_victory(self, board_fixture, player, expected, request):
        # Given
        board = request.getfixturevalue(board_fixture)
        nb_marks = 3

        # When
        result = board.check_victory(player, nb_marks)

        # Then
        assert result is expected
