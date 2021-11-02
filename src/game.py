"""
Main Game class
"""
from enum import Enum

import pygame

from food import Food
from globals import *
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
    GAME_OVER = 4


class Game:
    def __init__(self, display_width, display_height):
        self.game_state = GameState.NONE
        self.display_width = display_width
        self.display_height = display_height
        self.game_width = 1024
        self.game_height = 768
        self.screen = pygame.display.set_mode((display_width, display_height))
        self.game_canvas = pygame.Surface((self.game_width, self.game_height))  # upscale
        self.clock = pygame.time.Clock()
        self.player = Snake(self)
        self.player.colour = GREEN
        self.player.pos_x, self.player.pos_y = self.game_width // 2, self.game_height // 2
        self.running = False
        self.playing = False
        self.controls = {'left': False, 'right': False, 'up': False, 'down': False, 'action': False, 'back': False}
        self.delta_time = 0
        self.previous_time = 0
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.debug_font = pygame.font.Font(pygame.font.get_default_font(), 15)
        self.title_menu = Menu(self)
        self.food = Food(self)
        self.frame_rate = 60
        self.score = 0

    def get_events(self):
        """
        Get events from pygame and set the controls to true if the event is a keydown event.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.controls['left'] = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.controls['right'] = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.controls['up'] = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
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
        if self.game_state == GameState.RUNNING or self.game_state == GameState.GAME_OVER:
            # display title screen and menu
            self.title_menu.update()
            self.title_menu.draw(self.game_canvas)

        if self.game_state == GameState.PLAYING:
            self.game_canvas.fill(BLACK)  # clear the screen
            self.food.draw(self.game_canvas)
            self.player.update(self.delta_time, self.controls)
            self.player.draw(self.game_canvas)

            if self.player.eat(self.food):
                self.food = Food(self)
                self.score += 10  # score increment

            if self.player.is_dead():
                self.game_state = GameState.GAME_OVER

            self.display_score(str(self.score), WHITE, self.game_canvas)

            self.reset_keys()  # make sure to reset the keys after each loop.

        self.debug_info(self.game_canvas)

    def draw(self):
        # Scale up the canvas to the screensize and draw it to the screen.
        self.screen.blit(pygame.transform.scale(self.game_canvas, (self.display_width, self.display_height)), (0, 0))
        pygame.display.flip()

    def get_delta_time(self):
        """Get delta time by framerate"""
        self.delta_time = self.clock.tick(self.frame_rate) / 1000  # seconds

    def draw_text(self, surface, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def debug_info(self, surface):
        """Print debug info on the screen."""
        screen_pos = 15
        for k, v in vars(self.player).items():
            # print(k, v)
            text_surface = self.debug_font.render(f'{k}:{v}', True, (0, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.bottomleft = (10, screen_pos)
            surface.blit(text_surface, text_rect)
            screen_pos += 20

        text_surface = self.debug_font.render(f'GAME_STATE:{self.game_state}', True, (0, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, screen_pos)
        surface.blit(text_surface, text_rect)

        screen_pos += 20

        text_surface = self.debug_font.render('FOOD', True, (0, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, screen_pos)
        surface.blit(text_surface, text_rect)

        screen_pos += 20

        for k, v in vars(self.food).items():
            # print(k, v)
            text_surface = self.debug_font.render(f'{k}:{v}', True, (0, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.bottomleft = (10, screen_pos)
            surface.blit(text_surface, text_rect)
            screen_pos += 20

    def game_loop(self):
        while self.playing:
            self.get_delta_time()
            self.get_events()
            self.update()
            self.draw()

    def display_score(self, text, colour, screen):
        """Display score in top left corner."""
        m = self.font.render(text, True, colour)
        screen.blit(m, (5, self.game_height - 20))
