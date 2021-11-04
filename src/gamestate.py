from enum import Enum


class GameState(Enum):
    """
    Enum for game states
    """
    NONE = 0
    RUNNING = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    QUITTING = 5
    OPTIONS = 6
