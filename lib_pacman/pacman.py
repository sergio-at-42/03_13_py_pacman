from .config import Config
from .maze import Maze
from .sprite import SpPacman
from .direction import Direction
from .mood import Mood


class Pacman():

    def __init__(self) -> None:
        self.name: str = "Pacman"
        self.score: int = 0
        self.live: int = 0
        self.color: int = 0x00ffff
        self.home_pos: tuple[int, int] = (Config.width // 2 - 1, Config.height // 2)
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.pos
        self.direction: Direction = Direction.STOP
        self.next_direction: Direction = Direction.STOP
        self.normal_speed: float = 2
        self.speed: float = self.normal_speed
        self.turbo_speed: float = 4
        self.turbo_time: int = 0
        self.dead: bool = False
        self.between_pos: float = 0
        self.sprite_pos: tuple[int, int] = (40, 40)
        self.sprite: SpPacman = SpPacman(self)

    def turn(self, direction: Direction) -> None:
        if Maze.cell_exit(self.next_pos) & direction.value:
            self.next_direction = direction
        elif self.between_pos == 0:
            self.next_direction = Direction.STOP
            self.next_pos = self.pos

    def move(self) -> None:
        from .game import Game
        self.speed: float = self.normal_speed
        if self.turbo_time:
            self.turbo_time -= 1
            self.speed = self.turbo_speed
        self.between_pos = (self.between_pos 
                            + abs(self.direction.move()[0] * self.speed)
                            + abs(self.direction.move()[1] * self.speed))
        if self.between_pos >= Maze.cell_size or self.direction is Direction.STOP:
            self.between_pos = 0
            self.pos = self.next_pos
            self.turn(self.next_direction)
            self.direction = self.next_direction
            self.next_pos = self.direction.move_from(self.pos)
            col, row = self.pos
            if Maze.grid[row][col] & 32:
                self.score += Config.points_per_super_pacgum
                Maze.grid[row][col] -= 32
                Game.joy.rumble(1, 1, 1000)
                for g in Game.ghosts:
                    g.change_mood(Mood.SCARED)
            if Maze.grid[row][col] & 16:
                self.score += Config.points_per_pacgum
                Maze.grid[row][col] -= 16

        self.sprite_pos = Maze.convert_pos(self.pos)
        self.sprite_pos = (
            int(self.sprite_pos[0] + self.direction.move()[0] * self.between_pos),
            int(self.sprite_pos[1] + self.direction.move()[1] * self.between_pos))

    def turbo(self) -> None:
        self.turbo_time = 30

    def bomb(self) -> str:
        return ("images/poop.png")