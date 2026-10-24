from random import randrange
from .pm_config import PmConfig
from .pm_game import PmGame
# from .pm_pacman import PmPacman
# from .pm_ghost import PmGhost, PmBlinky, PmPinky, PmInky, PmClyde

from .mood import Mood


class PmGhostStrategy():

    def __init__(self, ghost) -> None:
        self.ghost = ghost

    def next_move(self) -> None:
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

    def bfs(self, target_pos: tuple[int, int]) -> None:
        # trouver next_pos et direction
        self.ghost.next_pos = (x, y)
        self.ghost.direction = 0