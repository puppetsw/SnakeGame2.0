import random

import pygame.draw
from pygame import Rect


class Food:
    """Handles the food positioning and colour."""

    def __init__(self, game):
        self.game = game
        self.size = 20
        self.colour = (255, 0, 0)
        self.pos_x = 0
        self.pos_y = 0
        self.update_position()

    # def update(self, controls):
    #     pass

    def draw(self, screen):
        """Draws the food on the screen"""
        rect = Rect(self.pos_x, self.pos_y, self.size, self.size)
        surf = pygame.Surface((self.size, self.size))
        surf.fill(self.colour)
        screen.blit(surf, rect)

    def update_position(self):
        """Generates a random position for the food"""
        self.pos_x = round(random.randrange(0, self.game.game_width - self.size) / self.size) * self.size
        self.pos_y = round(random.randrange(0, self.game.game_height - self.size) / self.size) * self.size
