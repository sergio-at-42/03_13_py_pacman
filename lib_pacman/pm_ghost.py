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
        self.sprite_pos:  tuple[int, int] = self.home_pos * 32
        self.direction: int = 0
        self.speed: int = 1

        self.spn0: str = "images/ghost_0.png"
        self.spn1: str = "images/ghost_1.png"
        self.spe0: str = "images/ghost_0.png"
        self.spe1: str = "images/ghost_1.png"
        self.sps0: str = "images/ghost_0.png"
        self.sps1: str = "images/ghost_1.png"
        self.spw0: str = "images/ghost_0.png"
        self.spw1: str = "images/ghost_1.png"
        self.anim: int = 0

    def chase(self) -> None:
        self.move_to(PmGhostStrategy.ride(self.pos))

    def escape(self) -> None:
        self.move_to(self.home_pos)

    def scatter(self) -> None:
        self.move_to(self.corner_pos)

    def move_to(self, pos: tuple[int, int]) -> None:
        self.next_pos = (0, 0)

    def sprite(self) -> str:
        x, y = self.sprite_pos
        if self.direction == 1:
            y -= self.speed
            nesw = "n"
        if self.direction == 2:
            x += self.speed
            nesw = "e"
        if self.direction == 4:
            y += self.speed
            nesw = "s"
        if self.direction == 8:
            x -= self.speed
            nesw = "w"
        self.sprite_pos = (x, y)
        self.anim = (datetime.now().microsecond // 250000) % 2
        sprite = getattr(self, f"sp{nesw}{str(self.anim)}")
        return (sprite)

class PmBlinky(PmGhost):
    def __init__(self) -> None:
        super().__init__()
        self.name = "blinky"
        self.color: int = 0xFF0000
        self.home_pos: tuple[int, int] = (5, 3)
        self.corner_pos: tuple[int, int] = (0, 0)
        self.pos: tuple[int, int] = self.home_pos
        self.speed = 2

        self.spn0 = "images/blinky_n0.png"
        self.spn1 = "images/blinky_n1.png"
        self.spe0 = "images/blinky_e0.png"
        self.spe1 = "images/blinky_e1.png"
        self.sps0 = "images/blinky_s0.png"
        self.sps1 = "images/blinky_s1.png"
        self.spw0 = "images/blinky_w0.png"
        self.spw1 = "images/blinky_w1.png"

    def chase(self) -> None:
        self.move_to(PmGhostStrategy.ride(self.pos))


class PmPinky(PmGhost):
    def __init__(self) -> None:
        super().__init__()
        self.name = "pinky"
        self.color: int = 0xFFc0c0
        self.home_pos: tuple[int, int] = (6, 3)
        self.corner_pos: tuple[int, int] = (PmConfig.width-1, 0)
        self.pos: tuple[int, int] = self.home_pos

        self.spn0 = "images/pinky_n0.png"
        self.spn1 = "images/pinky_n1.png"
        self.spe0 = "images/pinky_e0.png"
        self.spe1 = "images/pinky_e1.png"
        self.sps0 = "images/pinky_s0.png"
        self.sps1 = "images/pinky_s1.png"
        self.spw0 = "images/pinky_w0.png"
        self.spw1 = "images/pinky_w1.png"

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

        self.spn0 = "images/inky_n0.png"
        self.spn1 = "images/inky_n1.png"
        self.spe0 = "images/inky_e0.png"
        self.spe1 = "images/inky_e1.png"
        self.sps0 = "images/inky_s0.png"
        self.sps1 = "images/inky_s1.png"
        self.spw0 = "images/inky_w0.png"
        self.spw1 = "images/inky_w1.png"

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
        self.speed = 1.5

        self.spn0 = "images/clyde_n0.png"
        self.spn1 = "images/clyde_n1.png"
        self.spe0 = "images/clyde_e0.png"
        self.spe1 = "images/clyde_e1.png"
        self.sps0 = "images/clyde_s0.png"
        self.sps1 = "images/clyde_s1.png"
        self.spw0 = "images/clyde_w0.png"
        self.spw1 = "images/clyde_w1.png"

    def chase(self) -> None:
        self.move_to(PmGhostStrategy.ride(self.pos))

