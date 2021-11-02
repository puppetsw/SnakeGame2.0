"""
Snake class which will contain information about the snake!
"""
import pygame.draw
from globals import *


class Snake:

    def __init__(self):
        self.colour = (255, 255, 255)
        self.pos_x = 0  # set initial position
        self.pos_y = 0  # set initial position
        self.size = 20  # size of the snake on the screen.
        self.speed = 6
        self.speed_increment = 0.1
        self.length = 1
        self.body = []  # how many body of the snake to draw.
        self.snake_head = []  # current position of the head.
        self.direction = (self.size, 0)
        self.direction_text = 'right'

    def move(self, step):
        """Move the snake by it's size and the current direction."""
        self.pos_x += self.direction[0] * step * self.speed
        self.pos_y += self.direction[1] * step * self.speed

    def change_direction(self, direction: str):
        """Change the movement direction of the snake."""
        if direction == 'left' and self.direction_text != 'right':
            self.direction = -self.size, 0
            self.direction_text = 'left'
        elif direction == 'right' and self.direction_text != 'left':
            self.direction = self.size, 0
            self.direction_text = 'right'
        elif direction == 'up' and self.direction_text != 'down':
            self.direction = 0, -self.size
            self.direction_text = 'up'
        elif direction == 'down' and self.direction_text != 'up':
            self.direction = 0, self.size
            self.direction_text = 'down'

        # print(f"Current direction: {self.direction}")  # debug

    def _position_to_grid(self, x, y):
        """Translates the x y coordinates to grid positions."""
        return round(x / self.size) * self.size, round(y / self.size) * self.size

    def _draw(self, screen):
        """Draws the snake on the screen"""
        for part in self.body:
            x, y = self._position_to_grid(part[0], part[1])
            pygame.draw.rect(screen, self.colour, [x, y, self.size, self.size])

    def update(self, screen):
        """Updates the snakes body, size and draws the snake on the screen."""
        # self.snake_head = [self.pos_x, self.pos_y]  # update the head position of the snake.
        # self.body.append(self.snake_head)  # append the new head to the body list.
        #
        # # check if the length has decreased.
        # if len(self.body) > self.length:
        #     del self.body[0]
        snake_head = self._position_to_grid(self.pos_x, self.pos_y)
        self.snake_head = snake_head  # update position of head.

        if len(self.body) <= 0 or snake_head != self.body[-1]:
            self.body.append(snake_head)

        if len(self.body) > self.length:
            del self.body[0]

        self._draw(screen)  # draw the snake.

    def eat(self, food) -> bool:
        """Checks if the snake has eaten the food object.

        Args:
            food (Food): The food object that will be checked for position.
        """
        x, y = self._position_to_grid(self.pos_x, self.pos_y)
        if x == food.pos_x and y == food.pos_y:
            self.length += 1
            self.speed += self.speed_increment  # increase the game speed
            return True
        return False

    def is_dead(self) -> bool:
        """Check if the snake left the playable area, or tried to eat itself."""
        for part in self.body[:-1]:
            if part == self.snake_head:
                return True

        x, y = self._position_to_grid(self.pos_x, self.pos_y)
        if x < 0 or x >= DISPLAY_WIDTH:
            return True
        elif y < 0 or y >= DISPLAY_HEIGHT:
            return True

        return False

    def reset(self):
        del self.body[1:]
        self.length = 1
