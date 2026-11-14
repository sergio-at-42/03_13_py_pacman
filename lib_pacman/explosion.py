from __future__ import annotations
from .config import Config
from .maze import Maze
from .sprite import SpriteExplosion
from .sprite_image import SpExplosion
from .pacman import Pacman
from .ghost import Ghost
from .mood import Mood


class Explosion():

    explosions: set[Explosion] = set()

    def __init__(self, pos: tuple[int, int]) -> None:
        self.pos: tuple[int, int] = pos
        self.delay: int = 30  # delay in frames : 0.5 secondes * 60 FPS
        self.remain: int = self.delay
        self.images: SpExplosion = SpExplosion()
        self.sprite: SpriteExplosion = SpriteExplosion(self)
        px, py = self.pos
        px -= 1
        py -= 1
        x, y = Maze.convert_pos((px, py))
        self.sprite.rect.x = x
        self.sprite.rect.y = y
        Explosion.explosions.add(self)
        self.explosion_area: set[tuple[int, int]] = set()
        for x in range(px, px+3):
            for y in range(py, py+3):
                self.explosion_area.add((x, y))

    def boum(self) -> None:
        self.sprite.file()
        for g in Ghost.ghosts:
            if g.pos in self.explosion_area and g.mood != Mood.DEAD:
                g.change_mood(Mood.DEAD)
                Pacman.player.score += Config.points_per_ghost
        if self.remain > 0:
            self.remain -= 1
        else:
            Explosion.explosions.discard(self)
