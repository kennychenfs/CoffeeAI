class Board:
    def __init__(self, size, board=None):
        self.size = size  # length of each side of the board
        self.board = board or self.createBoard()

    def createBoard(
        self,
    ):  # a hex board in axial coordinates, marked with -1 if it's not a valid position.
        board = [[0] * (self.size * 2 - 1) for _ in range(self.size * 2 - 1)]
        for x in range(self.size * 2 - 1):
            for y in range(self.size * 2 - 1):
                if y - x >= self.size or x - y >= self.size:
                    board[x][y] = -1
        return board
