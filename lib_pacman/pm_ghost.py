from datetime import datetime
from .pm_config import PmConfig
from .pm_ghost_strategy import PmGhostStrategy
from .pm_sprite import PmSpGhost, PmSpBlinky, PmSpPinky, PmSpInky, PmSpClyde
from .mood import Mood

N, E, S, W = 1, 2, 4, 8





class PmGhost():

    def __init__(self) -> None:
        self.name: str = "Gogo"
        self.color: int = 0xffffff
        self.home_pos: tuple[int, int] = (7, 7)
        self.corner_pos: tuple[int, int] = (7, 7)
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.home_pos
        # self.sprite_pos:  tuple[int, int] = self.home_pos
        self.direction: int = 0
        self.speed: int = 1
        self.mood: Mood = Mood.RIDE
        # self.scared: bool = False
        # self.dead: bool = False
        # self.anim: int = 0
        self.sprite: PmSpGhost = PmSpGhost(self)

    def chase(self) -> None:
        self.move_to(PmGhostStrategy.ride(self.pos))

    def escape(self) -> None:
        self.move_to(self.home_pos)

    def scatter(self) -> None:
        self.move_to(self.corner_pos)

    def move_to(self, pos: tuple[int, int]) -> None:
        if self.ghost.pos == self.ghost.next_pos:
            pass # calculer la nest_pos et la direction


class PmBlinky(PmGhost):
    def __init__(self) -> None:
        super().__init__()
        self.name = "blinky"
        self.color: int = 0xff0000
        self.home_pos: tuple[int, int] = (5, 3)
        self.corner_pos: tuple[int, int] = (0, 0)
        self.pos: tuple[int, int] = self.home_pos
        self.speed = 1.6
        self.sprite = PmSpBlinky(self)

    def chase(self) -> None:
        self.move_to(PmGhostStrategy.ride(self.pos))


class PmPinky(PmGhost):
    def __init__(self) -> None:
        super().__init__()
        self.name = "pinky"
        self.color: int = 0xffc0c0
        self.home_pos: tuple[int, int] = (6, 3)
        self.corner_pos: tuple[int, int] = (PmConfig.width-1, 0)
        self.pos: tuple[int, int] = self.home_pos
        self.sprite = PmSpPinky(self)

    def chase(self) -> None:
        self.move_to(PmGhostStrategy.ride(self.pos))


class PmInky(PmGhost):
    def __init__(self) -> None:
        super().__init__()
        self.name = "inky"
        self.color: int = 0x0000ff
        self.home_pos: tuple[int, int] = (7, 3)
        self.corner_pos: tuple[int, int] = (PmConfig.width-1, PmConfig.height)
        self.pos: tuple[int, int] = self.home_pos
        self.sprite = PmSpInky(self)

    def chase(self) -> None:
        self.move_to(PmGhostStrategy.ride(self.pos))


class PmClyde(PmGhost):
    def __init__(self) -> None:
        super().__init__()
        self.name = "clyde"
        self.color: int = 0xff7f00
        self.home_pos: tuple[int, int] = (8, 3)
        self.corner_pos: tuple[int, int] = (0, PmConfig.height)
        self.pos: tuple[int, int] = self.home_pos
        self.speed = 1.3
        self.sprite = PmSpClyde(self)

    def chase(self) -> None:
        self.move_to(PmGhostStrategy.ride(self.pos))
