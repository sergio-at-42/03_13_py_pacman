import pygame
from .pm_error import PmError
from .pm_config import PmConfig
from .pm_pacman import PmPacman
from .pm_ghost import PmGhost, PmBlinky, PmPinky, PmInky, PmClyde
from .mood import Mood

from .pm_maze import display_maze


class PmGame():

    player: PmPacman = PmPacman()
    ghosts: list[PmGhost] = [
        PmBlinky(), PmPinky(), PmInky(), PmClyde(), PmGhost()]

    def __init__(self) -> None:
        PmConfig()

        #display_maze()

        self.game_loop()

    def game_loop(self) -> None:
        # pygame setup
        pygame.init()
        pygame.display.set_caption("PAC MAN")
        screen = pygame.display.set_mode((960, 640))
        clock = pygame.time.Clock()
        running = True

        PmGame.player.sprite.pos = (50, 50)
        PmGame.player.direction = 2
        i = 0
        for g in PmGame.ghosts:
            i += 1
            g.sprite.pos = (i*100, i*100)
            g.direction = 2
        
        direction: int = 2

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("blue")

            # RENDER YOUR GAME HERE
            
            i = 0
            for g in PmGame.ghosts:
                i += 1
                sprite = pygame.image.load(f"lib_pacman/{g.sprite.file()}").convert_alpha()
                screen.blit(sprite, g.sprite.pos)

            sprite = pygame.image.load(f"lib_pacman/{PmGame.player.sprite.file()}").convert_alpha()
            screen.blit(sprite, PmGame.player.sprite.pos)

            x, y = g.sprite.pos
            if x <= 500 and y >= 600:
                PmGame.ghosts[1].mood = Mood.RIDE
                PmGame.ghosts[4].mood = Mood.RIDE
                direction = 1
            if x <= 500 and y <= 500:
                PmGame.ghosts[4].mood = Mood.SCARED
                direction = 2
            if x >= 800 and y <= 500:
                PmGame.ghosts[1].mood = Mood.SCARED
                PmGame.ghosts[4].mood = Mood.RIDE
                direction = 4
            if x >= 800 and y >= 600:
                PmGame.ghosts[1].mood = Mood.DEAD
                PmGame.ghosts[4].mood = Mood.SCARED
                direction = 8

            PmGame.player.direction = direction
            for g in PmGame.ghosts:
                g.direction = direction


            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60

        pygame.quit()




######### AFFICHAGE D'UN SPRITE

# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Affichage d'un sprite")

# # Chargement du sprite
# sprite = pygame.image.load("images/player.png").convert_alpha()

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     screen.fill((30, 30, 30))

#     # Affichage du sprite à la position (100, 150)
#     screen.blit(sprite, (100, 150))

#     pygame.display.flip()

# pygame.quit()

######### BROUILLON A SUPPRIMER AVANT REVIEW

        # # RENDER YOUR GAME HERE
        # for y in range(0, 640, 10):
        #     x = y * 960 / 640
        #     # line(0, 640-y, 960 - x, 640)
        #     pygame.draw.aaline(screen, "orange", [0, 640-y], [960 - x, 640], True)
        #     pygame.draw.aaline(screen, "green", [960, y], [x, 0], True)
        # test d'affichage du fichier de log
        # lines = PmError.read_log().splitlines()
        # font = pygame.font.Font(None, 16)
        # y=16
        # for line in lines:
        #     text = font.render(line, True, (255, 0, 0))
        #     screen.blit(text, (16, y))
        #     y += font.get_linesize()
