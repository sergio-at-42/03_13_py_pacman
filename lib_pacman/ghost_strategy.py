from random import randrange
from .config import Config
# from .game import Game
# from .pacman import Pacman
# from .ghost import Ghost, Blinky, Pinky, Inky, Clyde

from .mood import Mood


################    FICHIER A SUPPRIMER 


class GhostStrategy():

    def __init__(self, ghost) -> None:
        self.ghost = ghost

    def next_move(self) -> None:
        if self.ghost.mood is Mood.RIDE:
            self.ghost.target_pos = (randrange(Config.width), randrange(Config.height))
        elif self.ghost.mood is Mood.SCATTER:
            self.ghost.target_pos = self.ghost.corner_pos
        elif self.ghost.mood is Mood.DEAD:
            self.ghost.target_pos = self.ghost.home_pos
        elif self.ghost.mood is Mood.SCARED:
            pass
        elif self.ghost.mood is Mood.CHASE:
            self.ghost.target_pos = Game.player.pos

        if self.ghost.mood is Mood.SLEEP:
            self.ghost.direction = 0
        else:
            self.bfs(self.ghost.target_pos)

    def bfs(self, target_pos: tuple[int, int]) -> None:
        # trouver next_pos et direction
        self.ghost.next_pos = (x, y)
        self.ghost.direction = 0