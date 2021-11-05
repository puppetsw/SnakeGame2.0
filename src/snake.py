"""
Snake class which will contain information about the snake!
"""

from enum import Enum

import pygame.draw
from pygame.rect import Rect

from globals import *


class SnakeDirection(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Snake:
    """Player snake"""
    def __init__(self, game, position: tuple[float, float]):
        self.game = game
        self.colour = WHITE
        self._pos_x = position[0]
        self._pos_y = position[1]
        self.size = 20  # size of the snake on the screen.
        self.speed = 5
        self.speed_increment = 0.1
        self.length = 1
        self.body = []  # the snakes body parts.
        self.snake_head = []  # current position of the head.
        # make sure the initial direction of the snake matches
        # the current_direction of the snake attribute.
        self.direction = (self.size, 0)
        self.current_direction = SnakeDirection.LEFT

    @property
    def x(self):
        return round(self._pos_x / self.size) * self.size

    @property
    def y(self):
        return round(self._pos_y / self.size) * self.size

    def update(self, delta_time: float, controls: dict[str, bool]):
        """
        Updates the snake position and body parts.
        Changes direction if the user has pressed a key.
        Direction is only changed if the new direction is not the opposite of the current direction.

        Args:
            delta_time: delta time since last update.
            controls: controls that the user has pressed.
        """
        self.snake_head = self.x, self.y  # update the current position of the head.

        if len(self.body) <= 0 or self.snake_head != self.body[-1]:
            self.body.append(self.snake_head)

        if len(self.body) > self.length:
            del self.body[0]

        if controls is not None:  # added, so we can use the same update function with ai.
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

        self._pos_x += self.direction[0] * self.speed * delta_time
        self._pos_y += self.direction[1] * self.speed * delta_time

        self.game.reset_keys()  # make sure to reset the keys after each loop.

    def draw(self, screen):
        """Draws the snake on the screen"""
        for part in self.body:
            rect = Rect(part[0], part[1], self.size, self.size)
            surf = pygame.Surface((self.size, self.size))
            surf.fill(self.colour)
            screen.blit(surf, rect)

    def eat(self, food) -> bool:
        """Checks if the snake has eaten the food object.

        Args:
            food: The food object that will be checked for position.

        Returns:
            bool: True if the snake has eaten the food, False otherwise.
        """
        if self.x == food.pos_x and self.y == food.pos_y:
            self.length += 1
            self.speed += self.speed_increment  # increase the game speed
            return True
        return False

    def is_dead(self) -> bool:
        """Check if the snake left the playable area, or tried to eat itself.

        Returns:
            bool: True if the snake is dead, False otherwise.
        """
        for part in self.body[:-1]:
            if part == self.snake_head:
                return True

        if self.x < 0 or self.x >= self.game.game_width:
            return True
        elif self.y < 0 or self.y >= self.game.game_height:
            return True

        return False

    def reset(self):
        """Resets the length of the snake back to initial settings."""
        del self.body[1:]
        self.length = 1
