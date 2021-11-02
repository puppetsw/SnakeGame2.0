"""
Food class for handling the generation of food.
"""

import random
import pygame.draw
from pygame import Rect

from globals import *


class Food:

    def __init__(self, game):
        self.game = game
        self.size = 20
        self.colour = (255, 0, 0)
        self.pos_x = round(random.randrange(0, game.game_width - self.size) / self.size) * self.size
        self.pos_y = round(random.randrange(0, game.game_height - self.size) / self.size) * self.size

    def update(self, screen):
        """Draws the food on the screen"""
        pygame.draw.rect(screen, RED, [self.pos_x, self.pos_y, self.size, self.size])

    def draw(self, screen):
        """Draws the food on the screen"""
        rect = Rect(self.pos_x, self.pos_y, self.size, self.size)
        surf = pygame.Surface((self.size, self.size))
        surf.fill(self.colour)
        screen.blit(surf, rect)