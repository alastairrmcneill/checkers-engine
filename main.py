import pygame

from checkers.constants import WIN_HEIGHT, WIN_WIDTH, SQUARE_SIZE, BLACK, WHITE
from checkers.game import Game
from engineV1.engine import EngineV1
from engineV2.engine import EngineV2
from engineV3.engine import EngineV3
from engineV4.engine import EngineV4
from engineV5.engine import EngineV5

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Checkers")


def get_row_col(pos):
    row = pos[1] // SQUARE_SIZE
    col = pos[0] // SQUARE_SIZE

    return (row, col)


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    engine1 = EngineV1()
    engine2 = EngineV2()
    engine3 = EngineV3()
    engine4 = EngineV4()
    engine5 = EngineV5()

    while run:
        clock.tick(30)

        if (game.isWinner() != None):
            print("Game is over")
            print(f"{game.isWinner()} won")
            run = False
            pygame.quit()
            quit()

        if game.turn == WHITE:
            # value, new_board, totalEvals = engine1.minimax(
            #     game, game.board, True, 3)
            value, new_board, totalEvals = engine3.minimax(
                game, game.board, False, 4, float('-inf'), float('inf'), 0)
            game.aiMove(new_board)
            print(f"V3 Board Eval: {value}")
            print(f"V3 boards evaluated: {totalEvals}")
            print(f"Moves since capture: {game.board.check40MoveRule()[1]}")
            game.draw()
            pygame.time.delay(200)

        if game.turn == BLACK:
            value, new_board, totalEvals = engine5.findBestMove(
                game, game.board, True)
            game.aiMove(new_board)
            print(f"V5 Boards evaluated: {totalEvals}")
            print(f"V5 Board Eval: {value}")
            print(f"Moves since capture: {game.board.check40MoveRule()[1]}")
            game.draw()
            pygame.time.delay(200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_row_col(pygame.mouse.get_pos())
                game.select(row, col)

        game.draw()

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
