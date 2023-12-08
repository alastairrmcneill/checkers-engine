import pygame

from checkers.constants import WIN_HEIGHT, WIN_WIDTH, SQUARE_SIZE, BLACK, WHITE
from checkers.game import Game
from engine.engine import Engine

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
    engine1 = Engine()
    engine2 = Engine()

    while run:
        clock.tick(30)

        if (game.isWinner() != None):
            print("Game is over")
            print(f"{game.isWinner()} won")
            run = False
            pygame.quit()
            quit()

        if game.turn == WHITE:
            value, new_board = engine1.minimax(game, game.board, False, 4)
            game.aiMove(new_board)
            print(f"Num since last capture: {game.board.check40MoveRule()[1]}")
            game.draw()
            pygame.time.delay(200)

        if game.turn == BLACK:
            value, new_board = engine2.minimax(game, game.board, True, 4)
            game.aiMove(new_board)
            print(f"Num since last capture: {game.board.check40MoveRule()[1]}")
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
