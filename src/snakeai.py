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

    def move_towards(self, food_x: float, food_y: float):
        """Tells the snake to move towards a given position.

        Todo:
            Add checks to stop the snake from moving backwards.
            or onto itself.

        Args:
            food_x: The x-coordinate of the target.
            food_y: The y-coordinate of the target.
        """
        if self.x > food_x:
            self.move_left()

        if self.x < food_x:
            self.move_right()

        if self.x == food_x:
            if self.y < food_y:
                self.move_down()

            if self.y > food_y:
                self.move_up()
