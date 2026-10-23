from datetime import datetime
from .pm_config import PmConfig
from .pm_ghost_strategy import PmGhostStrategy

class PmGhost():

    def __init__(self) -> None:
        self.name: str = "Gogo"
        self.color: int = 0xFFFFFF
        self.home_pos: tuple[int, int] = (7, 7)
        self.corner_pos: tuple[int, int] = (7, 7)
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.home_pos
        self.direction: int = 0

        self.spe0: str = "images/ghost_0.png"
        self.spe1: str = "images/ghost_1.png"
        self.sp: bool = False

    def chase(self) -> None:
        self.move_to(PmGhostStrategy.ride(self.pos))

    def escape(self) -> None:
        self.move_to(self.home_pos)

    def scatter(self) -> None:
        self.move_to(self.corner_pos)

    def move_to(self, pos: tuple[int, int]) -> None:
        self.next_pos = (0, 0)

    def sprite(self) -> str:
        if self.sp:
            sprite = self.spe1
        else:
            sprite = self.spe0
        self.sp = (datetime.now().microsecond // 250000) % 2 > 0
        return (sprite)

class PmBlinky(PmGhost):
    def __init__(self) -> None:
        super().__init__()
        self.name: str = "blinky"
        self.color: int = 0xFF0000
        self.home_pos: tuple[int, int] = (5, 3)
        self.corner_pos: tuple[int, int] = (0, 0)
        self.pos: tuple[int, int] = self.home_pos

        self.spe0 = "images/blinky_e0.png"
        self.spe1 = "images/blinky_e1.png"

    def chase(self) -> None:
        self.move_to(PmGhostStrategy.ride(self.pos))


class PmPinky(PmGhost):
    def __init__(self) -> None:
        super().__init__()
        self.name: str = "pinky"
        self.color: int = 0xFFc0c0
        self.home_pos: tuple[int, int] = (6, 3)
        self.corner_pos: tuple[int, int] = (PmConfig.width-1, 0)
        self.pos: tuple[int, int] = self.home_pos

        self.spe0 = "images/pinky_e0.png"
        self.spe1 = "images/pinky_e1.png"

    def chase(self) -> None:
        self.move_to(PmGhostStrategy.ride(self.pos))


class PmInky(PmGhost):
    def __init__(self) -> None:
        super().__init__()
        self.name: str = "inky"
        self.color: int = 0x0000ff
        self.home_pos: tuple[int, int] = (7, 3)
        self.corner_pos: tuple[int, int] = (PmConfig.width-1, PmConfig.height)
        self.pos: tuple[int, int] = self.home_pos

        self.spe0 = "images/inky_e0.png"
        self.spe1 = "images/inky_e1.png"

    def chase(self) -> None:
        self.move_to(PmGhostStrategy.ride(self.pos))


class PmClyde(PmGhost):
    def __init__(self) -> None:
        super().__init__()
        self.name: str = "clyde"
        self.color: int = 0xff7f00
        self.home_pos: tuple[int, int] = (8, 3)
        self.corner_pos: tuple[int, int] = (0, PmConfig.height)
        self.pos: tuple[int, int] = self.home_pos

        self.spe0 = "images/clyde_e0.png"
        self.spe1 = "images/clyde_e1.png"

    def chase(self) -> None:
        self.move_to(PmGhostStrategy.ride(self.pos))

