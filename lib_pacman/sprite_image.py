class SpriteImage():
    directory: str = "lib_pacman/images/"


class SpPacman(SpriteImage):
    spx0: str = "pacman_x0.png"
    spx1: str = "pacman_x1.png"
    spn0: str = "pacman_n0.png"
    spn1: str = "pacman_n1.png"
    spe0: str = "pacman_e0.png"
    spe1: str = "pacman_e1.png"
    sps0: str = "pacman_s0.png"
    sps1: str = "pacman_s1.png"
    spw0: str = "pacman_w0.png"
    spw1: str = "pacman_w1.png"
    nb_anim: int = 2


class SpGhost(SpriteImage):
    spx0: str = "ghost_0.png"
    spx1: str = "ghost_1.png"
    spn0: str = "ghost_0.png"
    spn1: str = "ghost_1.png"
    spe0: str = "ghost_0.png"
    spe1: str = "ghost_1.png"
    sps0: str = "ghost_0.png"
    sps1: str = "ghost_1.png"
    spw0: str = "ghost_0.png"
    spw1: str = "ghost_1.png"
    nb_anim: int = 2


class SpBlinky(SpGhost):
    spx0: str = "blinky_x0.png"
    spx1: str = "blinky_x1.png"
    spn0: str = "blinky_n0.png"
    spn1: str = "blinky_n1.png"
    spe0: str = "blinky_e0.png"
    spe1: str = "blinky_e1.png"
    sps0: str = "blinky_s0.png"
    sps1: str = "blinky_s1.png"
    spw0: str = "blinky_w0.png"
    spw1: str = "blinky_w1.png"


class SpPinky(SpGhost):
    spx0: str = "pinky_x0.png"
    spx1: str = "pinky_x1.png"
    spn0: str = "pinky_n0.png"
    spn1: str = "pinky_n1.png"
    spe0: str = "pinky_e0.png"
    spe1: str = "pinky_e1.png"
    sps0: str = "pinky_s0.png"
    sps1: str = "pinky_s1.png"
    spw0: str = "pinky_w0.png"
    spw1: str = "pinky_w1.png"


class SpInky(SpGhost):
    spx0: str = "inky_x0.png"
    spx1: str = "inky_x1.png"
    spn0: str = "inky_n0.png"
    spn1: str = "inky_n1.png"
    spe0: str = "inky_e0.png"
    spe1: str = "inky_e1.png"
    sps0: str = "inky_s0.png"
    sps1: str = "inky_s1.png"
    spw0: str = "inky_w0.png"
    spw1: str = "inky_w1.png"


class SpClyde(SpGhost):
    spx0: str = "clyde_x0.png"
    spx1: str = "clyde_x1.png"
    spn0: str = "clyde_n0.png"
    spn1: str = "clyde_n1.png"
    spe0: str = "clyde_e0.png"
    spe1: str = "clyde_e1.png"
    sps0: str = "clyde_s0.png"
    sps1: str = "clyde_s1.png"
    spw0: str = "clyde_w0.png"
    spw1: str = "clyde_w1.png"


class SpScared(SpGhost):
    spx0: str = "scared_0.png"
    spx1: str = "scared_1.png"
    spn0: str = "scared_0.png"
    spn1: str = "scared_1.png"
    spe0: str = "scared_0.png"
    spe1: str = "scared_1.png"
    sps0: str = "scared_0.png"
    sps1: str = "scared_1.png"
    spw0: str = "scared_0.png"
    spw1: str = "scared_1.png"


class SpEndScared(SpGhost):
    spx0: str = "ghost_0.png"
    spx1: str = "ghost_1.png"
    spn0: str = "ghost_0.png"
    spn1: str = "ghost_1.png"
    spe0: str = "ghost_0.png"
    spe1: str = "ghost_1.png"
    sps0: str = "ghost_0.png"
    sps1: str = "ghost_1.png"
    spw0: str = "ghost_0.png"
    spw1: str = "ghost_1.png"


class SpEyes(SpGhost):
    spx0: str = "eyes_0.png"
    spx1: str = "eyes_1.png"
    spn0: str = "eyes_0.png"
    spn1: str = "eyes_1.png"
    spe0: str = "eyes_0.png"
    spe1: str = "eyes_1.png"
    sps0: str = "eyes_0.png"
    sps1: str = "eyes_1.png"
    spw0: str = "eyes_0.png"
    spw1: str = "eyes_1.png"
