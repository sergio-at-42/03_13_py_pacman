from .config import Config
from .maze import Maze
from .sprite import SpriteBomb
from .sprite_image import SpBomb


class Bomb():

    def __init__(self, pos: tuple[int, int]) -> None:
        self.pos: tuple[int, int] = pos
        self.delay: int = 2
        self.sprite: SpriteBomb = SpriteBomb(SpBomb, self)
        self.sprite_pos: tuple[int, int] = Maze.convert_pos(self.pos)
