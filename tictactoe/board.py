from math import log10


class Board:

    def __init__(self, width: int = 3, height: int = 3):
        self.width = width
        self.height = height
        self.cells = [' '] * (width * height)

    def __str__(self):
        idx_pad = 1 + int(log10(self.width * self.height))
        row_sep = '\n' + '-+-'.join(['-' * (3 + idx_pad)] * self.width) + '\n'

        rows = []
        index = 1
        for r in range(0, self.height):
            cells = []
            for c in range(0, self.width):
                val = self.cells[r * self.width + c]
                idx = str(index).rjust(idx_pad, ' ')
                cells.append(f'{idx}: {val}')
                index += 1
            rows.append(' | '.join(cells))
        return row_sep.join(rows)

    def is_full(self) -> bool:
        """
        Checks whether board is full, i.e. no more marker can be added.

        :return: True if no more marker can be added. False otherwise
        """
        return ' ' not in self.cells

    def place_choice(self, cell: int, player: str) -> None:
        """
        Place given player's choice on board.

        :param cell: Cell number (1 = top left, board size = bottom right)
        :param player: Player marker
        """
        if not 1 <= cell <= len(self.cells):
            return None

        self.cells[cell - 1] = player

    def next_cell(self, cell: int, add_x: int, add_y: int) -> int:
        """
        Get next cell index for given cell and x, y direction.

        :param cell: Cell to move from
        :param add_x: x offset to add
        :param add_y: y offset to add
        :return: Next cell index for given direction, -1 if move gets out of board.
        """
        cell_id = cell - 1
        x = (cell_id % self.width) + add_x
        y = (cell_id // self.width) + add_y
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            # Board overflow
            return -1
        else:
            return 1 + x + y * self.width

    def has_mark_at(self, cell: int, player: str) -> bool:
        """
        Check if player has marked given cell on board

        :param cell: Cell index (0 based)
        :param player: Player marker
        :return: True if player has marked corresponding cell
        or False if not or if index is out of board
        """
        return 0 < cell <= len(self.cells) and self.cells[cell - 1] == player

        pass

    def check_cells(self, cell: int, player: str, add_x: int, add_y: int, nb_marks: int) -> bool:
        """
        Check if player marked cells at given position, into add_x/add_y direction, up to nb_marks.

        :param cell: Starting cell position on board
        :param player: Player marker to look for
        :param add_x: Offset to add to x coordinate
        :param add_y: Offset to add to y coordinate
        :param nb_marks: Number of player markers to find to return true
        :return: True if player has marked nb_marks consecutive cells on board in given direction starting from cell position
        False otherwise
        """
        if nb_marks == 0:
            return True

        next_cell = self.next_cell(cell, add_x, add_y)
        return self.has_mark_at(cell, player) and self.check_cells(next_cell, player, add_x, add_y, nb_marks - 1)
