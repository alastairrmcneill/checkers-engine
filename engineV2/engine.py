from checkers.game import Game
from checkers.board import Board
from checkers.piece import Piece
from checkers.constants import WHITE, BLACK, ROWS, COLS

from copy import deepcopy

# Engine V2 - improved evaluation


class EngineV2:
    def __init__(self):
        self.whiteMultiplier = [[0, 1, 0, 1, 0, 1, 0, 0.75],
                                [0.75, 0, 1, 0, 1, 0, 1, 0],
                                [0, 1, 0, 1.3, 0, 1.2, 0, 0.75],
                                [0.75, 0, 1.2, 0, 1.3, 0, 1, 0],
                                [0, 1.3, 0, 1.2, 0, 1.2, 0, 0.75],
                                [0.75, 0, 1, 0, 1, 0, 1.3, 0],
                                [0, 1, 0, 1, 0, 1, 0, 0.75],
                                [0.75, 0, 1.1, 0, 1.1, 0, 1.1, 0]]

        self.blackMultiplier = [[0, 1.1, 0, 1.1, 0, 1.1, 0, 0.75],
                                [0.75, 0, 1, 0, 1, 0, 1, 0],
                                [0, 1, 0, 1.3, 0, 1.2, 0, 0.75],
                                [0.75, 0, 1.2, 0, 1.3, 0, 1, 0],
                                [0, 1.3, 0, 1.2, 0, 1.2, 0, 0.75],
                                [0.75, 0, 1, 0, 1, 0, 1.3, 0],
                                [0, 1, 0, 1, 0, 1, 0, 0.75],
                                [0.75, 0, 1, 0, 1, 0, 1, 0]]

    def minimax(self, gameState: Game, board: Board, maximizeAI: bool, depth: int):
        result = board.isWinner()

        if depth == 0 or result != None:
            if result == BLACK:
                return 100, board
            elif result == WHITE:
                return -100, board
            elif result == "Draw":
                # A draw is only good if you are losing. If you are winning you shouldn't be satisfied with a draw
                if maximizeAI and self.evaluteBoard(board) > 0:
                    return -1, board
                elif not maximizeAI and self.evaluteBoard(board) < 0:
                    return 1, board
                else:
                    return 0, board

            return self.evaluteBoard(board), board

        if maximizeAI:
            maxEval = float('-inf')
            bestMove = None
            for move in self.getAllMoves(gameState, board, BLACK):
                evaluation = self.minimax(gameState, move, False, depth-1)[0]
                maxEval = max(maxEval, evaluation)
                if maxEval == evaluation:
                    bestMove = move

            return maxEval, bestMove
        else:
            minEval = float('inf')
            bestMove = None
            for move in self.getAllMoves(gameState, board, WHITE):
                evaluation = self.minimax(gameState, move, True, depth-1)[0]
                minEval = min(minEval, evaluation)
                if minEval == evaluation:
                    bestMove = move

            return minEval, bestMove

    def getAllMoves(self, gameState: Game, board: Board, player: tuple):
        moves = []
        # need to get the valid moves from the temp board not the game state
        validMoves = board.getValidMoves(player)
        for pieceMove in validMoves:
            piece = pieceMove["piece"]
            for possibleMove in pieceMove["moves"]:
                temp_board = deepcopy(board)
                temp_piece = temp_board.getPiece(piece.row, piece.col)
                new_board = self.simulateMove(
                    temp_board, temp_piece, possibleMove["position"], possibleMove["captures"])
                moves.append(new_board)
        return moves

    def simulateMove(self, tempBoard: Board, tempPiece: Piece, move: tuple, captures: list[Piece]):
        tempBoard.move(tempPiece, move[0], move[1], captures)
        return tempBoard

    def evaluteBoard(self, tempBoard: Board) -> int:
        eval = 0
        for i in range(ROWS):
            for j in range(COLS):
                piece = tempBoard.getPiece(i, j)
                if piece != 0:

                    if piece.color == WHITE:
                        pieceScore = self.whiteMultiplier[i][j]
                        if piece.isKing:
                            eval -= 3*pieceScore
                        else:
                            eval -= pieceScore
                    elif piece.color == BLACK:
                        pieceScore = self.blackMultiplier[i][j]
                        if piece.isKing:
                            eval += 3*pieceScore
                        else:
                            eval += pieceScore

        return eval
