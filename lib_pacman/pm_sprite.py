from datetime import datetime
from .mood import Mood
from .direction import Direction

class PmSprite():
    directory: str = "images/"

    def __init__(self) -> None:
        self.pos: tuple[int, int] = (32, 32)


class PmSpPacman(PmSprite):
    spn0 = "pacman_n0.png"
    spn1 = "pacman_n1.png"
    spe0 = "pacman_e0.png"
    spe1 = "pacman_e1.png"
    sps0 = "pacman_s0.png"
    sps1 = "pacman_s1.png"
    spw0 = "pacman_w0.png"
    spw1 = "pacman_w1.png"
    anim: int = 2

    def __init__(self, player) -> None:
        self.player = player

    def file(self) -> str:
        sprite: PmSprite = self
        # direction: str = "n"
        anim: int = 0
        x, y = self.pos
        if self.player.direction == Direction.NORTH:
            y -= self.player.speed
            # direction = "n"
        if self.player.direction == Direction.EST:
            x += self.player.speed
            # direction = "e"
        if self.player.direction == Direction.SOUTH:
            y += self.player.speed
            # direction = "s"
        if self.player.direction == Direction.WEST:
            x -= self.player.speed
            # direction = "w"
        self.pos = (x, y)
        anim = (datetime.now().microsecond // 250000) % self.anim
        if self.player.dead:
            sprite = PmSpEyes(self.player)
        file = f"{getattr(sprite, f"sp{self.player.direction.value}{str(anim)}")}"
        return (f"{self.directory}{file}")


class PmSpGhost(PmSprite):
    spn0: str = "ghost_0.png"
    spn1: str = "ghost_1.png"
    spe0: str = "ghost_0.png"
    spe1: str = "ghost_1.png"
    sps0: str = "ghost_0.png"
    sps1: str = "ghost_1.png"
    spw0: str = "ghost_0.png"
    spw1: str = "ghost_1.png"
    anim: int = 2

    def __init__(self, ghost) -> None:
        super().__init__()
        self.ghost = ghost

    def file(self) -> str:
        sprite: PmSprite = self
        # direction: str = "n"
        anim: int = 0
        next_pos = tuple(p * 48 + 8 for p in self.ghost.next_pos)
        x, y = self.pos
        if self.ghost.direction == Direction.NORTH:
            y -= self.ghost.speed
            # direction = "n"
        if self.ghost.direction == Direction.EST:
            x += self.ghost.speed
            # direction = "e"
        if self.ghost.direction == Direction.SOUTH:
            y += self.ghost.speed
            # direction = "s"
        if self.ghost.direction == Direction.WEST:
            x -= self.ghost.speed
            # direction = "w"
        self.pos = (x, y)
        if self.pos == next_pos:
            self.ghost.pos = self.ghost.next_pos
        anim = (datetime.now().microsecond // 250000) % self.anim
        if self.ghost.mood == Mood.SCARED:
            sprite = PmSpScared(self.ghost)
        if self.ghost.mood == Mood.DEAD:
            sprite = PmSpEyes(self.ghost)
        print(f"{self.ghost.direction.value}")
        file = f"{getattr(sprite, f"sp{self.ghost.direction.value}{str(anim)}")}"
        return (f"{self.directory}{file}")

class PmSpBlinky(PmSpGhost):
    spn0 = "blinky_n0.png"
    spn1 = "blinky_n1.png"
    spe0 = "blinky_e0.png"
    spe1 = "blinky_e1.png"
    sps0 = "blinky_s0.png"
    sps1 = "blinky_s1.png"
    spw0 = "blinky_w0.png"
    spw1 = "blinky_w1.png"


class PmSpPinky(PmSpGhost):
    spn0 = "pinky_n0.png"
    spn1 = "pinky_n1.png"
    spe0 = "pinky_e0.png"
    spe1 = "pinky_e1.png"
    sps0 = "pinky_s0.png"
    sps1 = "pinky_s1.png"
    spw0 = "pinky_w0.png"
    spw1 = "pinky_w1.png"


class PmSpInky(PmSpGhost):
    spn0 = "inky_n0.png"
    spn1 = "inky_n1.png"
    spe0 = "inky_e0.png"
    spe1 = "inky_e1.png"
    sps0 = "inky_s0.png"
    sps1 = "inky_s1.png"
    spw0 = "inky_w0.png"
    spw1 = "inky_w1.png"


class PmSpClyde(PmSpGhost):
    spn0 = "clyde_n0.png"
    spn1 = "clyde_n1.png"
    spe0 = "clyde_e0.png"
    spe1 = "clyde_e1.png"
    sps0 = "clyde_s0.png"
    sps1 = "clyde_s1.png"
    spw0 = "clyde_w0.png"
    spw1 = "clyde_w1.png"


class PmSpScared(PmSpGhost):
    spn0 = "scared_0.png"
    spn1 = "scared_1.png"
    spe0 = "scared_0.png"
    spe1 = "scared_1.png"
    sps0 = "scared_0.png"
    sps1 = "scared_1.png"
    spw0 = "scared_0.png"
    spw1 = "scared_1.png"


class PmSpEyes(PmSpGhost):
    spn0 = "eyes_0.png"
    spn1 = "eyes_1.png"
    spe0 = "eyes_0.png"
    spe1 = "eyes_1.png"
    sps0 = "eyes_0.png"
    sps1 = "eyes_1.png"
    spw0 = "eyes_0.png"
    spw1 = "eyes_1.png"
