from __future__ import annotations
from .maze import Maze
from .sprite import SpriteBomb
from .sprite_image import SpBomb
from .explosion import Explosion


class Bomb():

    bombs: set[Bomb] = set()

    def __init__(self, pos: tuple[int, int]) -> None:
        self.pos: tuple[int, int] = pos
        self.delay: int = 2 * 60 # delay in second * number of FPS
        self.remain: int = self.delay
        self.images: SpBomb = SpBomb()
        self.sprite: SpriteBomb = SpriteBomb(self)
        x, y = Maze.convert_pos(self.pos)
        self.sprite.rect.x = x
        self.sprite.rect.y = y
        Bomb.bombs.add(self)

    def danger(self) -> None:
        self.sprite.file()
        if self.remain > 0:
            self.remain -= 1
        else:
            self.explode()

    def explode(self) -> None:
        Explosion((self.pos))
        Bomb.bombs.discard(self)
