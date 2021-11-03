from gamestate import GameState


class Menu:
    def __init__(self, game):
        self.game = game

    def update(self, controls):

        if controls['action']:
            self.game.game_state = GameState.PLAYING

        self.game.reset_keys()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.game.draw_text(screen, 'Snake 2.0', (100, 100, 100),
                            self.game.game_width / 2, self.game.game_height / 4)
        self.game.draw_text(screen, 'Press space to play', (100, 100, 100),
                            self.game.game_width / 2, self.game.game_height / 2)

