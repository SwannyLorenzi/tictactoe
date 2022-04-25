from math import log10
from typing import List, Tuple

# GAME PARAMETERS
BOARD_WIDTH = 3
BOARD_HEIGHT = 3
BOARD_WIN_SIZE = 3  # Number of consecutive (row / column / diagonal) symbols to align to win
PLAYERS = ['O', 'X']

# Type alias
Board = List[str]


def clear_output() -> None:
    """
    Clears output.

    Does nothing here, replaces Jupyter notebook's cleat_output() to maintain code as is.
    """


# Done
def init_board(width: int = BOARD_WIDTH, height: int = BOARD_HEIGHT) -> Board:
    """
    Initializes a new board with empty cells

    :param width: Board width
    :param height: Board height
    :return: Game board with given dimensions
    """
    return [' '] * (width * height)


# Done -> __str__
def display(board: Board, width: int = BOARD_WIDTH, height: int = BOARD_HEIGHT) -> None:
    """
    Display the board with cell numbers counted from 1 = top left to (board size) = bottom left.

    :param board: Board to display
    :param width: Board width
    :param height: Board height
    """
    idx_pad = 1 + int(log10(width * height))
    row_sep = '\n' + '-+-'.join(['-' * (3 + idx_pad)] * width) + '\n'

    rows = []
    index = 1
    for r in range(0, height):
        cells = []
        for c in range(0, width):
            val = board[r * width + c]
            idx = str(index).rjust(idx_pad, ' ')
            cells.append(f'{idx}: {val}')
            index += 1
        rows.append(' | '.join(cells))
    output = row_sep.join(rows)
    clear_output()
    print(output)
    return None


def get_player_choice(board: Board, player: str) -> int:
    """
    Ask the player to choose a cell number in given grid, and retries until the choice is valid and available.

    Payer must give a number between 1 and board size, and corresponding to an empty cell

    :param board: Game board where an empty cell must be chosen
    :param player: Player marker
    :return: Cell number chosen by the player
    """

    def is_valid(player_choice):
        return player_choice.isdigit() and 1 <= int(player_choice) <= len(board)

    def is_available(player_choice):
        return board[int(player_choice) - 1] == ' '

    choice = 'wrong'

    while not is_valid(choice) or not is_available(choice):
        choice = input(f'Player {player}, please choose a cell number [1 - {len(board)}]: ')
        if not is_valid(choice):
            print(f'Sorry, but "{choice}" is not a valid cell number. Please try again.')
        elif not is_available(choice):
            print(f'Sorry, but "{choice}" cell is already taken. Please choose another one.')

    return int(choice)


def place_choice(board: Board, cell: int, player: str) -> None:
    """
    Place given player's choice on board

    :param board: Game board
    :param cell: Cell number (1 = top left, board size = bottom right)
    :param player: Player marker
    """
    if not 1 <= cell <= len(board):
        return None

    board[cell - 1] = player


def get_xy(cell: int, width: int = BOARD_WIDTH) -> Tuple[int, int]:
    """
    Get x,y coordinates for given cell index

    Does not check correctness or out of board things

    :param cell: Cell index in list (0 based)
    :param width: Board width
    :return: Corresponding x, y coordinates
    """
    x = (cell % width) + 1
    y = (cell // width) + 1
    return x, y


def get_idx(x: int, y: int, width: int = BOARD_WIDTH) -> int:
    """
    Get a cell index from (x, y) coordinates

    Does not check correctness or out of board things

    :param x: Column number (1 based)
    :param y: Row number (1 based)
    :param width: Board width
    :return: Cell index (0 based)
    """
    return (x - 1) + (y - 1) * width


def has_idx(player: str, board: Board, idx: int) -> bool:
    """
    Check if player has marked cell index on bard
    
    :param player: Player marker
    :param board: Game board
    :param idx: Cell index (0 based)
    :return: True if player has marked corresponding cell
    or False if not or if index is out of board
    """
    return 0 <= idx < len(board) and board[idx] == player


def check_cells(player: str, board: Board, idx: int,
                add_x: int = 0, add_y: int = 0, nb_marks: int = BOARD_WIN_SIZE,
                width: int = BOARD_WIDTH,
                height: int = BOARD_HEIGHT
                ) -> bool:
    """
    Checks if player marked cells on given index, into add_x / add_y direction, up to nb_marks
    
    :param player: Player marker
    :param board: Game board
    :param idx: Starting cell index (0 based)
    :param add_x: offset to add to x coordinate
    :param add_y: offset to add to y coordinate
    :param nb_marks: number of markers to find to return True
    :param width: Board width
    :param height: Board height
    :return: True if player has marked nb_marks consecutive cells in board in any direction starting from cell index
    False otherwise
    """
    if nb_marks == 0:
        return True

    (x, y) = get_xy(idx)
    x += add_x
    y += add_y
    next_idx = get_idx(x, y)
    if x < 1 or x > width or y < 1 or y > height:  # Board overflow detection
        next_idx = -1

    return has_idx(player, board, idx) and check_cells(player, board, next_idx, add_x, add_y, nb_marks - 1)


def check_win(player: str, board: Board, win_size: int = BOARD_WIN_SIZE) -> bool:
    """
    Check for player victory in given board
    
    :param player: Player marker
    :param board: Game board
    :param win_size: Number of consecutive cells to mark to win the game
    :return: True if player has marked enough consecutive cells. False otherwise
    """
    if player not in board:
        return False

    index = 0
    for cell in board:
        if cell == player:
            if (
                    check_cells(player, board, index, add_x=1, nb_marks=win_size)
                    or check_cells(player, board, index, add_x=1, add_y=1, nb_marks=win_size)
                    or check_cells(player, board, index, add_y=1, nb_marks=win_size)
                    or check_cells(player, board, index, add_x=-1, add_y=1, nb_marks=win_size)
            ):
                return True
        index += 1
    return False


def next_player(player: str, players: List[str]) -> str:
    """
    Get next playing player marker, rolling on players list

    :param player: Current player marker
    :param players: List of players
    :return: Next player marker
    """
    idx = players.index(player) + 1
    if idx > len(players) - 1:
        idx = 0
    return players[idx]


# Done -> board.is_full()
def is_board_full(board: Board) -> bool:
    """
    Checks whether board is full, i.e. no more marker can be added.

    :param board: Game board
    :return: True if no more marker can be added. False otherwise
    """
    for c in board:
        if c == ' ':
            return False
    return True


def tictactoe() -> None:
    """
    Starts a tic-tac-toe game
    """
    global PLAYERS
    current_player = PLAYERS[0]
    player_won = False

    board = init_board()

    while not player_won and not is_board_full(board):
        display(board)
        cell = get_player_choice(board, current_player)
        place_choice(board, cell, current_player)
        if check_win(current_player, board):
            player_won = True
            break
        current_player = next_player(current_player, PLAYERS)

    display(board)
    if player_won:
        print(f'Congratulations {current_player}, you won!')
    else:
        print("It's a draw!")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tictactoe()
