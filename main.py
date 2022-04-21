from math import log10

# GAME PARAMETERS
BOARD_WIDTH = 3
BOARD_HEIGHT = 3
BOARD_WIN_SIZE = 3  # Number of consecutive (row/col/diag) symbols to align to win
PLAYERS = ['O', 'X']

def clear_output():
    pass

def init_board(width=BOARD_WIDTH, height=BOARD_HEIGHT):
    '''
    Initializes a board list with empty cells
    '''
    return [' '] * (width * height)


def display(board, width=BOARD_WIDTH, height=BOARD_HEIGHT):
    '''
    Display the board with cell numbers counted from 1 = top left to 9 = bottom left.
    '''
    idx_pad = 1 + int(log10(width * height))
    row_sep = '\n' + '-+-'.join(['-' * (3 + idx_pad) for i in range(0, width)]) + '\n'

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


def get_player_choice(board, player):
    '''
    Ask for player choice and check its validity.
    Payer must give a number between 1 and board size
    '''

    def is_valid(choice):
        return choice.isdigit() and 1 <= int(choice) <= len(board)

    def is_available(choice):
        return board[int(choice) - 1] == ' '

    choice = 'wrong'

    while not is_valid(choice) or not is_available(choice):
        choice = input(f'Player {player}, please choose a cell number [1 - {len(board)}]: ')
        if not is_valid(choice):
            print(f'Sorry, but "{choice}" is not a valid cell number. Please try again.')
        elif not is_available(choice):
            print(f'Sorry, but "{choice}" cell is already taken. Please choose another one.')

    return int(choice)


def place_choice(board, cell, player):
    '''
    Place given player's choice on board
    cell is cell number as asked, 1 = top left, (board size) = bottom right
    '''
    if not 1 <= cell <= len(board):
        return None

    board[cell - 1] = player
    return None


def get_xy(cell, width=BOARD_WIDTH, height=BOARD_HEIGHT):
    '''
    Get (x, y) coordinates from a cell index
    '''
    x = (cell % width) + 1
    y = (cell // width) + 1
    return (x, y)


def get_idx(x, y, width=BOARD_WIDTH, height=BOARD_HEIGHT):
    '''
    Get a cell index from (x, y) coordinates
    '''
    return (x - 1) + (y - 1) * width


def has_idx(player, board, idx):
    '''
    Check if player has marked cell index on bard
    Return True if it has, False if not or if asked index is out of board
    '''
    return 0 <= idx < len(board) and board[idx] == player


def check_cells(player, board, idx, add_x=0, add_y=0, nb_marks=BOARD_WIN_SIZE, width=BOARD_WIDTH, height=BOARD_HEIGHT):
    '''
    Checks if player marked cells on given index, into add_x / add_y direction, up to nb_marks
    '''
    if nb_marks == 0:
        return True

    (x, y) = get_xy(idx)
    x += add_x
    y += add_y
    next_idx = get_idx(x, y)
    if x < 1 or x > width or y < 1 or y > height:  # Board overflow detection
        next_idx = -1

    return has_idx(player, board, idx) and check_cells(player, board, next_idx, add_x, add_y, nb_marks - 1)


def check_win(player, board, win_size=BOARD_WIN_SIZE, width=BOARD_WIDTH, height=BOARD_HEIGHT):
    '''
    Check for player victory: win_size consecutive marks on same line, column or diagonal
    '''
    if not player in board:
        return False

    index = 0
    for cell in board:
        if cell == player:
            if (check_cells(player, board, index, add_x=1, nb_marks=win_size)
                    or check_cells(player, board, index, add_x=1, add_y=1, nb_marks=win_size)
                    or check_cells(player, board, index, add_y=1, nb_marks=win_size)
                    or check_cells(player, board, index, add_x=-1, add_y=1, nb_marks=win_size)
            ):
                return True
        index += 1
    return False


def next_player(player, players):
    idx = players.index(player) + 1
    if idx > len(players) - 1:
        idx = 0
    return players[idx]


def is_board_full(board):
    for c in board:
        if c == ' ':
            return False
    return True


def tictactoe():
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