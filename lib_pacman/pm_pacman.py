from datetime import datetime
from .pm_config import PmConfig
from .pm_ghost_strategy import PmGhostStrategy
from .pm_sprite import PmSpPacman
from .direction import Direction


class PmPacman():

    def __init__(self) -> None:
        self.name: str = "Pacman"
        self.color: int = 0x00ffff
        self.home_pos: tuple[int, int] = (7, 7)
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.home_pos
        self.direction: Direction = Direction.STOP
        self.speed: int = 2
        self.dead: bool = False
        self.sprite: PmSpPacman = PmSpPacman(self)

    def chase(self) -> None:
        self.move_to(PmGhostStrategy.ride(self.pos))

    def escape(self) -> None:
        self.move_to(self.home_pos)

    def scatter(self) -> None:
        self.move_to(self.corner_pos)

    def move_to(self, pos: tuple[int, int]) -> None:
        self.next_pos = (0, 0)
