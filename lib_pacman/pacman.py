from __future__ import annotations
from .config import Config
from .session import Session
from .maze import Maze
from .sprite import SpritePacman
from .sprite_image import SpPacman
from .direction import Direction
from .mood import Mood


class Pacman():

    player: Pacman

    def __init__(self) -> None:
        self.sprite: SpritePacman = SpritePacman(self)
        Pacman.player = self
        self.images: SpPacman = SpPacman()
        self.name: str = "Pacman"
        self.score: int = 0
        self.points_multiplier: int = 1
        self.lives: int = 3
        self.color: int = 0x00ffff
        self.home_pos: tuple[int, int] = (
            (Config.width - 1) // 2 - 1, Config.height // 2)
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.pos
        self.direction: Direction = Direction.STOP
        self.next_direction: Direction = Direction.STOP
        self.normal_speed: float = 2
        self.speed: float = self.normal_speed
        self.turbo_speed: float = 2
        self.turbo_time: int = 0
        self.dead: int = 0
        self.between_pos: float = 0

    def init_start_position(self) -> None:
        self.home_pos = ((Config.width + 1) // 2 - 1, Config.height // 2)
        self.pos = self.home_pos
        self.next_pos = self.pos
        self.between_pos = 0
        self.direction = Direction.STOP
        self.next_direction = Direction.STOP
        self.dead = 0

    def move(self) -> None:
        from .game import Game
        from .ghost import Ghost
        # set speed
        self.speed = self.normal_speed
        if self.turbo_time:
            self.turbo_time -= 1
            self.speed = self.normal_speed * self.turbo_speed
        if self.dead != 0:
            self.speed = 0
            self.dead += 1
            if self.dead >= 60:
                Game.loose = True
        # determine the next position and the direction based on
        # the next direction
        if self.between_pos == 0:
            if Maze.cell_exit(self.pos) & self.next_direction.value:
                self.direction = self.next_direction
                self.next_pos = self.direction.move_from(self.pos)
            elif Maze.cell_exit(self.pos) & self.direction.value:
                self.next_pos = self.direction.move_from(self.pos)
            else:
                self.speed = 0
        # cas of U-turn between 2 cells
        elif self.next_direction == self.direction.inverse():
            self.direction = self.next_direction
            pos: tuple[int, int] = self.pos
            self.pos = self.next_pos
            self.next_pos = pos
            self.between_pos = 48 - self.between_pos
        # set number of pixel between 2 cells positions
        self.between_pos = (self.between_pos
                            + abs(self.direction.move()[0] * self.speed)
                            + abs(self.direction.move()[1] * self.speed))
        # set new position when arrival in a new cell
        if self.between_pos >= Maze.cell_size:
            self.between_pos = 0
            self.pos = self.next_pos
            # processing of cell content
            if self.pos in Maze.pellets.super_pacgums:
                self.score += Config.points_per_super_pacgum
                Maze.pellets.super_pacgums.discard(self.pos)
                if hasattr(Game, "joy"):
                    Game.joy.rumble(1, 1, 1000)
                for g in Ghost.ghosts:
                    g.change_mood(Mood.SCARED)
            if self.pos in Maze.pellets.pacgums:
                self.score += Config.points_per_pacgum
                Maze.pellets.pacgums.discard(self.pos)
            if len(Maze.pellets.pacgums) == 0\
                    and len(Maze.pellets.super_pacgums) == 0:
                Session.session.next_level = True
        px, py = Maze.convert_pos(self.pos)
        mx, my = self.direction.move()
        self.sprite.rect.x = int(px + mx * self.between_pos)
        self.sprite.rect.y = int(py + my * self.between_pos)
        self.sprite.file()

    def turbo(self) -> None:
        self.turbo_time = 30
