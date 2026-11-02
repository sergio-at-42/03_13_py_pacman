from .maze import Maze
from .sprite import SpriteBomb
from .sprite_image import SpBomb
from .explosion import Explosion


class Bomb():

    bombs: dict[tuple[int, int], Bomb] = {}

    def __init__(self, pos: tuple[int, int]) -> None:
        self.pos: tuple[int, int] = pos
        self.delay: int = 2 * 60 # delay in second * number of FPS
        self.remain: int = self.delay
        self.images: SpBomb = SpBomb()
        self.sprite: SpriteBomb = SpriteBomb(self)
        self.sprite_pos: tuple[int, int] = Maze.convert_pos(self.pos)
        Bomb.bombs[self.pos] = self

    def file(self) -> str:
        file_name: str = self.sprite.file()
        if self.remain > 0:
            self.remain -= 1
        else:
            self.explode()
        return(file_name)

    def explode(self) -> None:
        Explosion((self.pos))
        Bomb.bombs.pop(self.pos, None)
