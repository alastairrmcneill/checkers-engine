from checkers.game import Game
from checkers.board import Board
from checkers.piece import Piece
from checkers.constants import WHITE, BLACK, ROWS, COLS

from copy import deepcopy
from datetime import datetime, timedelta

# Engine V6 - Implement time based searching


class EngineV7:
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

        self.transpositionTable = {}
        self.endTime = datetime.now()

    def findBestMove(self, gameState: Game, board: Board, maximizeAI: bool):
        self.transpositionTable = {}
        timeLimit = 3
        self.endTime = datetime.now() + timedelta(0, timeLimit)

        eval, bestMove, totalEvals = self.iterativeDeepening(
            gameState, board, maximizeAI)

        print(f"V7 Boards evaluated: {totalEvals}")
        print(f"V7 Board Eval: {eval}")
        return eval, bestMove, totalEvals

    def iterativeDeepening(self, gameState: Game, board: Board, maximizeAI: bool):
        depth = 1
        totalEvals = 0
        while not self.timeIsUp():
            eval, bestMove, totalEvals = self.minimax(
                gameState, board, maximizeAI, depth, float('-inf'), float('inf'), totalEvals)
            depth += 1

        return eval, bestMove, totalEvals

    def minimax(self, gameState: Game, board: Board, maximizeAI: bool, depth: int, alpha: float, beta: float, totalEvals: int):
        boardHash = hash(board)

        if boardHash in self.transpositionTable and self.transpositionTable[boardHash]["depth"] >= depth:
            return self.transpositionTable[boardHash]["eval"], board, totalEvals + 1

        result = board.isWinner()

        if depth == 0 or result != None:
            if result == BLACK:
                self.transpositionTable[boardHash] = {
                    "eval": 100, "depth": depth, "bestMove": board}
                return 100, board, totalEvals + 1
            elif result == WHITE:
                self.transpositionTable[boardHash] = {
                    "eval": -100, "depth": depth, "bestMove": board}
                return -100, board, totalEvals + 1
            elif result == "Draw":
                # A draw is only good if you are losing. If you are winning you shouldn't be satisfied with a draw
                if maximizeAI and self.evaluteBoard(board) > 0:
                    self.transpositionTable[boardHash] = {
                        "eval": -1, "depth": depth, "bestMove": board}
                    return -1, board, totalEvals + 1
                elif not maximizeAI and self.evaluteBoard(board) < 0:
                    self.transpositionTable[boardHash] = {
                        "eval": 1, "depth": depth, "bestMove": board}
                    return 1, board, totalEvals + 1
                else:
                    self.transpositionTable[boardHash] = {
                        "eval": 0, "depth": depth, "bestMove": board}
                    return 0, board, totalEvals + 1

            eval = self.evaluteBoard(board)
            self.transpositionTable[boardHash] = {
                "eval": eval, "depth": depth, "bestMove": board}

            return eval, board, totalEvals + 1

        if self.timeIsUp():
            eval = self.evaluteBoard(board)
            self.transpositionTable[boardHash] = {
                "eval": eval, "depth": depth, "bestMove": board}

            return eval, board, totalEvals + 1

        if maximizeAI:
            maxEval = float('-inf')
            bestMove = None
            movesList = self.getAllMoves(gameState, board, BLACK)

            if boardHash in self.transpositionTable and self.transpositionTable[boardHash]['bestMove'] in movesList:
                # Move the best move to the front of the move list
                movesList.remove(
                    self.transpositionTable[boardHash]['bestMove'])
                movesList.insert(
                    0, self.transpositionTable[boardHash]['bestMove'])

            for move in reversed(movesList):
                evaluation, board, totalEvals = self.minimax(
                    gameState, move, False, depth-1, alpha, beta, totalEvals)
                maxEval = max(maxEval, evaluation)
                if maxEval == evaluation:
                    bestMove = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break

            self.transpositionTable[boardHash] = {
                "eval": maxEval, "depth": depth, "bestMove": bestMove}
            return maxEval, bestMove, totalEvals
        else:
            minEval = float('inf')
            bestMove = None
            movesList = self.getAllMoves(gameState, board, WHITE)

            if boardHash in self.transpositionTable and self.transpositionTable[boardHash]['bestMove'] in movesList:
                # Move the best move to the front of the move list
                movesList.remove(
                    self.transpositionTable[boardHash]['bestMove'])
                movesList.insert(
                    0, self.transpositionTable[boardHash]['bestMove'])

            for move in movesList:
                evaluation, board, totalEvals = self.minimax(
                    gameState, move, True, depth-1, alpha, beta,  totalEvals)
                minEval = min(minEval, evaluation)
                if minEval == evaluation:
                    bestMove = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break

            self.transpositionTable[boardHash] = {
                "eval": minEval, "depth": depth, "bestMove": bestMove}
            return minEval, bestMove, totalEvals

    def timeIsUp(self):
        currentTime = datetime.now()
        return currentTime > self.endTime

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
