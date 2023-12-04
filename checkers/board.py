import pygame

from checkers.constants import BLACK, WHITE, BOARDDARK, BOARDLIGHT, ROWS, COLS, SQUARE_SIZE
from checkers.piece import Piece


class Board():
    def __init__(self, win: pygame.Surface) -> None:
        self.win: pygame.Surface = win
        self.board: list[list[Piece]] = []
        self.create_board()
        self.whiteKings: int = 0
        self.blackKings: int = 0
        self.whitePieces: int = 12
        self.blackPieces: int = 12

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(0)

                # if col % 2 == ((row + 1) % 2):
                #     if row < 3:
                #         self.board[row].append(
                #             Piece(self.win, row, col, BLACK))
                #     elif row > 4:
                #         self.board[row].append(
                #             Piece(self.win, row, col, WHITE))
                #     else:
                #         self.board[row].append(0)
                # else:
                #     self.board[row].append(0)

        # self.board[5][4] = Piece(self.win, 5, 4, BLACK)
        # self.board[3][6] = Piece(self.win, 3, 6, BLACK)
        # self.board[1][4] = Piece(self.win, 1, 4, BLACK)
        # self.board[5][2] = Piece(self.win, 5, 2, BLACK)
        # self.board[3][2] = Piece(self.win, 3, 2, BLACK)
        self.board[1][2] = Piece(self.win, 1, 2, BLACK)
        self.board[0][3] = Piece(self.win, 0, 3, WHITE)
        self.board[0][3].makeKing()

    def move(self, piece: Piece, row: int, col: int):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.makeKing()
            if piece.color == WHITE:
                self.whiteKings += 1
            else:
                self.blackKings += 1

    def getPiece(self, row: int, col: int) -> Piece or int:
        return self.board[row][col]

    def getValidMoves(self, piece: Piece) -> dict:
        moves: dict = {}
        row = piece.row
        left = piece.col - 1
        right = piece.col + 1

        if piece.color == WHITE or piece.isKing:

            moves.update(self.traverseLeft(
                row - 1, max(row-3, -1), -1, piece.color, left))
            moves.update(self.traverseRight(
                row - 1, max(row-3, -1), -1, piece.color, right))

        if piece.color == BLACK or piece.isKing:
            moves.update(self.traverseLeft(
                row + 1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self.traverseRight(
                row + 1, min(row+3, ROWS), 1, piece.color, right))

        # If any move captures then remove all the ones that don't.
        return self.filterMovesIfCaptureAvailable(moves)

    def traverseLeft(self, start: int, stop: int, step: int, color: tuple, left: int, captured=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.getPiece(r, left)
            print(f"Current: {current}")
            print(f"Last: {[print(element) for element in last]}")
            print(f"Captured: {[print(element) for element in captured]}")
            print("\n\n")
            if current == 0:
                if captured and not last:
                    break
                elif captured:
                    moves[(r, left)] = last + captured
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self.traverseLeft(
                        r+step, row, step, color, left - 1, captured=last))
                    moves.update(self.traverseRight(
                        r+step, row, step, color, left + 1, captured=last))

                break
            elif current.color == color:
                break

            else:
                last = [current]
            left -= 1

        return moves

    def traverseRight(self, start: int, stop: int, step: int, color: tuple, right: int, captured=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.getPiece(r, right)
            print(f"Current: {current}")
            print(f"Last: {[print(element) for element in last]}")
            print(f"Captured: {[print(element) for element in captured]}")
            print("\n\n")

            if current == 0:
                if captured and not last:
                    break
                elif captured:
                    moves[(r, right)] = last + captured
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self.traverseLeft(
                        r+step, row, step, color, right - 1, captured=last))
                    moves.update(self.traverseRight(
                        r+step, row, step, color, right + 1, captured=last))
                break
            elif current.color == color:
                break

            else:
                last = [current]
            right += 1

        return moves

    def filterMovesIfCaptureAvailable(self, moves):
        # Check if any list in the dictionary has items
        if any(moves[key] for key in moves):
            # Keep only those key-value pairs where the list is not empty
            return {key: value for key, value in moves.items() if value}
        else:
            # If no list has items, return the original dictionary
            return moves

    def draw(self):
        self.draw_squares()
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw()

    def draw_squares(self):
        self.win.fill(BOARDDARK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(self.win, BOARDLIGHT, (row*SQUARE_SIZE,
                                 col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
