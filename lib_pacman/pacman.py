from .config import Config
from .ghost_strategy import GhostStrategy
from .sprite import SpPacman
from .direction import Direction


class Pacman():

    def __init__(self) -> None:
        self.name: str = "Pacman"
        self.color: int = 0x00ffff
        self.home_pos: tuple[int, int] = (Config.width // 2, Config.height * 3 // 4)
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.home_pos
        self.direction: Direction = Direction.STOP
        self.speed: int = 2
        self.dead: bool = False
        self.sprite: SpPacman = SpPacman(self)

    def chase(self) -> None:
        self.move_to(GhostStrategy.ride(self.pos))

    def escape(self) -> None:
        self.move_to(self.home_pos)

    def scatter(self) -> None:
        self.move_to(self.corner_pos)

    def move_to(self, pos: tuple[int, int]) -> None:
        self.next_pos = (0, 0)
