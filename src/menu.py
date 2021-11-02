
import pygame


class Menu:
    def __init__(self, game):
        self.game = game

    def update(self):
        self.game.reset_keys()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.game.draw_text(screen, 'Title Screen', (100, 100, 100),
                            self.game.game_width / 2, self.game.game_height / 2)

