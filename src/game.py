import sys

import pygame

from food import Food
from gamestate import GameState
from globals import *
from menu import TitleMenu
from snake import Snake
from snakeai import SnakeAI

pygame.init()  # initialise pygame


class Game:
    """
    Main class for handling the main loops of the game,
    game states and menu interactions.
    """
    def __init__(self, display_width, display_height):
        pygame.display.set_caption(GAME_NAME)  # set the title of the window.
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

            self.food.draw(self.game_canvas)  # draw the food

            self.player.update(self.delta_time, self.controls)  # check player controls and update position
            self.player.draw(self.game_canvas)  # draw the player snake.

            self.enemy.update(self.delta_time, None)  # pass None for controls
            self.enemy.draw(self.game_canvas)  # draw the enemy snake.
            self.enemy.move_towards(self.food.pos_x, self.food.pos_y)  # make the ai move towards the food.

            if self.player.eat(self.food):  # if the player has eaten the food
                self.food.update_position()  # set a new position for the food.
                self.score += 10  # score increment

            if self.enemy.eat(self.food):
                self.food.update_position()
                self.score -= 10

            if self.player.is_dead():
                self.game_state = GameState.GAME_OVER

            self.draw_score(str(self.score), WHITE, self.game_canvas)

        if self.game_state == GameState.GAME_OVER:
            # TODO Add game over screen
            pass

        if self.game_state == GameState.QUITTING:
            pygame.quit()
            sys.exit()

        self.draw_debug_info(self.game_canvas)

    def update_delta_time(self):
        """Get delta time by framerate"""
        self.delta_time = self.clock.tick(self.frame_rate) / 1000  # seconds

    def draw(self):
        # Scale up the canvas to the screensize and draw it to the screen.
        self.screen.blit(pygame.transform.scale(self.game_canvas, (self.display_width, self.display_height)), (0, 0))
        pygame.display.flip()

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

    def draw_debug_info(self, surface):
        """Print debug info on the screen."""
        self.draw_text(surface, "FPS: " + str(int(self.clock.get_fps())), WHITE, self.game_width, self.game_height,
                       font=self.debug_font, position='bottomright')

        # Draw the current GameState on screen
        self.draw_text(surface, f'GAME_STATE:{self.game_state}', CYAN, self.game_width, 20,
                       position='bottomright', font=self.debug_font)

        screen_pos = [20]  # set starting y position
        # Draw the player snake object data on screen
        player_exclude_keys = ['body', 'game']  # keys to be excluded from debug info.
        self.draw_object_data(surface, self.player, screen_pos, CYAN, player_exclude_keys)
        # Draw the food object data on screen
        self.draw_object_data(surface, self.food, screen_pos, CYAN, ['game'])
        # Draw the ai object data on screen
        self.draw_object_data(surface, self.enemy, screen_pos, YELLOW, player_exclude_keys)

    def draw_object_data(self, surface, object_, screen_position: list[int], color: tuple[int, int, int],
                         exclude_keys: list[str]):
        """Loop through the attributes in the _object and display them and the values on screen.

        Note:
            Pass the screen_position in a list so that the y position can be incremented and
            updated by reference.

        Args:
            surface: the surface to draw the data on.
            object_: the object to get the data from.
            screen_position: the screen position to start drawing the data.
            color: the colour of the text.
            exclude_keys: any keys to be excluded from the data.
        """
        self.draw_text(surface, str(type(object_).__name__).upper(), color, 10, screen_position[0],
                       font=self.debug_font, position='bottomleft')
        screen_position[0] += 20  # increment the y position.
        for k, v in vars(object_).items():
            if k in exclude_keys:
                continue
            self.draw_text(surface, f'{k}:{v}', color, 10, screen_position[0],
                           font=self.debug_font, position='bottomleft')
            screen_position[0] += 20  # increment the y position.

    def draw_score(self, text, colour, screen):
        """Display score in bottom left corner."""
        m = self.font.render(text, True, colour)
        screen.blit(m, (5, self.game_height - 20))

    def game_loop(self):
        """The main game loop!"""
        while self.running:
            self.update_delta_time()
            self.get_events()
            self.update()
            self.draw()
