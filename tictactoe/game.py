from typing import List

from tictactoe.board import Board


class Game:

    def __init__(self, width: int = 3, height: int = 3, nb_marks: int = 3, players: List[str] = ('X', 'O')) -> None:
        self.board = Board(width, height)
        self.nb_marks = nb_marks
        self.players = players

    def get_player_choice(self, player: str) -> int:
        """
        Ask the player to choose a cell number in given grid, and retries until the choice is valid and available.

        Payer must give a number between 1 and board size, and corresponding to an empty cell

        :param player: Player marker
        :return: Cell number chosen by the player
        """

        def is_valid(player_choice):
            return player_choice.isdigit() and 1 <= int(player_choice) <= len(self.board.cells)

        def is_available(player_choice):
            return self.board.cells[int(player_choice) - 1] == ' '

        choice = 'wrong'

        while not is_valid(choice) or not is_available(choice):
            choice = input(f'Player {player}, please choose a cell number [1 - {len(self.board.cells)}]: ')
            if not is_valid(choice):
                print(f'Sorry, but "{choice}" is not a valid cell number. Please try again.')
            elif not is_available(choice):
                print(f'Sorry, but "{choice}" cell is already taken. Please choose another one.')

        return int(choice)

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
        """
        Starts a tic-tac-toe game
        """
        current_player = self.players[0]
        player_won = False

        while not player_won and not self.board.is_full():
            print(self.board)
            cell = self.get_player_choice(current_player)
            self.board.place_choice(cell, current_player)
            if self.board.check_victory(current_player, self.nb_marks):
                player_won = True
                break
            current_player = self.get_next_player(current_player)

        print(self.board)
        if player_won:
            print(f'Congratulations {current_player}, you won!')
        else:
            print("It's a draw!")

