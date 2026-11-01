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
    K_h,
    K_r,
    K_s,
    K_c,
    K_f,
    QUIT,
)
from .config import Config
from .pacman import Pacman
from .ghost import Ghost, Blinky, Pinky, Inky, Clyde
from .mood import Mood
from .direction import Direction

from .maze import Maze


class Game():

    surface_score_height:int = 0
    surface_game_height:int = 0
    window_width:int = 0
    window_height:int = 0
    screen:pygame.Surface
    joy: pygame.joystick
    player: Pacman = Pacman()
    ghosts: list[Ghost] = [Blinky(), Pinky(), Inky(), Clyde()]
    bombs: list[tuple[int, int]] = []
    resume:bool = False

    # A deplacer dans la classe qui gere le main menu et la partie
    level:int = 0
    level_time:int = 0
    cheat: bool = True

    def __init__(self) -> None:
        Config()
        Maze()
        Game.surface_score_height = Maze.cell_size * 2
        Game.surface_game_height = Config.height * Maze.cell_size
        Game.window_width = Config.width * Maze.cell_size
        Game.window_height = Game.surface_score_height + Game.surface_game_height

        # pygame setup
        pygame.init()
        pygame.display.set_caption("Pac-Man since 1980")
        Game.screen = pygame.display.set_mode((Game.window_width, Game.window_height))
        # joystick init
        pygame.joystick.init()
        Game.joy = pygame.joystick.Joystick(0)
        self.game_loop()

    def game_loop(self) -> None:
        line_score: str = ""

        # # pygame setup
        # pygame.init()
        # pygame.display.set_caption("Pac-Man since 1980")
        # screen = pygame.display.set_mode((Game.window_width, Game.window_height))
        # Création des deux surfaces
        score_area = pygame.Surface((Game.window_width, Game.surface_score_height))
        game_area = pygame.Surface((Game.window_width, Game.surface_game_height))

        # RESUME Area creation
        resume_area = pygame.Surface((Game.window_width, Game.surface_game_height), pygame.SRCALPHA)
        resume_area.fill((0, 0, 128, 192))
        font = pygame.font.Font(None, 48)
        text = font.render(f"Press < ESC > to exit the game", True, (255, 255, 0))
        resume_area.blit(text, (Game.window_width // 6, Game.surface_game_height // 4))
        text = font.render(f"Press any other key to continue", True, (255, 255, 0))
        resume_area.blit(text, (Game.window_width // 6, Game.surface_game_height // 4 * 2))

        # couleur
        score_area.fill((0, 0, 48))
        game_area.fill((0, 0, 0))
        
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
            running = self.events()

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
            Game.screen.blit(score_area, (0, 0))
            Game.screen.blit(game_area, (0, Game.surface_score_height))
            if Game.resume:
                Game.screen.blit(resume_area, (0, Game.surface_score_height))

            # flip() the display to put your work on screen
            pygame.display.flip()

            if Game.resume:
                running = self.resume_loop()

            clock.tick(60)  # limits FPS to 60

        pygame.quit()

    def events(self) -> bool:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        running:bool = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN \
                or event.type == pygame.JOYHATMOTION \
                or event.type == pygame.JOYAXISMOTION \
                or event.type == pygame.JOYBUTTONDOWN:
                # Was it the Escape key? If so, stop the loop.
                if getattr(event, "key", None) == K_ESCAPE \
                    or getattr(event, "button", None) == 11:
                    Game.resume = True
                elif getattr(event, "key", None) == K_UP \
                    or (getattr(event, "hat", None) == 0 and getattr(event, "value", None) == (0, 1)) \
                    or (getattr(event, "axis", None) == 1 and getattr(event, "value", None) < -0.9):
                    Game.player.next_direction = Direction.NORTH
                elif getattr(event, "key", None) == K_DOWN \
                    or (getattr(event, "hat", None) == 0 and getattr(event, "value", None) == (0, -1)) \
                    or (getattr(event, "axis", None) == 1 and getattr(event, "value", None) > 0.9):
                    Game.player.next_direction = Direction.SOUTH
                elif getattr(event, "key", None) == K_LEFT \
                    or (getattr(event, "hat", None) == 0 and getattr(event, "value", None) == (-1, 0)) \
                    or (getattr(event, "axis", None) == 0 and getattr(event, "value", None) < -0.9):
                    Game.player.next_direction = Direction.WEST
                elif getattr(event, "key", None) == K_RIGHT \
                    or (getattr(event, "hat", None) == 0 and getattr(event, "value", None) == (1, 0)) \
                    or (getattr(event, "axis", None) == 0 and getattr(event, "value", None) > 0.9):
                    Game.player.next_direction = Direction.EST
                # events with cheat mode activated
                if Game.cheat:
                    if getattr(event, "key", None) == K_SPACE \
                        or getattr(event, "button", None) == 0:
                        Game.player.turbo()
                    elif getattr(event, "key", None) == K_x \
                        or getattr(event, "button", None) == 1:
                        Game.bombs.append(Game.player.sprite_pos)
                    elif getattr(event, "key", None) == K_f \
                        or getattr(event, "button", None) == 3:
                        for g in Game.ghosts:
                            g.change_mood(Mood.SCARED)
                    elif getattr(event, "key", None) == K_d \
                        or getattr(event, "button", None) == 2:
                        for g in Game.ghosts:
                            g.change_mood(Mood.DEAD)
                    elif getattr(event, "key", None) == K_h \
                        or getattr(event, "button", None) == 6:
                        for g in Game.ghosts:
                            g.move(g.home_pos)
                    elif getattr(event, "key", None) == K_r \
                        or getattr(event, "button", None) == 7:
                        for g in Game.ghosts:
                            g.change_mood(Mood.RIDE)
                    elif getattr(event, "key", None) == K_s \
                        or getattr(event, "button", None) == 5:
                        for g in Game.ghosts:
                            g.change_mood(Mood.SLEEP)
                    elif getattr(event, "key", None) == K_c \
                        or getattr(event, "button", None) == 8:
                        for g in Game.ghosts:
                            g.change_mood(Mood.CHASE)
                if event.type == pygame.JOYBUTTONDOWN:
                    Game.joy.rumble(0, 1, 100)
        return (running)

    def resume_loop(self) -> bool:
        running:bool = True
        key_down:bool = False
        Game.resume = False
        while not key_down and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == KEYDOWN or event.type == pygame.JOYBUTTONDOWN:
                    key_down = True
                    if getattr(event, "key", None) == K_ESCAPE or getattr(event, "button", None) == 11:
                        running = False
        return (running)
