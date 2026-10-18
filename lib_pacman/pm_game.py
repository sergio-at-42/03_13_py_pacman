import pygame
from .pm_config import PmConfig


class PmGame():

    def __init__(self) -> None:
        self.cfg: PmConfig = PmConfig()
        self.game_loop()

        print(f"{vars(self.cfg)}")

    def game_loop(self) -> None:
        self.my_beautiful_loop()

    def my_beautiful_loop(self) -> None:
        # pygame setup
        pygame.init()
        screen = pygame.display.set_mode((960, 640))
        clock = pygame.time.Clock()
        running = True

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("black")

            # RENDER YOUR GAME HERE
            for y in range(0, 640, 10):
                x = y * 960 / 640
                # line(0, 640-y, 960 - x, 640)
                pygame.draw.aaline(screen, "orange", [0, 640-y], [960 - x, 640], True)
                pygame.draw.aaline(screen, "green", [960, y], [x, 0], True)

            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60

        pygame.quit()
