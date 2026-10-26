import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from .pm_error import PmError
from .pm_config import PmConfig
from .pm_pacman import PmPacman
from .pm_ghost import PmGhost, PmBlinky, PmPinky, PmInky, PmClyde
from .mood import Mood
from .direction import Direction

from .maze import Maze


class PmGame():

    player: PmPacman = PmPacman()
    ghosts: list[PmGhost] = [PmBlinky(), PmPinky(), PmInky(), PmClyde()]

    def __init__(self) -> None:
        PmConfig()
        Maze()

        self.game_loop()

    def game_loop(self) -> None:
        # pygame setup
        pygame.init()
        pygame.display.set_caption("Pac-Man")
        screen = pygame.display.set_mode((Maze.window_width, Maze.window_height))
        # Création des deux surfaces
        score_area = pygame.Surface((Maze.window_width, Maze.surface_score_height))
        game_area = pygame.Surface((Maze.window_width, Maze.surface_game_height))
        # couleur
        score_area.fill((30, 40, 80))
        game_area.fill((0, 0, 0))

        

        PmGame.player.sprite.pos = PmGame.player.sprite.convert_pos(PmGame.player.home_pos)
        PmGame.player.direction = Direction.STOP
        i = 0
        for g in PmGame.ghosts:
            i += 1
            g.mood = Mood.SCATTER
            g.direction = Direction.STOP

        # direction pour test
        # direction: Direction = Direction.EST

        clock = pygame.time.Clock()
        running = True
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    # Was it the Escape key? If so, stop the loop.
                    if event.key == K_ESCAPE:
                        running = False

            # fill the screen with a color to wipe away anything from last frame
            game_area.fill((0, 0, 0))
            Maze.draw_maze(game_area)

            # RENDER YOUR GAME HERE
            i = 0
            for g in PmGame.ghosts:
                i += 1
                sprite = pygame.image.load(f"lib_pacman/{g.sprite.file()}").convert_alpha()
                game_area.blit(sprite, g.sprite_pos)
                g.move()

            sprite = pygame.image.load(f"lib_pacman/{PmGame.player.sprite.file()}").convert_alpha()
            game_area.blit(sprite, PmGame.player.sprite.pos)

            # x, y = g.sprite.pos
            # if x <= 248 and y >= 488:
            #     PmGame.ghosts[1].mood = Mood.RIDE
            #     PmGame.ghosts[4].mood = Mood.RIDE
            #     direction = Direction.NORTH
            # if x <= 248 and y <= 248:
            #     PmGame.ghosts[4].mood = Mood.SCARED
            #     direction = Direction.EST
            # if x >= 728 and y <= 248:
            #     PmGame.ghosts[1].mood = Mood.SCARED
            #     PmGame.ghosts[4].mood = Mood.RIDE
            #     direction = Direction.SOUTH
            # if x >= 728 and y >= 488:
            #     PmGame.ghosts[1].mood = Mood.DEAD
            #     PmGame.ghosts[4].mood = Mood.SCARED
            #     direction = Direction.WEST

            # PmGame.player.direction = direction
            # for g in PmGame.ghosts:
            #     g.direction = direction


            # Affichage des deux surfaces dans la fenêtre principale
            screen.blit(score_area, (0, 0))
            screen.blit(game_area, (0, Maze.surface_score_height))

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
