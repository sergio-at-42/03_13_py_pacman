from datetime import datetime
import pygame
from .sprite_image import SpPacman, SpGhost, SpScared, SpEndScared, SpEyes, SpBomb
from.maze import Maze
from .mood import Mood


class Sprite(pygame.sprite.Sprite):
    directory: str = "lib_pacman/images/"

    def __init__(self) -> None:
        # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.image.load(f"{self.directory}tardis.png").convert_alpha()
       self.rect = self.image.get_rect()

    @classmethod
    def convert_pos(self, grid_pos: tuple[int, int]) -> tuple[int, int]:
        grid_x: int = 0
        grid_y: int = 0
        grid_x, grid_y = grid_pos
        return ((grid_x * Maze.cell_size + 8, grid_y * Maze.cell_size + 8))

class SpritePacman(Sprite):
    def __init__(self, player_images: type[SpPacman], player) -> None:
        from .pacman import Pacman
        super().__init__()
        self.player_images: SpGhost = player_images()
        self.player: Pacman = player

    def file(self) -> str:
        if self.player.dead:
            sprite = SpEyes(self.player)
        else:
            sprite: SpPacman = self.player_images
        anim: int = (datetime.now().microsecond // 250000) % sprite.nb_anim
        file = f"{getattr(sprite, f"sp{self.player.direction.letter()}{str(anim)}")}"
        return (f"{self.directory}{file}")


class SpriteGhost(Sprite):
    def __init__(self, ghost_images: type[SpGhost], ghost) -> None:
        from .ghost import Ghost
        super().__init__()
        self.ghost_images: SpGhost = ghost_images()
        self.ghost: Ghost = ghost

    def file(self) -> str:
        if self.ghost.mood == Mood.SCARED:
            if self.ghost.mood_time <= 180 and (self.ghost.mood_time // 20) % 2 == 0:
                sprite = SpEndScared()
            else:
                sprite = SpScared()
        elif self.ghost.mood == Mood.DEAD:
            sprite = SpEyes()
        else:
            sprite: SpGhost = self.ghost_images
        anim: int = (datetime.now().microsecond // 250000) % sprite.nb_anim
        file = f"{getattr(sprite, f"sp{self.ghost.direction.letter()}{str(anim)}")}"
        return (f"{self.directory}{file}")


class SpriteBomb(Sprite):
    def __init__(self, bomb_images: type[SpBomb], bomb) -> None:
        from .bomb import Bomb
        super().__init__()
        self.bomb_images: SpGhost = bomb_images()
        self.bomb_images.nb_anim -= 1
        self.bomb: Bomb = bomb
        self.delay: int = self.bomb.delay * 60
        self.remain: int = self.delay

    def file(self) -> str:
        anim: int = int(self.bomb_images.nb_anim - self.remain / self.delay * self.bomb_images.nb_anim)
        if self.remain > 0:
            self.remain -= 1
        file = f"{getattr(self.bomb_images, f"sp{str(anim)}")}"
        return (f"{self.directory}{file}")
