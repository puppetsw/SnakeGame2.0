"""
Main Game class
"""
import time
from enum import Enum
import pygame

from menu import Menu
from snake import Snake

pygame.init()


class GameState(Enum):
    """
    Enum for game states
    """
    NONE = 0
    RUNNING = 1
    PLAYING = 2
    PAUSED = 3


class Game:
    def __init__(self, display_width, display_height):
        self.game_state = GameState.NONE
        self.display_width = display_width
        self.display_height = display_height
        self.game_width = 800
        self.game_height = 600
        self.screen = pygame.display.set_mode((display_width, display_height))
        self.game_canvas = pygame.Surface((self.game_width, self.game_height))  # upscale
        self.clock = pygame.time.Clock()
        self.player = Snake()
        self.running = False
        self.playing = False
        self.controls = {'left': False, 'right': False, 'up': False, 'down': False, 'action': False, 'back': False}
        self.delta_time = 0
        self.previous_time = 0
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.title_menu = Menu(self)

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.controls['left'] = True
                if event.key == pygame.K_RIGHT:
                    self.controls['right'] = True
                if event.key == pygame.K_UP:
                    self.controls['up'] = True
                if event.key == pygame.K_DOWN:
                    self.controls['down'] = True
                if event.key == pygame.K_ESCAPE:
                    self.controls['back'] = True
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.controls['action'] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.controls['left'] = False
                if event.key == pygame.K_RIGHT:
                    self.controls['right'] = False
                if event.key == pygame.K_UP:
                    self.controls['up'] = False
                if event.key == pygame.K_DOWN:
                    self.controls['down'] = False
                if event.key == pygame.K_ESCAPE:
                    self.controls['back'] = False
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.controls['action'] = False

    def reset_keys(self):
        for k in self.controls:
            self.controls[k] = False

    def update(self):
        if self.game_state == GameState.RUNNING:
            # display title screen and menu
            self.title_menu.update()
            self.title_menu.draw(self.game_canvas)
        if self.game_state == GameState.PLAYING:
            pass

    def draw(self):
        # Scale up the canvas to the screensize and draw it to the screen.
        self.screen.blit(pygame.transform.scale(self.game_canvas, (self.display_width, self.display_height)), (0, 0))
        pygame.display.flip()

    def get_delta_time(self):
        now = time.time()
        self.delta_time = now - self.previous_time
        self.previous_time = now

    def draw_text(self, surface, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def game_loop(self):
        while self.playing:
            self.get_delta_time()
            self.get_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game(1920, 1200)
    game.running = True
    game.playing = True
    game.game_state = GameState.RUNNING

    while game.running:
        game.game_loop()
