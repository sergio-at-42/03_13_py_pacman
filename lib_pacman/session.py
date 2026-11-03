from enum import Enum
from lib_pacman.menu import Menu, MenuEntry
from lib_pacman.game import Game

class SessionState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    HIGHSCORES = "highscores"
    INSTRUCTIONS = "instructions"


class Session:
    def __init__(self) -> None:
        self.state: SessionState = SessionState.MENU
        self.running: bool = True
        self.menu: Menu = Menu(levels_count=10)
        self.game: Game | None = None
        # window, clock and MenuView are created in run(), after pygame.init()

  