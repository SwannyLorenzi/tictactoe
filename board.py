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
