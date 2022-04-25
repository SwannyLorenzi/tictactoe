from typing import List

from tictactoe.board import Board


class Game:

    def __init__(self, width: int = 3, height: int = 3, nb_marks: int = 3, players: List[str] = ('X', 'O')) -> None:
        self.board = Board(width, height)
        self.nb_marks = nb_marks
        self.players = players

    def get_player_choice(self, player: str) -> int:
        pass

    def get_next_player(self, current_player: str) -> str:
        """
        Get next playing player marker, rolling on players list.

        :param current_player: Current player marker
        :return: Next player marker
        """
        idx = self.players.index(current_player) + 1
        if idx >= len(self.players):
            idx = 0
        return self.players[idx]

    def run(self):
        pass
