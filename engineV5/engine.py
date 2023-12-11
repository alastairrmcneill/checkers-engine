from checkers.game import Game
from checkers.board import Board
from checkers.piece import Piece
from checkers.constants import WHITE, BLACK, ROWS, COLS

from copy import deepcopy

# Engine V5 - Implement transposition tables


class EngineV5:
    def __init__(self):
        self.whiteMultiplier = [1, 1, 1, 0.75,
                                0.75, 1, 1, 1,
                                1, 1.3, 1.2, 0.75,
                                0.75, 1.2, 1.3, 1,
                                1.3, 1.2, 1.2, 0.75,
                                0.75, 1, 1, 1.3,
                                1, 1, 1, 0.75,
                                0.75, 1.1, 1.1, 1.1]

        self.blackMultiplier = [1.1, 1.1, 1.1, 0.75,
                                0.75, 1, 1, 1,
                                1, 1.3, 1.2, 0.75,
                                0.75, 1.2, 1.3, 1,
                                1.3, 1.2, 1.2, 0.75,
                                0.75, 1, 1, 1.3,
                                1, 1, 1, 0.75,
                                0.75, 1, 1, 1]

        self.transpositionTable = {}

    def findBestMove(self, gameState: Game, board: Board, maximizeAI: bool):
        self.transpositionTable = {}

        eval, bestMove, totalEvals = self.minimax(
            gameState, board, maximizeAI, 5, float('-inf'), float('inf'), 0)
        print(f"V5 Boards evaluated: {totalEvals}")
        print(f"V5 Board Eval: {eval}")
        return eval, bestMove, totalEvals

    def minimax(self, gameState: Game, board: Board, maximizeAI: bool, depth: int, alpha: float, beta: float, totalEvals: int):
        boardHash = hash(board)

        if boardHash in self.transpositionTable:
            return self.transpositionTable[boardHash], board, totalEvals + 1

        result = board.isWinner()

        if depth == 0 or result != None:
            if result == BLACK:
                self.transpositionTable[boardHash] = 100
                return 100, board, totalEvals + 1
            elif result == WHITE:
                self.transpositionTable[boardHash] = -100
                return -100, board, totalEvals + 1
            elif result == "Draw":
                # A draw is only good if you are losing. If you are winning you shouldn't be satisfied with a draw
                if maximizeAI and self.evaluteBoard(board) > 0:
                    self.transpositionTable[boardHash] = -1
                    return -1, board, totalEvals + 1
                elif not maximizeAI and self.evaluteBoard(board) < 0:
                    self.transpositionTable[boardHash] = 1
                    return 1, board, totalEvals + 1
                else:
                    self.transpositionTable[boardHash] = 0
                    return 0, board, totalEvals + 1

            eval = self.evaluteBoard(board)
            self.transpositionTable[boardHash] = eval

            return eval, board, totalEvals + 1

        if maximizeAI:
            maxEval = float('-inf')
            bestMove = None
            for move in reversed(self.getAllMoves(gameState, board, BLACK)):
                evaluation, board, totalEvals = self.minimax(
                    gameState, move, False, depth-1, alpha, beta, totalEvals)
                maxEval = max(maxEval, evaluation)
                if maxEval == evaluation:
                    bestMove = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break

            self.transpositionTable[boardHash] = maxEval
            return maxEval, bestMove, totalEvals
        else:
            minEval = float('inf')
            bestMove = None
            for move in self.getAllMoves(gameState, board, WHITE):
                evaluation, board, totalEvals = self.minimax(
                    gameState, move, True, depth-1, alpha, beta,  totalEvals)
                minEval = min(minEval, evaluation)
                if minEval == evaluation:
                    bestMove = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break

            self.transpositionTable[boardHash] = minEval
            return minEval, bestMove, totalEvals

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
        for i, piece in enumerate(tempBoard.board):
            if piece != 0:
                if piece.color == WHITE:
                    pieceScore = self.whiteMultiplier[i]
                    if piece.isKing:
                        eval -= 3*pieceScore
                    else:
                        eval -= pieceScore
                elif piece.color == BLACK:
                    pieceScore = self.blackMultiplier[i]
                    if piece.isKing:
                        eval += 3*pieceScore
                    else:
                        eval += pieceScore

        return eval
