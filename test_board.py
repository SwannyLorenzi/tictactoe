import pytest

from board import Board


@pytest.mark.parametrize('width,height', [(3, 3), (4, 4)])
class TestBoard:

    def test_board_width(self, width, height):
        # Given
        # When
        board = Board(width, height)

        # Then
        assert board.width == width

    def test_board_height(self, width, height):
        # Given
        # When
        board = Board(width, height)

        # Then
        assert board.height == height

    def test_board_cells(self, width, height):
        # Given
        # When
        board = Board(width, height)

        # Then
        assert board.cells == [' '] * width * height
