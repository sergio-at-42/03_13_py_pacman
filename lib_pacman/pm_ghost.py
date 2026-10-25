from random import randrange
from .pm_config import PmConfig
# from .pm_ghost_strategy import PmGhostStrategy
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
        self.next_pos: tuple[int, int] = ()
        self.target_pos: tuple[int, int] = ()
        self.direction: int = 0
        self.speed: int = 1
        self.mood: Mood = Mood.RIDE
        # self.strategy: PmGhostStrategy = PmGhostStrategy(self)
        self.sprite: PmSpGhost = PmSpGhost(self)

    def move(self, pos: tuple[int, int] = ()) -> None:
        from .pm_game import PmGame
        if pos != ():
            self.mood = Mood.GO
            self.ghost.target_pos = pos
        if self.ghost.pos == self.ghost.next_pos:
            # self.strategy.next_move()
            if self.ghost.mood is Mood.RIDE:
                self.ghost.target_pos = (randrange(PmConfig.width), randrange(PmConfig.height))
            elif self.ghost.mood is Mood.SCATTER:
                self.ghost.target_pos = self.ghost.corner_pos
            elif self.ghost.mood is Mood.DEAD:
                self.ghost.target_pos = self.ghost.home_pos
            elif self.ghost.mood is Mood.SCARED:
                pass
            elif self.ghost.mood is Mood.CHASE:
                self.ghost.target_pos = PmGame.player.pos
    
            if self.ghost.mood is Mood.SLEEP:
                self.ghost.direction = 0
            else:
                self.bfs(self.ghost.target_pos)

    def bfs(self) -> None:
        # trouver next_pos et direction
        self.next_pos = (7, 7)
        self.direction = 0

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


class PmPinky(PmGhost):
    def __init__(self) -> None:
        super().__init__()
        self.name = "pinky"
        self.color: int = 0xffc0c0
        self.home_pos: tuple[int, int] = (6, 3)
        self.corner_pos: tuple[int, int] = (PmConfig.width-1, 0)
        self.pos: tuple[int, int] = self.home_pos
        self.sprite = PmSpPinky(self)


class PmInky(PmGhost):
    def __init__(self) -> None:
        super().__init__()
        self.name = "inky"
        self.color: int = 0x0000ff
        self.home_pos: tuple[int, int] = (7, 3)
        self.corner_pos: tuple[int, int] = (PmConfig.width-1, PmConfig.height)
        self.pos: tuple[int, int] = self.home_pos
        self.sprite = PmSpInky(self)


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
