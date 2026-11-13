from __future__ import annotations
from random import randint, randrange
import pygame  # type: ignore
from .config import Config
from .pacman import Pacman
from .maze import Maze
from .sprite import SpriteGhost
from .sprite_image import SpGhost, SpBlinky, SpPinky, SpInky, SpClyde
from .mood import Mood
from .direction import Direction


class Ghost():

    ghosts: set[Ghost] = set()
    sprites: pygame.sprite.Group = pygame.sprite.Group()

    def __init__(self) -> None:
        self.sprite: SpriteGhost = SpriteGhost(self)
        Ghost.sprites.add(self.sprite)
        Ghost.ghosts.add(self)
        self.images: SpGhost = SpGhost()
        self.name: str = "Gogo"
        self.color: int = 0xffffff
        self.home_pos: tuple[int, int] = (0, 0)
        self.corner_pos: tuple[int, int] = (0, 0)
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.pos
        self.target_pos: tuple[int, int] = self.corner_pos
        self.direction: Direction = Direction.STOP
        self.speed: float = 1
        self.normal_speed: float = 1
        self.mood: Mood = Mood.CHASE
        self.mood_time: int = randint(960, 1440)
        self.between_pos: float = 0

    def strategy(self) -> tuple[int, int]:
        return (Pacman.player.pos)

    def change_mood(self, new_mood: Mood) -> None:
        match new_mood:
            case Mood.CHASE:
                self.mood = Mood.CHASE
                self.mood_time = randint(960, 1440)  # 16 to 24 seconds
                self.speed = self.normal_speed
            case Mood.SCATTER:
                self.mood = Mood.SCATTER
                self.mood_time = randint(600, 960)  # 10 to 16 seconds
                self.speed = self.normal_speed
            case Mood.SCARED:
                self.mood = Mood.SCARED
                self.mood_time = 480
                self.speed = 0.7
            case Mood.HOME:
                self.mood = Mood.HOME
                self.mood_time = -1
                self.speed = 20
            case Mood.DEAD:
                self.mood = Mood.DEAD
                self.mood_time = -1
                self.speed = 8
            case Mood.RIDE:
                self.mood = Mood.RIDE
                self.mood_time = -1
                self.speed = self.normal_speed
            case Mood.GO:
                self.mood = Mood.GO
                self.mood_time = -1
                self.speed = 6
            case Mood.SLEEP:
                self.mood = Mood.SLEEP
                self.mood_time = -1
                self.speed = 0

    def move(self, pos: tuple[int, int] = (-1, -1)) -> None:
        # change mood to GO if a position is supplied
        if pos != (-1, -1):
            self.change_mood(Mood.GO)
            self.target_pos = pos

        # mood management of the ghost
        self.mood_time -= 1
        if self.mood_time == 0:
            if self.mood != Mood.CHASE:
                if self.mood == Mood.SCARED:
                    Pacman.player.points_multiplier = 1
                self.change_mood(Mood.CHASE)
            else:
                self.change_mood(Mood.SCATTER)

        # determine the target position based on the ghost's mood
        if self.pos == self.next_pos:
            if self.mood is Mood.CHASE:
                self.target_pos = self.strategy()
            elif self.mood is Mood.SCATTER:
                self.target_pos = self.corner_pos
            elif self.mood is Mood.HOME:
                self.target_pos = self.home_pos
                if self.pos == self.home_pos:
                    self.mood_time = 1
            elif self.mood is Mood.SCARED:
                px, py = Pacman.player.pos
                self.target_pos = (abs(Config.width - 1 - px),
                                   abs(Config.height - 1 - py))
            elif self.mood is Mood.DEAD:
                self.target_pos = self.home_pos
                if self.pos == self.home_pos:
                    self.mood_time = 1
            elif self.mood is Mood.RIDE:
                self.target_pos = (randrange(Config.width),
                                   randrange(Config.height))
            # compute the next cell to go
            next_directions: int = Maze.cell_exit(self.pos) \
                - self.direction.inverse().value
            if next_directions in (1, 2, 4, 8):
                self.direction = Direction(next_directions)
            elif next_directions == 0:
                self.direction = self.direction.inverse()
            else:
                self.bfs()
            self.next_pos = self.direction.move_from(self.pos)

        # compute the position in pixel between the origin of the cell
        # and the ghost position in the cell
        self.between_pos = (self.between_pos
                            + abs(self.direction.move()[0] * self.speed)
                            + abs(self.direction.move()[1] * self.speed))
        # verify if the ghost enter in a new cell
        if self.between_pos >= Maze.cell_size:
            self.between_pos = 0
            self.pos = self.next_pos
        # convertion of the cell position in sprite position for the ghost
        px, py = self.convert_pos(self.pos)
        self.sprite.rect.x = px
        self.sprite.rect.y = py
        self.sprite.rect.x = int(self.sprite.rect.x
                                 + self.direction.move()[0] * self.between_pos)
        self.sprite.rect.y = int(self.sprite.rect.y
                                 + self.direction.move()[1] * self.between_pos)
        self.sprite.file()

    def bfs(self) -> None:
        next_cells: dict[tuple[int, int], Direction] = {}
        visited_cells: set[tuple[int, int]] = set()
        visited_cells.add(self.pos)
        start_cell = Maze.cell_exit(self.pos) - self.direction.inverse().value
        if start_cell & Direction.NORTH.value:
            next_cells[Direction.NORTH.move_from(self.pos)] = Direction.NORTH
        if start_cell & Direction.EST.value:
            next_cells[Direction.EST.move_from(self.pos)] = Direction.EST
        if start_cell & Direction.SOUTH.value:
            next_cells[Direction.SOUTH.move_from(self.pos)] = Direction.SOUTH
        if start_cell & Direction.WEST.value:
            next_cells[Direction.WEST.move_from(self.pos)] = Direction.WEST

        search_pos: tuple[int, int] = list(next_cells.keys())[0]

        while search_pos != self.target_pos and len(next_cells) != 0:
            visited_cells.add(search_pos)
            search_pos_exit = Maze.cell_exit(search_pos)
            if search_pos_exit & Direction.NORTH.value:
                next_pos = Direction.NORTH.move_from(search_pos)
                if next_pos not in visited_cells:
                    next_cells[next_pos] = next_cells[search_pos]
            if search_pos_exit & Direction.EST.value:
                next_pos = Direction.EST.move_from(search_pos)
                if next_pos not in visited_cells:
                    next_cells[next_pos] = next_cells[search_pos]
            if search_pos_exit & Direction.SOUTH.value:
                next_pos = Direction.SOUTH.move_from(search_pos)
                if next_pos not in visited_cells:
                    next_cells[next_pos] = next_cells[search_pos]
            if search_pos_exit & Direction.WEST.value:
                next_pos = Direction.WEST.move_from(search_pos)
                if next_pos not in visited_cells:
                    next_cells[next_pos] = next_cells[search_pos]
            del next_cells[search_pos]
            if len(next_cells) != 0:
                search_pos = list(next_cells.keys())[0]
            else:
                search_pos = self.target_pos
        if len(next_cells) == 0:
            self.direction = self.direction.inverse()
        else:
            self.direction = next_cells[search_pos]

    def convert_pos(self, grid_pos: tuple[int, int]) -> tuple[int, int]:
        grid_x: int = 0
        grid_y: int = 0
        grid_x, grid_y = grid_pos
        return ((grid_x * Maze.cell_size + 8, grid_y * Maze.cell_size + 8))

    @classmethod
    def move_ghosts_to_home_position(cls) -> None:
        for g in Ghost.ghosts:
            g.change_mood(Mood.HOME)


