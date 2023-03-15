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


class Board:
    def __init__(self, size, board=None, player=1):
        self.size = size  # length of each side of the board
        self.board = board or self.createBoard()
        # board slot value:
        # -1: invalid position
        # 0: empty
        # 1: player 1, direction 1
        # 2: player 1, direction 2
        # 3: player 1, direction 3
        # 4: player 2, direction 1
        # 5: player 2, direction 2
        # 6: player 2, direction 3
        self.player = player
        self.lastPosition = None

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
        if self.board[position.x][position.y] != 0:
            return False
        # check direction
        if self.lastPosition is None:
            return True
        return self.lastPosition.getDirection(position) == direction

    def play(self, player, position, direction):
        if not self.isValid(position, direction):
            return False
        if self.board[position.x][position.y] > 0:
            raise ValueError(
                f"Board:\n{self}\nPosition is {position} already occupied."
            )
        if self.board[position.x][position.y] == -1:
            raise ValueError(f"Position {position} is invalid.")

        self.board[position.x][position.y] = (player - 1) * 3 + direction
        self.lastPosition = position
        self.player = 3 - self.player
        return True

    def getHumanInputAndPlay(self):
        while True:
            try:
                print(self)
                position = Position(*map(int, input("Position: ").split()))
                direction = int(input("Direction: "))
                done = self.play(self.player, position, direction)
                while not done:
                    print("Invalid move, please try again.")
                    position = Position(*map(int, input("Position: ").split()))
                    direction = int(input("Direction: "))
                    done = self.play(self.player, position, direction)
                break
            except ValueError as e:
                print(e)
                print("Please try again.")

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
                    word = ". "
                elif self.board[x][y] % 3 == 1 % 3:
                    word = "/ "
                elif self.board[x][y] % 3 == 2 % 3:
                    word = "--"
                elif self.board[x][y] % 3 == 3 % 3:
                    word = "\ "

                if self.board[x][y] == 0:
                    backgroundColor = None
                elif self.board[x][y] <= 3:
                    backgroundColor = 196
                else:
                    backgroundColor = 33

                result += outputHelper.colorize(word, backgroundColor=backgroundColor)
                result += "  "
            result += "\n"
        return result


if __name__ == "__main__":
    b = Board(5)
    b.board[0][4] = 1  # player 1, direction 1
    b.board[4][6] = 5  # player 2, direction 2
    b.board[6][5] = 3  # player 1, direction 3
    # the moves are not valid, but it's just for testing
    print(b)
    b = Board(5)
    while True:
        b.getHumanInputAndPlay()
