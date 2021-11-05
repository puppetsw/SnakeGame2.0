from snake import Snake, SnakeDirection


class SnakeAI(Snake):
    """Computer controlled snake."""
    def __init__(self, game, position: tuple[float, float]):
        super().__init__(game, position)

    def move_left(self):
        self.direction = -self.size, 0
        self.current_direction = SnakeDirection.LEFT

    def move_right(self):
        self.direction = self.size, 0
        self.current_direction = SnakeDirection.RIGHT

    def move_up(self):
        self.direction = 0, -self.size
        self.current_direction = SnakeDirection.UP

    def move_down(self):
        self.direction = 0, self.size
        self.current_direction = SnakeDirection.DOWN

    def target(self, dx: float, dy: float):
        """Tells the snake to move towards a given position.

        Args:
            dx: The x-coordinate of the target.
            dy: The y-coordinate of the target.
        """
        if self.x > dx:
            self.move_left()

        if self.x < dx:
            self.move_right()

        if self.x == dx:
            if self.y < dy:
                self.move_down()

            if self.y > dy:
                self.move_up()
