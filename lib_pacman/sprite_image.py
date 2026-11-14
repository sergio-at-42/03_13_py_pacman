class SpriteImage():
    sp: str = "tardis.png"
    nb_anim: int = 1


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


class SpPacmanExplosion(SpriteImage):
    sp0: str = "pacman_explosion_0.png"
    sp1: str = "pacman_explosion_1.png"
    sp2: str = "pacman_explosion_2.png"
    sp3: str = "pacman_explosion_3.png"
    sp4: str = "pacman_explosion_4.png"
    sp5: str = "pacman_explosion_5.png"
    sp6: str = "pacman_explosion_6.png"
    sp7: str = "pacman_explosion_7.png"
    sp8: str = "pacman_explosion_8.png"
    sp9: str = "pacman_explosion_9.png"
    sp10: str = "pacman_explosion_10.png"
    nb_anim: int = 11


class SpEatPacman(SpriteImage):
    sp0: str = "ghost_eat_pacman_0.png"
    sp1: str = "ghost_eat_pacman_1.png"
    sp2: str = "ghost_eat_pacman_2.png"
    sp3: str = "ghost_eat_pacman_3.png"
    sp4: str = "ghost_eat_pacman_4.png"
    sp5: str = "ghost_eat_pacman_5.png"
    sp6: str = "ghost_eat_pacman_6.png"
    sp7: str = "ghost_eat_pacman_7.png"
    sp8: str = "ghost_eat_pacman_8.png"
    sp9: str = "ghost_eat_pacman_9.png"
    nb_anim: int = 10


class SpBomb(SpriteImage):
    sp0: str = "bomb_0.png"
    sp1: str = "bomb_1.png"
    sp2: str = "bomb_2.png"
    sp3: str = "bomb_3.png"
    sp4: str = "bomb_4.png"
    sp5: str = "bomb_5.png"
    sp6: str = "bomb_6.png"
    sp7: str = "bomb_7.png"
    nb_anim: int = 8


class SpExplosion(SpriteImage):
    sp0: str = "explosion_0.png"
    sp1: str = "explosion_1.png"
    sp2: str = "explosion_2.png"
    sp3: str = "explosion_3.png"
    sp4: str = "explosion_4.png"
    sp5: str = "explosion_5.png"
    sp6: str = "explosion_6.png"
    sp7: str = "explosion_7.png"
    sp8: str = "explosion_8.png"
    sp9: str = "explosion_9.png"
    nb_anim: int = 10


class SpItem(SpriteImage):
    sptardis: str = "tardis.png"
    spgum: str = "pacgum.png"
    spsuper: str = "super.png"
    splogo: str = "pacman-logo.png"
    nb_anim: int = 1
