"""
Snake game v2
"""

import pygame as p

from pygame.constants import *

from time import sleep

from globals import *
from snake import Snake
from food import Food


def message(text, colour, screen, font_style):
    """Display a message in the middle of the screen"""
    m = font_style.render(text, True, colour)
    text_rect = m.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2))
    screen.blit(m, text_rect)


def display_score(text, colour, screen):
    """Display score in top left corner."""
    font_style = p.font.SysFont('Arial', 20)
    m = font_style.render(text, True, colour)
    screen.blit(m, (10, 10))


def main():
    """Main loop of the game."""
    p.init()
    screen = p.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    p.display.update()
    p.display.set_caption('Snake')
    p.font.init()
    clock = p.time.Clock()
    font_style = p.font.SysFont('Arial', 50)

    score = 0

    # initialise snake object.
    snake = Snake()
    snake.colour = GREEN
    snake.pos_x, snake.pos_y = DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2

    food = Food()

    game_over = False
    game_running = False
    while not game_over:

        delta_time = clock.tick(60)  # fps
        step = delta_time / 1000  # / 1000 because unit of velocity is seconds

        for event in p.event.get():
            if event.type == p.QUIT:  # quit when the X is clicked.
                game_over = True

            if event.type == p.KEYDOWN:
                if p.key.get_pressed()[K_LEFT]:
                    snake.change_direction('left')
                elif p.key.get_pressed()[K_RIGHT]:
                    snake.change_direction('right')
                elif p.key.get_pressed()[K_UP]:
                    snake.change_direction('up')
                elif p.key.get_pressed()[K_DOWN]:
                    snake.change_direction('down')
                elif p.key.get_pressed()[K_SPACE]:
                    game_running = True

        if not game_running:
            message("GAME PAUSED - PRESS SPACE", WHITE, screen, font_style)
        else:
            screen.fill(BLACK)

            food.update(screen)

            snake.move(step)  # tell the snake to continue to move.
            snake.update(screen)  # update the snake information.

            if snake.eat(food):
                # increase score
                score += 10
                food = Food()  # create new food object.

            if snake.is_dead():  # check if the snake has crossed itself or left the screen.
                game_over = True

            # display score
            display_score(f"Score: {score}", WHITE, screen)

        # p.display.update()
        p.display.flip()  # use flip instead to update whole screen

    message("GAME OVER", RED, screen, font_style)
    p.display.update()
    sleep(1)

    p.quit()
    #quit()


if __name__ == "__main__":
    main()
