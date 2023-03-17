class OutputHelper:
    BACKGROUND = "\x1b[48;5;"
    WORD = "\x1b[38;5;"
    END = "m"
    RESET = "\x1b[0m"

    def colorize(self, text, wordColor=None, backgroundColor=None):
        result = ""
        if wordColor is not None:
            result += self.WORD + str(wordColor) + self.END
        if backgroundColor is not None:
            result += self.BACKGROUND + str(backgroundColor) + self.END
        result += text
        result += self.RESET
        return result


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        if other == None:
            return False
        return self.x == other.x and self.y == other.y

    def getDirection(self, other):
        if self == other:
            raise ValueError("Cannot get direction of same position")
        array = other - self
        if array.x != 0 and array.y == 0:
            return 1
        elif array.x == 0 and array.y != 0:
            return 2
        elif array.x == array.y:
            return 3
        else:
            raise ValueError(
                f"The two positions are not in the same line:{self} and {other}"
            )

    def __str__(self):
        return f"({self.x}, {self.y})"


outputHelper = OutputHelper()


class HexBoard:
    def __init__(self, size, winLen, board=None, initPlayer=1):
        self.size = size  # length of each side of the board
        self.winLen = winLen  # number of pieces in a row to win
        self.board = board or self.createBoard()
        # board slot value:
        # -1: invalid position
        # 0: empty
        # 1: player 1
        # 2: player 2
        self.player = initPlayer
        self.lastPosition = None
        self.lastDirection = None
        self.result = None

    def createBoard(
        self,
    ):  # a hex board in axial coordinates, marked with -1 if it's not a valid position.
        board = [[0] * (self.size * 2 - 1) for _ in range(self.size * 2 - 1)]
        for x in range(self.size * 2 - 1):
            for y in range(self.size * 2 - 1):
                if y - x >= self.size or x - y >= self.size:
                    board[x][y] = -1
        return board

    def isValid(self, position, direction):
        # check position
        if (
            position.x > self.size * 2 - 1
            or position.y > self.size * 2 - 1
            or position.x < 0
            or position.y < 0
        ):
            return False, "out of board"
        if self.board[position.x][position.y] == -1:
            return False, "out of board"
        if self.board[position.x][position.y] > 0:
            return False, "position occupied"
        # check direction
        if direction > 3 or direction < 1:
            return False, "invalid direction"
        if self.lastPosition is None:
            return True, None
        inSameLine = self.lastPosition.getDirection(position) == self.lastDirection
        if not inSameLine:
            return False, "not in the given direction"
        return True, None

    def play(self, player, position, direction):
        valid, errorMessage = self.isValid(position, direction)
        if not valid:
            raise ValueError(errorMessage)
        if self.board[position.x][position.y] > 0:
            raise ValueError(
                f"Board:\n{self}\nPosition is {position} already occupied."
            )
        if self.board[position.x][position.y] == -1:
            raise ValueError(f"Position {position} is invalid.")

        self.board[position.x][position.y] = player
        self.lastPosition = position
        self.lastDirection = direction
        self.player = 3 - self.player
        return True

    def getHumanInputAndPlay(self):
        while True:
            try:
                print(self)
                x, y, direction = map(
                    int, input("Position and direction(x y d): ").split()
                )
                position = Position(x, y)
                done = self.play(self.player, position, direction)
                while not done:
                    print("Invalid move, please try again.")
                    x, y, direction = map(
                        int, input("Position and direction(x y d): ").split()
                    )
                    position = Position(x, y)
                    done = self.play(self.player, position, direction)
                break
            except ValueError as e:
                print(e)
                print("Please try again.")
        if self.isTerminal():
            print(f"Player {self.player} wins!")
            return True
        return False

    def isTerminal(self):
        x = self.lastPosition.x
        y = self.lastPosition.y
        if self.lastPosition is None:
            return False
        if self.isWinByLine():
            self.result = 3 - self.player
            return True
        for x in range(self.size * 2 - 1):
            if self.board[x][y] == 0:
                return False
        for y in range(self.size * 2 - 1):
            if self.board[x][y] == 0:
                return False
        _min = min(x, y)
        x -= _min
        y -= _min
        for i in range(self.size * 2 - 1):
            if x >= self.size * 2 - 1 or y >= self.size * 2 - 1:
                break
            if self.board[x + i][y + i] == 0:
                return False
        return True

    def isWinByLine(self):
        checkPlayer = 3 - self.player
        # This function is written by ChatGPT. Cool!
        if self.lastPosition is None:
            return False
        directions = [
            Position(0, 1),
            Position(1, 0),
            Position(1, 1),
            Position(0, -1),
            Position(-1, 0),
            Position(-1, -1),
        ]
        for direction in directions:
            count = 1
            pos = self.lastPosition
            while True:
                pos = pos + direction
                if (
                    pos.x < 0
                    or pos.y < 0
                    or pos.x >= self.size * 2 - 1
                    or pos.y >= self.size * 2 - 1
                    or self.board[pos.x][pos.y] != checkPlayer
                ):
                    break
                count += 1
            pos = self.lastPosition
            while True:
                pos = pos - direction
                if (
                    pos.x < 0
                    or pos.y < 0
                    or pos.x >= self.size * 2 - 1
                    or pos.y >= self.size * 2 - 1
                    or self.board[pos.x][pos.y] != checkPlayer
                ):
                    break
                count += 1
            if count >= self.winLen:
                return True
        return False

    def __str__(self):
        result = f"Board size: {self.size}\n"
        for x in range(self.size * 2 - 1):
            spaces = abs(x - (self.size - 1))
            result += "  " * spaces
            for y in range(
                max(0, x - (self.size - 1)), min(self.size * 2 - 1, x + self.size)
            ):
                assert self.board[x][y] != -1
                if self.board[x][y] == 0:
                    word = "."
                elif self.board[x][y] == 1 or self.board[x][y] == 2:
                    word = " "
                if Position(x, y) == self.lastPosition:
                    word = " /-\\"[self.lastDirection]
                backgroundColor = [None, 196, 33][self.board[x][y]]

                result += outputHelper.colorize(word, backgroundColor=backgroundColor)
                result += "   "
            result += "\n"
        result += f"last position: {self.lastPosition}\n"
        return result


if __name__ == "__main__":
    """b = Board(5)
    b.board[0][4] = 1  # player 1, direction 1
    b.board[4][6] = 5  # player 2, direction 2
    b.board[6][5] = 3  # player 1, direction 3
    # the moves are not valid, but it's just for testing
    print(b)"""
    b = HexBoard(5, 4)
    while True:
        if b.getHumanInputAndPlay():
            break
