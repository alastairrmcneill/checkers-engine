import pygame

from checkers.constants import BLACK, WHITE, BOARDDARK, BOARDLIGHT, ROWS, COLS, SQUARE_SIZE
from checkers.piece import Piece


class Board():
    def __init__(self) -> None:
        self.board: list[Piece] = []
        self.create_board()
        self.history: list[list[Piece]] = []
        self.whiteKings: int = 0
        self.blackKings: int = 0
        self.whitePieces: int = 12
        self.blackPieces: int = 12

    def create_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                # self.board[row].append(0)  # comment out
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board.append(
                            Piece(row, col, BLACK))
                    elif row > 4:
                        self.board.append(
                            Piece(row, col, WHITE))
                    else:
                        self.board.append(0)

    def convertBoardToList(self):
        convertedBoard = []

        for piece in self.board:
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
        currentPieceIndex = self.getIndexFromRowCol(piece.row, piece.col)
        futurePieceIndex = self.getIndexFromRowCol(row, col)

        self.board[currentPieceIndex], self.board[futurePieceIndex] = self.board[futurePieceIndex], self.board[currentPieceIndex]

        self.addToHistory()
        self.isWinner()
        piece.move(row, col)
        for capturedPiece in captures:
            capturedIndex = self.getIndexFromRowCol(
                capturedPiece.row, capturedPiece.col)
            self.board[capturedIndex] = 0
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

    def aiMove(self, board: list):
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

    def getIndexFromRowCol(self, row: int, col: int) -> Piece or int:
        pos = (row, col)
        squares = {
            (0,	1):	0,
            (0,	3):	1,
            (0,	5):	2,
            (0,	7):	3,
            (1,	0):	4,
            (1,	2):	5,
            (1,	4):	6,
            (1,	6):	7,
            (2,	1):	8,
            (2,	3):	9,
            (2,	5):	10,
            (2,	7):	11,
            (3,	0):	12,
            (3,	2):	13,
            (3,	4):	14,
            (3,	6):	15,
            (4,	1):	16,
            (4,	3):	17,
            (4,	5):	18,
            (4,	7):	19,
            (5,	0):	20,
            (5,	2):	21,
            (5,	4):	22,
            (5,	6):	23,
            (6,	1):	24,
            (6,	3):	25,
            (6,	5):	26,
            (6,	7):	27,
            (7,	0):	28,
            (7,	2):	29,
            (7,	4):	30,
            (7,	6):	31, }

        return squares[pos]

    def getPiece(self, row: int, col: int) -> Piece or int:
        try:
            index = self.getIndexFromRowCol(row, col)
            return self.board[index]
        except:
            return None

    def getValidMoves(self, color: tuple) -> list:
        pseudoValidMoves = []

        # Loop through all pieces
        for piece in self.board:
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
        for piece in self.board:
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
        for piece in self.board:
            pieceHash = hash(piece) if piece != 0 else -1
            board_state.append(pieceHash)
        return hash(tuple(board_state))

    def __str__(self) -> str:
        returnString = f""
        for piece in self.board:
            returnString += f"{piece}"

        return returnString
