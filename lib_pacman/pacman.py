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

    def move(self) -> None:
        from .game import Game
        # set speed
        self.speed = self.normal_speed
        if self.turbo_time:
            self.turbo_time -= 1
            self.speed = self.turbo_speed
        # determine the next position and the direction based on the next direction
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
        if self.between_pos >= Maze.cell_size: # or self.direction is Direction.STOP:
            self.between_pos = 0
            self.pos = self.next_pos
            # processing of cell content
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
        # set new position in pixels
        px, py = Maze.convert_pos(self.pos)
        mx, my = self.direction.move()
        self.sprite_pos = (
            int(px + mx * self.between_pos),
            int(py + my * self.between_pos))

    def turbo(self) -> None:
        self.turbo_time = 30

    def bomb(self) -> str:
        return ("images/poop.png")