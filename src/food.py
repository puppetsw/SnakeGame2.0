"""
Food class for handling the generation of food.
"""

import random
import pygame.draw
from globals import *


class Food:

    def __init__(self):
        self.size = 20
        self.pos_x = round(random.randrange(0, DISPLAY_WIDTH - self.size) / self.size) * self.size
        self.pos_y = round(random.randrange(0, DISPLAY_HEIGHT - self.size) / self.size) * self.size

    def update(self, screen):
        """Draws the food on the screen"""
        pygame.draw.rect(screen, RED, [self.pos_x, self.pos_y, self.size, self.size])
