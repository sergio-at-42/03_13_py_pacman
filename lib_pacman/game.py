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
from .config import Config
from .pacman import Pacman
from .ghost import Ghost, Blinky, Pinky, Inky, Clyde
from .mood import Mood
from .direction import Direction

from .maze import Maze


class Game():

    player: Pacman = Pacman()
    ghosts: list[Ghost] = [Blinky(), Pinky(), Inky(), Clyde()]

    def __init__(self) -> None:
        Config()
        Maze()

        self.game_loop()

    def game_loop(self) -> None:
        # pygame setup
        pygame.init()
        pygame.display.set_caption("Pac-Man since 1980")
        screen = pygame.display.set_mode((Maze.window_width, Maze.window_height))
        # Création des deux surfaces
        score_area = pygame.Surface((Maze.window_width, Maze.surface_score_height))
        game_area = pygame.Surface((Maze.window_width, Maze.surface_game_height))
        # couleur
        score_area.fill((0, 0, 48))
        game_area.fill((0, 0, 0))

        

        Game.player.sprite.pos = Game.player.sprite.convert_pos(Game.player.home_pos)
        Game.player.direction = Direction.STOP
        i = 0
        for g in Game.ghosts:
            i += 1
            g.mood = Mood.SCATTER
            g.direction = Direction.STOP
        Game.ghosts[1].mood = Mood.CHASE
        Game.ghosts[3].mood = Mood.RIDE

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
            for g in Game.ghosts:
                i += 1
                sprite = pygame.image.load(f"lib_pacman/{g.sprite.file()}").convert_alpha()
                game_area.blit(sprite, g.sprite_pos)
                g.move()

            sprite = pygame.image.load(f"lib_pacman/{Game.player.sprite.file()}").convert_alpha()
            game_area.blit(sprite, Game.player.sprite.pos)

            # Affichage des deux surfaces dans la fenêtre principale
            screen.blit(score_area, (0, 0))
            screen.blit(game_area, (0, Maze.surface_score_height))

            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60

        pygame.quit()
