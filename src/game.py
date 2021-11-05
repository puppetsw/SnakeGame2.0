import sys

import pygame

from food import Food
from gamestate import GameState
from globals import *
from menu import TitleMenu
from snake import Snake
from snakeai import SnakeAI

pygame.init()


class Game:
    """
    Main class for handling the main loops of the game,
    game states and menu interactions.
    """
    def __init__(self, display_width, display_height):
        self.screen = pygame.display.set_mode((display_width, display_height))
        self.display_width = display_width
        self.display_height = display_height

        self.game_state = GameState.NONE
        self.game_width = 1024
        self.game_height = 768
        self.game_canvas = pygame.Surface((self.game_width, self.game_height))  # upscale

        self.clock = pygame.time.Clock()
        self.frame_rate = 30
        self.score = 0

        self.running = False
        self.controls = {'left': False, 'right': False, 'up': False, 'down': False, 'action': False, 'back': False}
        self.delta_time = 0

        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.debug_font = pygame.font.Font(pygame.font.get_default_font(), 15)

        self.title_menu = TitleMenu(self)

        self.player = Snake(self, (self.game_width // 2, self.game_height // 2))
        self.player.colour = GREEN

        self.enemy = SnakeAI(self, (self.game_width // 2, self.game_height // 3))
        self.enemy.colour = YELLOW

        self.food = Food(self)

    def get_events(self):
        """Get events from pygame and set the controls to true."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
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
        if self.game_state == GameState.RUNNING:
            # display title screen and menu
            self.title_menu.update(self.controls)
            self.title_menu.draw(self.game_canvas)

        if self.game_state == GameState.PLAYING:
            self.game_canvas.fill(BLACK)  # clear the screen

            self.food.draw(self.game_canvas)

            self.player.update(self.delta_time, self.controls)
            self.player.draw(self.game_canvas)

            self.enemy.update(self.delta_time, None)  # pass None for controls
            self.enemy.draw(self.game_canvas)
            self.enemy.target(self.food.pos_x, self.food.pos_y)

            if self.player.eat(self.food):
                self.food.update_position()
                self.score += 10  # score increment

            if self.enemy.eat(self.food):
                self.food.update_position()
                self.score -= 10

            if self.player.is_dead():
                self.game_state = GameState.GAME_OVER

            self.display_score(str(self.score), WHITE, self.game_canvas)

        if self.game_state == GameState.GAME_OVER:
            # TODO Add game over screen
            pass

        if self.game_state == GameState.QUITTING:
            pygame.quit()
            sys.exit()

        self.debug_info(self.game_canvas)

    def draw(self):
        # Scale up the canvas to the screensize and draw it to the screen.
        self.screen.blit(pygame.transform.scale(self.game_canvas, (self.display_width, self.display_height)), (0, 0))
        pygame.display.flip()

    def update_delta_time(self):
        """Get delta time by framerate"""
        self.delta_time = self.clock.tick(self.frame_rate) / 1000  # seconds

    def draw_text(self, surface, text, color, x, y, position='center', font=None):
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if position == 'bottomleft':
            text_rect.bottomleft = (x, y)
        elif position == 'bottomright':
            text_rect.bottomright = (x, y)
        elif position == 'topleft':
            text_rect.topleft = (x, y)
        elif position == 'topright':
            text_rect.topright = (x, y)
        elif position == 'center':
            text_rect.center = (x, y)
        else:
            text_rect.center = (x, y)

        surface.blit(text_surface, text_rect)

    def debug_info(self, surface):
        """Print debug info on the screen."""
        screen_pos = 20
        self.draw_text(surface, "FPS: " + str(int(self.clock.get_fps())), WHITE, self.game_width, self.game_height,
                       font=self.debug_font, position='bottomright')

        for k, v in vars(self.player).items():
            self.draw_text(surface, f'{k}:{v}', CYAN, 10, screen_pos, font=self.debug_font, position='topleft')
            screen_pos += 20

        self.draw_text(surface, f'GAME_STATE:{self.game_state}',
                       (0, 255, 255), self.game_width, 20, position='bottomright', font=self.debug_font)

        self.draw_text(surface, 'FOOD', CYAN, 10, screen_pos, font=self.debug_font, position='topleft')
        screen_pos += 20

        for k, v in vars(self.food).items():
            self.draw_text(surface, f'{k}:{v}', CYAN, 10, screen_pos, font=self.debug_font, position='topleft')
            screen_pos += 20

    def game_loop(self):
        while self.running:
            self.update_delta_time()
            self.get_events()
            self.update()
            self.draw()

    def display_score(self, text, colour, screen):
        """Display score in bottom left corner."""
        m = self.font.render(text, True, colour)
        screen.blit(m, (5, self.game_height - 20))
