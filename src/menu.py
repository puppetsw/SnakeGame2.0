"""
Class for handling the menus. Plan to have it so you pass in the menu names as a list.
That is then displayed on the screen with the selected item being the first in the list.
When the user presses up or down control keys, the selected index is moved up or down the list.
Just going to have selection being a asterisk or something next to the menu names for now.
This will all probably change as I work on it.
"""
from abc import ABC, abstractmethod

from gamestate import GameState
from globals import *


class MenuItem:
    def __init__(self, name):
        self.name = name
        self.position = (0, 0)
        self.selected = False


class Menu(ABC):
    def __init__(self, game, menu_items: list[MenuItem]):
        self.game = game
        self.selected_index = 0
        self.menu_items = menu_items
        self.menu_items[0].selected = True
        self.screen_center = (self.game.game_width / 2, self.game.game_height / 2)

    @abstractmethod
    def update(self, controls):
        pass

    @abstractmethod
    def draw(self, screen):
        pass


class OptionsMenu(Menu):
    def __init__(self, game):
        super().__init__(game, [])

    def update(self, controls):
        pass

    def draw(self, screen):
        pass


class TitleMenu(Menu):
    def __init__(self, game):
        super().__init__(game, [MenuItem('Start Game'), MenuItem('Multiplayer'),
                                MenuItem('Options'), MenuItem('Quit')])

        y_pos = 0
        for item in self.menu_items:
            item.position = (self.screen_center[0], self.screen_center[1] + y_pos)
            y_pos += 20

    def update(self, controls):
        if controls['action']:
            if self.selected_index == 0:
                self.game.game_state = GameState.PLAYING
            if self.selected_index == 3:
                self.game.game_state = GameState.QUITTING

        if controls['up']:
            self.menu_items[self.selected_index].selected = False
            self.selected_index -= 1
            if self.selected_index < 0:
                self.selected_index = len(self.menu_items) - 1
            self.menu_items[self.selected_index].selected = True

        if controls['down']:
            self.menu_items[self.selected_index].selected = False
            self.selected_index += 1
            if self.selected_index > len(self.menu_items) - 1:
                self.selected_index = 0
            self.menu_items[self.selected_index].selected = True

        self.game.reset_keys()

    def draw(self, screen):
        screen.fill(BLACK)

        self.game.draw_text(screen, 'Snake 2.0', WHITE, self.screen_center[0], self.screen_center[1] - 200)

        for menu_item in self.menu_items:
            if menu_item.selected:
                self.game.draw_text(screen, f'> {menu_item.name}', WHITE, menu_item.position[0], menu_item.position[1])
            else:
                self.game.draw_text(screen, menu_item.name, WHITE, menu_item.position[0], menu_item.position[1])
