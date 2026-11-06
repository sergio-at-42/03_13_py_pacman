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
from .bomb import Bomb
from .explosion import Explosion
from .sprite_image import SpriteImage, SpPacman
from .mood import Mood
from .pacgum import Pacgum
from .direction import Direction

from .maze import Maze


class Game():

    surface_score_height:int = 0
    surface_game_height:int = 0
    window_width:int = 0
    window_height:int = 0
    screen:pygame.Surface
    joy: pygame.joystick
    resume:bool = False

    # A deplacer dans la classe qui gere le main menu et la partie
    level:int = 0
    level_time:int = 0
    next_level: bool = False
    game_over: bool = False
    cheat: bool = True

    def __init__(self) -> None:
        Maze()
        Game.surface_score_height = Maze.cell_size * 2
        Game.surface_game_height = Config.height * Maze.cell_size
        Game.window_width = Config.width * Maze.cell_size
        Game.window_height = Game.surface_score_height + Game.surface_game_height

        # pygame setup
        pygame.init()
        pygame.display.set_caption("Pac-Man since 1980")
        Game.screen = pygame.display.set_mode((Game.window_width, Game.window_height))
        # Création des deux surfaces
        Game.score_area = pygame.Surface((Game.window_width, Game.surface_score_height), pygame.SRCALPHA)
        Game.game_area = pygame.Surface((Game.window_width, Game.surface_game_height), pygame.SRCALPHA)
        # joystick init
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            Game.joy = pygame.joystick.Joystick(0)
        Game.game_loop()

    @classmethod
    def game_loop(cls) -> None:
        line_score: str = ""

        # set main game screen background
        background = pygame.image.load(f"{Config.game_area_bg}")

        #load sprites
        Maze.load_sprites()

        # RESUME Area creation
        resume_area = pygame.Surface((Game.window_width, Game.surface_game_height), pygame.SRCALPHA)
        resume_area.fill((0, 0, 128, 192))
        font = pygame.font.Font(None, 48)
        text = font.render(f"Press < ESC > to exit the game", True, (255, 255, 0))
        resume_area.blit(text, (Game.window_width // 6, Game.surface_game_height // 4))
        text = font.render(f"Press any other key to continue", True, (255, 255, 0))
        resume_area.blit(text, (Game.window_width // 6, Game.surface_game_height // 4 * 2))

        # initialise Pacman
        Pacman.player = Pacman()
        # initialise ghosts
        Blinky(), Pinky(), Inky(), Clyde()
        # initialise pacgums
        excluded = {Pacman.player.home_pos} | {g.home_pos for g in Ghost.ghosts}
        Maze.pellets = Pacgum.place_pacgums(Maze.grid, excluded)

        # Initialise Pacman start position
        Pacman.player.init_start_position()

        # START GAME LOOP
        clock = pygame.time.Clock()
        while not Game.game_over and not Game.next_level:

            # display main game screen for background
            Game.screen.blit(background, (0, 0))

            # update score arera
            Game.update_score_area()

            # poll for events
            Game.events()

            # DISPLAY GAME AREA
            # fill the screen with a color to wipe away anything from last frame
            Game.game_area.fill((0, 0, 48, 127))
            Maze.draw_maze(Game.game_area)

            # display bombs
            for b in list(Bomb.bombs):
                b.danger()
                Game.game_area.blit(b.sprite.image, b.sprite.rect)
            # display explosions
            for e in list(Explosion.explosions):
                e.boum()
                Game.game_area.blit(e.sprite.image, e.sprite.rect)
            # display ghosts
            for g in Ghost.ghosts:
                g.move()
                Game.game_area.blit(g.sprite.image, g.sprite.rect)
            # display pacman
            Pacman.player.move()
            Game.game_area.blit(Pacman.player.sprite.image, Pacman.player.sprite.rect)

            # manage colisions between pacman and ghosts
            ghosts_hit_list = pygame.sprite.spritecollide(Pacman.player.sprite, Ghost.sprites, False, pygame.sprite.collide_rect_ratio(0.75))
            for g in ghosts_hit_list:
                if g.ghost.mood == Mood.SCARED:
                    g.ghost.change_mood(Mood.DEAD)
                    Pacman.player.score += Config.points_per_ghost
                else:
                    if g.ghost.mood != Mood.DEAD:
                        Pacman.player.dead = 1

            # Display the 2 areas in the main window
            Game.screen.blit(Game.score_area, (0, 0))
            Game.screen.blit(Game.game_area, (0, Game.surface_score_height))
            # Display the resume area
            if Game.resume:
                Game.screen.blit(resume_area, (0, Game.surface_score_height))

            # flip() the display to put your work on screen
            pygame.display.flip()

            # if Game Over, verify the number of lives left
            if Game.game_over and Pacman.player.live > 0:
                Pacman.player.init_start_position()
                Game.game_over = False

            # waiting loop for resume
            if Game.resume:
                Game.resume_loop()

            clock.tick(60)  # limits FPS to 60

        pygame.quit()

    @classmethod
    def events(cls) -> None:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Pacman.player.live = 0
                Game.game_over = True
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
                    Pacman.player.next_direction = Direction.NORTH
                elif getattr(event, "key", None) == K_DOWN \
                    or (getattr(event, "hat", None) == 0 and getattr(event, "value", None) == (0, -1)) \
                    or (getattr(event, "axis", None) == 1 and getattr(event, "value", None) > 0.9):
                    Pacman.player.next_direction = Direction.SOUTH
                elif getattr(event, "key", None) == K_LEFT \
                    or (getattr(event, "hat", None) == 0 and getattr(event, "value", None) == (-1, 0)) \
                    or (getattr(event, "axis", None) == 0 and getattr(event, "value", None) < -0.9):
                    Pacman.player.next_direction = Direction.WEST
                elif getattr(event, "key", None) == K_RIGHT \
                    or (getattr(event, "hat", None) == 0 and getattr(event, "value", None) == (1, 0)) \
                    or (getattr(event, "axis", None) == 0 and getattr(event, "value", None) > 0.9):
                    Pacman.player.next_direction = Direction.EST
                # events with cheat mode activated
                if Game.cheat:
                    if getattr(event, "key", None) == K_SPACE \
                        or getattr(event, "button", None) == 0:
                        Pacman.player.turbo()
                    elif getattr(event, "key", None) == K_x \
                        or getattr(event, "button", None) == 1:
                        Bomb(Pacman.player.pos)
                    elif getattr(event, "key", None) == K_f \
                        or getattr(event, "button", None) == 3:
                        for g in Ghost.ghosts:
                            g.change_mood(Mood.SCARED)
                    elif getattr(event, "key", None) == K_d \
                        or getattr(event, "button", None) == 2:
                        for g in Ghost.ghosts:
                            g.change_mood(Mood.DEAD)
                    elif getattr(event, "key", None) == K_h \
                        or getattr(event, "button", None) == 6:
                        for g in Ghost.ghosts:
                            g.move(g.home_pos)
                    elif getattr(event, "key", None) == K_r \
                        or getattr(event, "button", None) == 7:
                        for g in Ghost.ghosts:
                            g.change_mood(Mood.RIDE)
                    elif getattr(event, "key", None) == K_s \
                        or getattr(event, "button", None) == 5:
                        for g in Ghost.ghosts:
                            g.change_mood(Mood.SLEEP)
                    elif getattr(event, "key", None) == K_c \
                        or getattr(event, "button", None) == 8:
                        for g in Ghost.ghosts:
                            g.change_mood(Mood.CHASE)
                if event.type == pygame.JOYBUTTONDOWN and hasattr(Game, "joy"):
                    Game.joy.rumble(0, 1, 100)

    @classmethod
    def resume_loop(cls) -> None:
        key_down:bool = False
        Game.resume = False
        while not key_down:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    key_down = True
                    Game.game_over = True
                elif event.type == KEYDOWN or event.type == pygame.JOYBUTTONDOWN:
                    key_down = True
                    if getattr(event, "key", None) == K_ESCAPE or getattr(event, "button", None) == 11:
                        Game.game_over = True

    @classmethod
    def update_score_area(cls) -> None:
        Game.score_area.fill((0, 0, 48, 0))
        y=8
        font = pygame.font.Font(None, 32)
        line_score = f"SCORE {Pacman.player.score}"
        text = font.render(line_score, True, (255, 255, 0))
        Game.score_area.blit(text, (Game.window_width // 4, y))
        y += font.get_linesize() + 8

        sprite: SpriteImage = SpPacman()
        anim: int = (pygame.time.get_ticks() // 250000) % sprite.nb_anim
        file = f"{getattr(sprite, f"spe{str(anim)}")}"
        live_image = pygame.image.load(f"{SpriteImage.directory}{file}").convert_alpha()
        x = Game.window_width - live_image.get_rect().width - 16
        y = Game.surface_score_height - live_image.get_rect().height - 8
        for _ in range(Pacman.player.live):
            Game.score_area.blit(live_image, (x, y))
            x -= live_image.get_rect().width + 16
