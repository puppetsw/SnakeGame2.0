"""
Snake class which will contain information about the snake!
"""

from enum import Enum

import pygame.draw
from pygame.rect import Rect

from globals import *


class SnakeDirection(Enum):
    """Enum class for the snake directions"""
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Snake:
    """Snake player class"""
    def __init__(self, game):
        self.game = game
        self.colour = GREEN
        self.pos_x = 0  # set initial position # TODO Use properties to set?
        self.pos_y = 0  # set initial position # TODO Use properties to set?
        self.size = 20  # size of the snake on the screen.
        self.speed = 5
        self.speed_increment = 0.1
        self.length = 1
        self.body = []  # how many body of the snake to draw.
        self.snake_head = []  # current position of the head.
        self.direction = (self.size, 0)
        self.current_direction = SnakeDirection.LEFT

    def update(self, delta_time: float, controls: dict[str, bool]):
        """
        Updates the snake position and body parts.
        Changes direction if the user has pressed a key.
        Direction is only changed if the new direction is not the opposite of the current direction.

        Args:
            delta_time: delta time since last update.
            controls: controls that the user has pressed.
        """
        snake_head = self._position_to_grid(self.pos_x, self.pos_y)
        self.snake_head = snake_head  # update position of head.

        if len(self.body) <= 0 or snake_head != self.body[-1]:
            self.body.append(snake_head)

        if len(self.body) > self.length:
            del self.body[0]

        if controls['left'] and self.current_direction != SnakeDirection.RIGHT:
            self.direction = -self.size, 0
            self.current_direction = SnakeDirection.LEFT
        if controls['right'] and self.current_direction != SnakeDirection.LEFT:
            self.direction = self.size, 0
            self.current_direction = SnakeDirection.RIGHT
        if controls['up'] and self.current_direction != SnakeDirection.DOWN:
            self.direction = 0, -self.size
            self.current_direction = SnakeDirection.UP
        if controls['down'] and self.current_direction != SnakeDirection.UP:
            self.direction = 0, self.size
            self.current_direction = SnakeDirection.DOWN

        self.pos_x += self.direction[0] * self.speed * delta_time
        self.pos_y += self.direction[1] * self.speed * delta_time
        self.game.reset_keys()  # make sure to reset the keys after each loop.

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
            food: The food object that will be checked for position.
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
