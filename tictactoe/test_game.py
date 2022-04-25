import pytest

from tictactoe.game import Game


@pytest.mark.parametrize('players, current_player, expected', [
    (['X', 'O'], 'X', 'O'),
    (['X', 'O'], 'O', 'X'),
    (['X', 'O', '#'], 'X', 'O'),
    (['X', 'O', '#'], 'O', '#'),
    (['X', 'O', '#'], '#', 'X'),
])
def test_get_next_player(players, current_player, expected):
    # Given
    game = Game(players=players)

    # When
    actual = game.get_next_player(current_player)

    # Then
    assert actual == expected
