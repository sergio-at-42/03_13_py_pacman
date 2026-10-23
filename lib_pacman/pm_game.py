import pygame
from .pm_error import PmError
from .pm_config import PmConfig
from .pm_maze import display_maze


class PmGame():

    def __init__(self) -> None:
        PmConfig()
        display_maze()

        # self.game_loop()

    def game_loop(self) -> None:
        # pygame setup
        pygame.init()
        screen = pygame.display.set_mode((960, 640))
        clock = pygame.time.Clock()
        running = True

        # flip() the display to put your work on screen
        pygame.display.flip()
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("black")

            # RENDER YOUR GAME HERE
            

            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60

        pygame.quit()



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
