"""
Snake class which will contain information about the snake!
"""

import pygame.draw
from pygame.rect import Rect

from globals import *
from enum import Enum


class SnakeDirections(Enum):
    """
    Enum class for the snake directions
    """
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Snake:

    def __init__(self, game):
        self.game = game
        self.colour = (255, 255, 255)
        self.pos_x = 0  # set initial position # TODO Use properties to set?
        self.pos_y = 0  # set initial position # TODO Use properties to set?
        self.size = 20  # size of the snake on the screen.
        self.speed = 6
        self.speed_increment = 0.1
        self.length = 1
        self.body = []  # how many body of the snake to draw.
        self.snake_head = []  # current position of the head.
        self.direction = (self.size, 0)
        self.current_direction = 'left'

    def update(self, delta_time, actions):
        snake_head = self._position_to_grid(self.pos_x, self.pos_y)
        self.snake_head = snake_head  # update position of head.

        if len(self.body) <= 0 or snake_head != self.body[-1]:
            self.body.append(snake_head)

        if len(self.body) > self.length:
            del self.body[0]

        if actions['left'] and self.current_direction != 'right':
            self.direction = -self.size, 0
            self.current_direction = 'left'
        if actions['right'] and self.current_direction != 'left':
            self.direction = self.size, 0
            self.current_direction = 'right'
        if actions['up'] and self.current_direction != 'down':
            self.direction = 0, -self.size
            self.current_direction = 'up'
        if actions['down'] and self.current_direction != 'up':
            self.direction = 0, self.size
            self.current_direction = 'down'

        self.pos_x += self.direction[0] * self.speed * delta_time
        self.pos_y += self.direction[1] * self.speed * delta_time

    def _position_to_grid(self, x, y):
        """Translates the x y coordinates to grid positions."""
        return round(x / self.size) * self.size, round(y / self.size) * self.size

    def draw(self, screen):
        """Draws the snake on the screen"""
        for part in self.body:
            x, y = self._position_to_grid(part[0], part[1])
            rect = Rect(x, y, self.size, self.size)
            surf = pygame.Surface((self.size, self.size))
            surf.fill(self.colour)
            screen.blit(surf, rect)

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
        if x < 0 or x >= self.game.game_width:
            return True
        elif y < 0 or y >= self.game.game_height:
            return True

        return False

    def reset(self):
        del self.body[1:]
        self.length = 1
