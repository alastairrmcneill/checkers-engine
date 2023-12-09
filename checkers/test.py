
class Piece():

    def __init__(self, row: int, col: int, color: tuple) -> None:
        self.row: int = row
        self.col: int = col
        self.color: tuple = color
        self.isKing: bool = False

    def makeKing(self):
        self.isKing = True

    def __hash__(self) -> int:
        return hash((self.color, self.isKing, self.row, self.col))

    def __str__(self) -> str:
        if self.color == (255, 255, 255):
            color = "White"
        else:
            color = "Black"
        return f"Color: {color}, Row: {self.row}, Col: {self.col}"


piece1 = Piece(0, 0, (255, 255, 255))
piece2 = Piece(0, 1, (255, 255, 255))
piece3 = Piece(1, 0, (0, 0, 0))
piece4 = Piece(1, 1, (0, 0, 0))
piece4.makeKing()

hash1 = hash(piece1)
hash2 = hash(piece2)
hash3 = hash(piece3)
hash4 = hash(piece4)

print(f"Hash1: {hash1}")
print(f"Hash2: {hash2}")
print(f"Hash3: {hash3}")
print(f"Hash4: {hash4}")


def hash_board(board):
    board_state = []
    for row in board:
        row_state = []
        for square in row:
            square_hash = hash(square) if square != 0 else -1
            row_state.append(square_hash)
        board_state.append(tuple(row_state))
    return hash(tuple(board_state))


board1 = [[piece1, 0], [piece3, piece4]]
boardHash1 = hash_board(board1)
print(f"Board Hash 1: {boardHash1}")

piece1.col = 1

board2 = [[0, piece1], [piece3, piece4]]
boardHash2 = hash_board(board2)
print(f"Board Hash 2: {boardHash2}")


class Board():
    def __init__(self) -> None:
        self.board: list[list[Piece]] = []
        self.create_board()
        self.history: list[list[list[Piece]]] = []
        self.whiteKings: int = 0
        self.blackKings: int = 0
        self.whitePieces: int = 12
        self.blackPieces: int = 12

    def create_board(self):
        for row in range(8):
            self.board.append([])
            for col in range(8):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(
                            Piece(row, col, (0, 0, 0)))
                    elif row > 4:
                        self.board[row].append(
                            Piece(row, col, (255, 255, 255)))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def __hash__(self):
        board_state = []
        for row in self.board:
            row_state = []
            for square in row:
                square_hash = hash(square) if square != 0 else -1
                row_state.append(square_hash)
            board_state.append(tuple(row_state))
        return hash(tuple(board_state))

    def __str__(self) -> str:
        return f"""Black Pieces: {self.blackPieces},White Pieces: {self.whitePieces}"""


board3 = Board()
board4 = Board()
board3.board[0][1] = 0
board3.board[4][4] = Piece(4, 4, (0, 0, 0))

boardHash3 = hash(board3)
boardHash4 = hash(board4)


print(f"Board Hash 3: {boardHash3}")
print(f"Board Hash 4: {boardHash4}")
