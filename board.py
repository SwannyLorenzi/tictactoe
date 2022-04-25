class Board:

    def __init__(self, width: int = 3, height: int = 3):
        self.width = width
        self.height = height
        self.cells = [' '] * (width * height)
