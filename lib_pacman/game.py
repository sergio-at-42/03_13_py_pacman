import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    K_x,
    K_d,
    QUIT,
)
from .config import Config
from .pacman import Pacman
from .ghost import Ghost, Blinky, Pinky, Inky, Clyde
from .mood import Mood
from .direction import Direction

from .maze import Maze


class Game():

    surface_score_height = 0
    surface_game_height = 0
    window_width = 0
    window_height = 0
    level:int = 0
    level_time:int
    player: Pacman = Pacman()
    ghosts: list[Ghost] = [Blinky(), Pinky(), Inky(), Clyde()]
    bombs: list[tuple[int, int]] = []

    def __init__(self) -> None:
        Config()
        excluded = {Game.player.home_pos} | {g.home_pos for g in Game.ghosts}
        Maze(excluded)
        Game.surface_score_height = Maze.cell_size * 2
        Game.surface_game_height = Config.height * Maze.cell_size
        Game.window_width = Config.width * Maze.cell_size
        Game.window_height = Game.surface_score_height + Game.surface_game_height

        self.game_loop()

    def game_loop(self) -> None:
        line_score: str = ""

        # pygame setup
        pygame.init()
        pygame.display.set_caption("Pac-Man since 1980")
        screen = pygame.display.set_mode((Game.window_width, Game.window_height))
        # Création des deux surfaces
        score_area = pygame.Surface((Game.window_width, Game.surface_score_height))
        game_area = pygame.Surface((Game.window_width, Game.surface_game_height))

        # couleur
        score_area.fill((0, 0, 48))
        game_area.fill((0, 0, 0))
        
        #load sprites
        Maze.load_sprites()
        Game.player.sprite_pos = Game.player.sprite.convert_pos(Game.player.home_pos)
        Game.player.direction = Direction.STOP
        i = 0
        for g in Game.ghosts:
            i += 1
            g.mood = Mood.CHASE
            g.direction = Direction.STOP

        clock = pygame.time.Clock()
        running = True
        while running:

            # DISPLAY SCORE AREA
            score_area.fill((0, 0, 48))
            font = pygame.font.Font(None, 32)
            y=8
            line_score = f"SCORE {Game.player.score}"
            text = font.render(line_score, True, (255, 255, 0))
            score_area.blit(text, (Game.window_width // 4, y))
            y += font.get_linesize()

            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    # Was it the Escape key? If so, stop the loop.
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_UP:
                        Game.player.turn(Direction.NORTH)
                    elif event.key == K_DOWN:
                        Game.player.turn(Direction.SOUTH)
                    elif event.key == K_LEFT:
                        Game.player.turn(Direction.WEST)
                    elif event.key == K_RIGHT:
                        Game.player.turn(Direction.EST)
                    elif event.key == K_SPACE:
                        Game.player.turbo()
                    elif event.key == K_x:
                        self.bombs.append(Game.player.sprite_pos)
                    elif event.key == K_d:
                        for g in self.ghosts:
                            g.mood = Mood.DEAD
                            g.mood_time = -1
                            g.speed = 4

            # fill the screen with a color to wipe away anything from last frame
            game_area.fill((0, 0, 0))
            Maze.draw_maze(game_area)

            # RENDER YOUR GAME HERE
            for b in Game.bombs:
                sprite = pygame.image.load(f"lib_pacman/{Game.player.bomb()}").convert_alpha()
                game_area.blit(sprite, b)

            i = 0
            for g in Game.ghosts:
                i += 1
                sprite = pygame.image.load(f"lib_pacman/{g.sprite.file()}").convert_alpha()
                game_area.blit(sprite, g.sprite_pos)
                g.move()

            sprite = pygame.image.load(f"lib_pacman/{Game.player.sprite.file()}").convert_alpha()
            game_area.blit(sprite, Game.player.sprite_pos)
            Game.player.move()

            # Affichage des deux surfaces dans la fenêtre principale
            screen.blit(score_area, (0, 0))
            screen.blit(game_area, (0, Game.surface_score_height))

            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60

        pygame.quit()
