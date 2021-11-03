"""
Snake v2.0
"""

from game import Game, GameState


def main():
    """Main loop of the game."""
    game = Game(1024, 768)
    game.running = True
    game.playing = True
    game.game_state = GameState.RUNNING

    while game.running:
        game.game_loop()


if __name__ == "__main__":
    main()
