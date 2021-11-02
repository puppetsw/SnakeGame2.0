"""
Snake game v2
"""

import pygame as p

from pygame.constants import *

from time import sleep

from game import Game, GameState
from globals import *
from snake import Snake
from food import Food


def main():
    """Main loop of the game."""
    game = Game(1024, 768)
    game.running = True
    game.playing = True
    game.game_state = GameState.PLAYING

    while game.running:
        game.game_loop()


if __name__ == "__main__":
    main()
