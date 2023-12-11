import pygame

from checkers.constants import BLACK, WHITE, BOARDDARK, BOARDLIGHT, ROWS, COLS, SQUARE_SIZE
from checkers.piece import Piece


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
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                # self.board[row].append(0)  # comment out
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(
                            Piece(row, col, BLACK))
                    elif row > 4:
                        self.board[row].append(
                            Piece(row, col, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

        # self.board[0][1] = Piece(0, 1, BLACK)
        # self.board[0][3] = Piece(0, 3, BLACK)
        # self.board[0][5] = Piece(0, 5, BLACK)
        # self.board[1][6] = Piece(1, 6, BLACK)
        # self.board[4][7] = Piece(4, 7, BLACK)
        # self.board[5][0] = Piece(5, 0, BLACK)

        # self.board[5][4] = Piece(5, 4, WHITE)
        # self.board[6][5] = Piece(6, 5, WHITE)
        # self.board[7][0] = Piece(7, 0, WHITE)
        # self.board[7][6] = Piece(7, 4, WHITE)
        # self.board[7][6] = Piece(7, 6, WHITE)

    def convertBoardToList(self):
        convertedBoard = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.getPiece(row, col)
                if piece == 0:
                    convertedBoard.append(0)
                elif piece.color == WHITE:
                    if piece.isKing:
                        convertedBoard.append(10)
                    convertedBoard.append(1)
                elif piece.color == BLACK:
                    convertedBoard.append(2)
                    if piece.isKing:
                        convertedBoard.append(20)

        return convertedBoard

    def move(self, piece: Piece, row: int, col: int, captures: list[Piece]):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        self.addToHistory()
        self.isWinner()
        piece.move(row, col)
        for capturedPiece in captures:
            self.board[capturedPiece.row][capturedPiece.col] = 0
            if capturedPiece != 0:
                if capturedPiece.color == BLACK:
                    self.blackPieces -= 1
                else:
                    self.whitePieces -= 1
        if (row == ROWS - 1) or (row == 0):
            if not piece.isKing:
                piece.makeKing()
                if piece.color == WHITE:
                    self.whiteKings += 1
                else:
                    self.blackKings += 1

    def aiMove(self, board: list[list[Piece]]):
        self.board = board
        self.addToHistory()

    def addToHistory(self):
        self.history.append(self.convertBoardToList())

    def checkThreePeat(self):
        if len(self.history) > 0:
            target_sublist = self.history[-1]
            count = sum(sublist == target_sublist for sublist in self.history)
            if count >= 3:
                return True

        return False

        count = sum(sublist == target_sublist for sublist in data)

    def check40MoveRule(self):
        sums = [sum(lst) for lst in self.history]
        unique_sum_index = -1

        for i, current_sum in enumerate(sums):
            if all(current_sum != previous_sum for previous_sum in sums[:i]):
                unique_sum_index = i

        numberMovesSinceLastCapture = len(self.history) - unique_sum_index

        return numberMovesSinceLastCapture >= 40, numberMovesSinceLastCapture

    def isWinner(self):
        if self.blackPieces <= 0:
            return WHITE
        elif self.whitePieces <= 0:
            return BLACK

        if self.checkThreePeat() or self.check40MoveRule()[0]:
            print(f"3 Peat: {self.checkThreePeat()}")
            print(f"40 Moves: {self.check40MoveRule()}")
            return "Draw"

        return None

    def getPiece(self, row: int, col: int) -> Piece or int:
        return self.board[row][col]

    def getValidMoves(self, color: tuple) -> list:
        pseudoValidMoves = []

        # Loop through all pieces
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    # Append valid moves
                    pseudoValidMoves.append(
                        {"piece": piece, "moves": self.getPieceMoves(piece)})

        # If any move captures then remove all the ones that don't.
        pseudoValidMoves = self.filterMovesIfCaptureAvailable(pseudoValidMoves)

        # # Remove partial routes
        pseudoValidMoves = self.filterOutPartialMoves(pseudoValidMoves)

        moves = pseudoValidMoves
        return moves

    def getPieceMoves(self, piece: Piece) -> dict:
        moves = []
        row = piece.row
        left = piece.col - 1
        right = piece.col + 1

        if piece.color == WHITE or piece.isKing:

            moves.extend(self.traverseLeft(
                row - 1, max(row-3, -1), -1, piece.color, left))
            moves.extend(self.traverseRight(
                row - 1, max(row-3, -1), -1, piece.color, right))

        if piece.color == BLACK or piece.isKing:
            moves.extend(self.traverseLeft(
                row + 1, min(row+3, ROWS), 1, piece.color, left))
            moves.extend(self.traverseRight(
                row + 1, min(row+3, ROWS), 1, piece.color, right))

        return moves

    def traverseLeft(self, start: int, stop: int, step: int, color: tuple, left: int, captured=[], partialRoute=[]):
        moves = []
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.getPiece(r, left)
            # print(f"Looking at: ({r},{left})")
            # print(f"Current:")
            # print(current)
            # print("Last:")
            # for element in last:
            #     print(element)
            # print("Captured: ")
            # for element in captured:
            #     print(element)

            # print("\n-------------\n")
            if current == 0:
                if captured and not last:
                    break
                elif captured:
                    moves.append(
                        {"position": (r, left), "captures": captured + last, "partialRoute": partialRoute + [(r, left)]})
                else:
                    moves.append({"position": (r, left), "captures": last,
                                 "partialRoute": partialRoute + [(r, left)]})

                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.extend(self.traverseLeft(
                        r+step, row, step, color, left - 1, captured=captured + last, partialRoute=partialRoute + [(r, left)]))
                    moves.extend(self.traverseRight(
                        r+step, row, step, color, left + 1, captured=captured + last, partialRoute=partialRoute + [(r, left)]))

                break
            elif current.color == color:
                break

            else:
                last = [current]
            left -= 1

        return moves

    def traverseRight(self, start: int, stop: int, step: int, color: tuple, right: int, captured=[], partialRoute=[]):
        moves = []
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.getPiece(r, right)
            # print(f"Looking at: ({r},{right})")
            # print(f"Current:")
            # print(current)
            # print("Last:")
            # for element in last:
            #     print(element)
            # print("Captured: ")
            # for element in captured:
            #     print(element)

            # print("\n-------------\n")

            if current == 0:
                if captured and not last:
                    break
                elif captured:
                    moves.append(
                        {"position": (r, right), "captures": captured + last, "partialRoute": partialRoute + [(r, right)]})
                else:
                    moves.append({"position": (r, right), "captures": last,
                                 "partialRoute": partialRoute + [(r, right)]})

                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.extend(self.traverseLeft(
                        r+step, row, step, color, right - 1, captured=captured + last, partialRoute=partialRoute + [(r, right)]))
                    moves.extend(self.traverseRight(
                        r+step, row, step, color, right + 1, captured=captured + last, partialRoute=partialRoute + [(r, right)]))
                break
            elif current.color == color:
                break

            else:
                last = [current]
            right += 1

        return moves

    def filterMovesIfCaptureAvailable(self, moves):
        # Check if any move in any piece has at least one capture
        has_capture = any(
            any(len(move['captures']) > 0 for move in piece['moves']) for piece in moves)

        if has_capture:
            # Filter out pieces without captures in any of their moves and also remove moves without captures
            return [
                {
                    'piece': piece['piece'],
                    'moves': [move for move in piece['moves'] if len(move['captures']) > 0]
                }
                for piece in moves
                if any(len(move['captures']) > 0 for move in piece['moves'])
            ]
        return moves

    def filterOutPartialMoves(self, moves):
        def is_route_contained(route, other_routes):
            for other_route in other_routes:
                if route != other_route and all(point in other_route for point in route):
                    return True
            return False

        # Function to filter the moves based on 'partialRoute'

        def filter_moves(moves):
            for piece_data in moves:
                piece_data['moves'] = [move for move in piece_data['moves'] if not is_route_contained(
                    move['partialRoute'], [other_move['partialRoute'] for other_move in piece_data['moves']])]
            return moves

        # Applying the function to the data
        output = filter_moves(moves)
        return output

    def draw(self, win: pygame.Surface):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def draw_squares(self, win: pygame.Surface):
        win.fill(BOARDDARK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, BOARDLIGHT, (row*SQUARE_SIZE,
                                 col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

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
