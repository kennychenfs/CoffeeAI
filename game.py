from enum import Enum
from typing import Tuple, Optional


class Direction(Enum):
    DOWN_LEFT = 1
    RIGHT = 2
    DOWN_RIGHT = 3


class OutputHelper:
    BACKGROUND = "\x1b[48;5;"
    WORD = "\x1b[38;5;"
    END = "m"
    RESET = "\x1b[0m"

    @staticmethod
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
        if other is None:
            return False
        return self.x == other.x and self.y == other.y

    def getDirection(self, other):
        if self == other:
            raise ValueError("Cannot get direction of same position")
        array = other - self
        if array.x != 0 and array.y == 0:
            return Direction(1)
        elif array.x == 0 and array.y != 0:
            return Direction(2)
        elif array.x == array.y:
            return Direction(3)
        else:
            raise ValueError(
                f"The two positions are not in the same line:{self} and {other}"
            )

    def __str__(self):
        return f"({self.x}, {self.y})"


class HexBoard:
    def __init__(self, size, winLen, board=None, initialPlayer=1):
        self.size = size  # length of each side of the board
        self.winLen = winLen  # number of pieces in a row to win
        self.board = board or self.createBoard()
        # board slot value:
        # -1: invalid position
        # 0: empty
        # 1: player 1
        # 2: player 2
        self.player = initialPlayer
        self.lastPosition = None
        self.lastDirection = None
        self.result = None

    def createBoard(self):
        # Create a hex board in axial coordinates, marked with -1 if it's not a valid position.
        board = [[0] * (self.size * 2 - 1) for _ in range(self.size * 2 - 1)]
        for x in range(self.size * 2 - 1):
            for y in range(self.size * 2 - 1):
                if y - x >= self.size or x - y >= self.size:
                    board[x][y] = -1
        return board

    def isValid(
        self, position: Position, direction: Direction
    ) -> Tuple[bool, Optional[str]]:
        # Check if a move is valid.
        # Check position
        if not (
            0 <= position.x < self.size * 2 - 1 and 0 <= position.y < self.size * 2 - 1
        ):
            return False, f"Position {position} out of range of board"
        if self.board[position.x][position.y] == -1:
            return False, f"Position {position} out of range of board"
        if self.board[position.x][position.y] > 0:
            return False, f"Position {position} occupied"
        if not self.isThereNextMove(position):
            return (
                False,
                f"Position {position} is illegal because the next player has no free spaces available.",
            )
        # Check if the position fits lastDirection
        if (
            self.lastPosition is not None
            and self.lastPosition.getDirection(position) != self.lastDirection
        ):
            return False, "Move is not in the given direction"
        return True, None

    def play(self, player: int, position: Position, direction: Direction):
        if player != self.player:
            raise ValueError(f"Player {player} is not the current player")
        valid, errorMessage = self.isValid(position, direction.value)
        if not valid:
            raise ValueError(errorMessage)
        self.board[position.x][position.y] = player
        self.lastPosition = position
        self.lastDirection = direction.value
        self.player = 3 - self.player

    def getHumanInputAndPlay(self):
        while True:
            try:
                print(self)
                x, y, d = map(int, input("Position and direction(x y d): ").split())
                position = Position(x, y)
                direction = Direction(d)
                self.play(self.player, position, direction)
                break
            except ValueError as e:
                print(e)
                print("Please try again.")
        if self.isTerminal():
            print(f"Player {self.result} wins!")

    def isThereNextMove(self, position: Position):
        # Check if the next player has no free spaces available.
        if self.lastDirection is None:
            return False
        freeSpace = self.findFreeSpace(
            position, self.lastDirection, returnPositions=True
        )
        if len(freeSpace) >= 2:
            return True
        if len(freeSpace) == 1:
            position = freeSpace[0]
            for d in Direction:
                if self.findFreeSpace(position, d):
                    return True
        return False

    def findFreeSpace(self, position, direction, returnPositions=False):
        result = []
        if direction == Direction.DOWN_LEFT:
            for x in range(
                max(0, position.y - (self.size - 1)),
                min(self.size * 2 - 1, position.y + self.size),
            ):
                if self.board[x][position.y] == 0:
                    if returnPositions:
                        result.append(Position(x, position.y))
                    else:
                        return True
        elif direction == Direction.RIGHT:
            for y in range(
                max(0, position.x - (self.size - 1)),
                min(self.size * 2 - 1, position.x + self.size),
            ):
                if self.board[position.x][y] == 0:
                    if returnPositions:
                        result.append(Position(position.x, y))
                    else:
                        return True
        elif direction == Direction.DOWN_RIGHT:
            # in direction (1,1)
            x = position.x
            y = position.y
            _min = min(x, y)
            x -= _min
            y -= _min
            for i in range(self.size * 2 - 1):
                if x >= self.size * 2 - 1 or y >= self.size * 2 - 1:
                    break
                if self.board[x][y] == 0:
                    if returnPositions:
                        result.append(Position(x, y))
                    else:
                        return True
                x += 1
                y += 1
        if returnPositions:
            return result
        else:
            return False

    def isTerminal(self):
        if self.lastPosition is None:
            return False
        if self.isWinByLine():
            # The last player wins
            self.result = 3 - self.player
            return True
        # if the current player cannot move, the other player wins
        for x in range(self.size * 2 - 1):
            if self.board[x][self.lastPosition.y] == 0:
                return False
        for y in range(self.size * 2 - 1):
            if self.board[self.lastPosition.x][y] == 0:
                return False
        x = self.lastPosition.x
        y = self.lastPosition.y
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
                    word = " /-\\"[self.lastDirection.value]
                backgroundColor = [None, 196, 33][self.board[x][y]]

                result += OutputHelper.colorize(word, backgroundColor=backgroundColor)
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