class Blinky(Ghost):
    def __init__(self) -> None:
        self.sprite = SpriteGhost(self)
        super().__init__()
        self.images: SpGhost = SpBlinky()
        self.name = "blinky"
        self.color: int = 0xff0000
        self.corner_pos: tuple[int, int] = (0, 0)
        self.home_pos: tuple[int, int] = self.corner_pos
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.pos
        self.normal_speed = 1.5

    def strategy(self) -> tuple[int, int]:
        remain_gum: float = 1  # gum remaining percentage
        px, py = Pacman.player.pos
        gx, gy = self.pos
        if abs(px - gx) + abs(py - gy) <= 4:
            self.speed = Pacman.player.normal_speed
        else:
            remain_gum = (len(Maze.pellets.pacgums)
                          + len(Maze.pellets.super_pacgums)) \
                            / (Config.pacgum + Config.spacgum)
            if remain_gum > 0.2:
                remain_gum = 0.3
            self.speed = self.normal_speed * (1.3 - remain_gum)
        return (Pacman.player.pos)


class Pinky(Ghost):
    def __init__(self) -> None:
        self.sprite = SpriteGhost(self)
        super().__init__()
        self.images: SpGhost = SpPinky()
        self.name = "pinky"
        self.color: int = 0xffc0c0
        self.corner_pos: tuple[int, int] = (Config.width-1, 0)
        self.home_pos: tuple[int, int] = self.corner_pos
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.pos
        self.normal_speed = 1

    def strategy(self) -> tuple[int, int]:
        px, py = Pacman.player.pos
        dx, dy = Pacman.player.direction.move()
        px = px + dx * 4
        py = py + dy * 4
        return (Maze.limit((px, py)))


class Inky(Ghost):
    def __init__(self) -> None:
        self.sprite = SpriteGhost(self)
        super().__init__()
        self.images: SpGhost = SpInky()
        self.name = "inky"
        self.color: int = 0x0000ff
        self.corner_pos: tuple[int, int] = (Config.width-1, Config.height-1)
        self.home_pos: tuple[int, int] = self.corner_pos
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.pos
        self.normal_speed: float = 1

    def strategy(self) -> tuple[int, int]:
        px, py = Pacman.player.pos
        dx, dy = Pacman.player.direction.move()
        px = px + dx * 2
        py = py + dy * 2
        return (Maze.limit((px, py)))


class Clyde(Ghost):
    def __init__(self) -> None:
        self.sprite = SpriteGhost(self)
        super().__init__()
        self.images: SpGhost = SpClyde()
        self.name = "clyde"
        self.color: int = 0xff7f00
        self.corner_pos: tuple[int, int] = (0, Config.height-1)
        self.home_pos: tuple[int, int] = self.corner_pos
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.pos
        self.normal_speed = 1.3

    def strategy(self) -> tuple[int, int]:
        # if Pacman.player.speed == 0:
        #     self.speed = 16
        # else:
        #     self.speed = self.normal_speed
        px, py = Pacman.player.pos
        gx, gy = self.pos
        if abs(px - gx) + abs(py - gy) > 8:
            return (Pacman.player.pos)
        return (self.corner_pos)
