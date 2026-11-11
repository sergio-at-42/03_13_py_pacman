import pygame
from pygame.locals import (
    QUIT,
    KEYDOWN,
    TEXTINPUT,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_RETURN,
    K_ESCAPE,
    K_BACKSPACE,
    K_SPACE,
    K_x,
    K_d,
    K_h,
    K_r,
    K_s,
    K_c,
    K_f,
    K_l,
    JOYHATMOTION,
    JOYAXISMOTION,
    JOYBUTTONDOWN,
)
from .config import Config
from .session import Session
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

    window:pygame.Surface
    background: pygame.Surface
    main_area:pygame.Surface
    score_area:pygame
    game_area: pygame.Surface
    resume_area: pygame.Surface
    game_over_area: pygame.Surface
    joy: pygame.joystick

    area_score_height: int = 0
    area_game_height: int = 0
    main_area_width: int = 0
    main_area_height: int = 0
    main_area_center: tuple[int, int] = (0, 0)
    resume:bool = False
    remain_time: float = 0
    loose: bool = False
    fps: int = 60 # limits FPS to 60

    font_size: int = 64
    font: pygame.font

    def __init__(self) -> None:
        # Game.window = pygame.display.set_mode( (0, 0), pygame.FULLSCREEN)
        Game.window = Session.session.window
        Game.area_score_height = Maze.cell_size * 2
        Game.area_game_height = Config.height * Maze.cell_size
        Game.main_area_width = Config.width * Maze.cell_size
        Game.main_area_height = Game.area_score_height + Game.area_game_height
        Game.main_area_center = (
            (Game.window.get_width() - Game.main_area_width) // 2,
            (Game.window.get_height() - Game.main_area_height) // 2)

        pygame.display.set_caption("Pac-Man since 1980")
        # set main game window background
        Game.background = pygame.Surface(Game.window.get_size(), pygame.SRCALPHA)
        bg: pygame.image = pygame.image.load(f"{Config.game_bg}")
        Game.background.blit(bg, ((Game.background.get_width() - bg.get_width()) // 2, 0))

        # Game.main_area = pygame.display.set_mode((Game.main_area_width, Game.main_area_height))
        Game.main_area = pygame.Surface((Game.main_area_width, Game.main_area_height), pygame.SRCALPHA)
        # Création des deux surfaces
        Game.score_area = pygame.Surface((Game.main_area_width, Game.area_score_height), pygame.SRCALPHA)
        Game.game_area = pygame.Surface((Game.main_area_width, Game.area_game_height), pygame.SRCALPHA)
        # initialise font for score area
        if Config.width < 13:
            Game.font_size = 48
        else:
            Game.font_size = 64
        Game.font = pygame.font.Font(None, Game.font_size)

        # RESUME Area creation
        Game.resume_area = pygame.Surface((Game.main_area_width, Game.area_game_height), pygame.SRCALPHA)
        Game.resume_area.fill((0, 0, 128, 192))
        font = pygame.font.Font(None, 48)
        text = font.render(f"Press < ESC > to exit the game", True, (255, 255, 0))
        Game.resume_area.blit(text, (Game.main_area_width // 6, Game.area_game_height // 4))
        text = font.render(f"Press any other key to continue", True, (255, 255, 0))
        Game.resume_area.blit(text, (Game.main_area_width // 6, Game.area_game_height // 4 * 2))

        # GAME OVER Area creation
        Game.game_over_area = pygame.Surface((Game.main_area_width, Game.area_game_height), pygame.SRCALPHA)
        Game.game_over_area.fill((0, 0, 128, 192))
        image = pygame.image.load(f"{Config.game_over}").convert_alpha()
        Game.game_over_area.blit(image, ((Game.main_area_width - image.get_width()) // 2, (Game.area_game_height - image.get_height()) // 2))

        # joystick init
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            Game.joy = pygame.joystick.Joystick(0)

        # initialise ghosts
        Ghost.ghosts.clear()
        Ghost.sprites.empty()
        Blinky(), Pinky(), Inky(), Clyde()
        Ghost.move_ghosts_to_home_position()
        Game.remain_time = Session.session.level_time
        # Initialise Pacman start position
        Pacman.player.init_start_position()

        Game.fps = Session.session.fps
        # start game
        Game.loose = False
        Game.game_loop()

    @classmethod
    def game_loop(cls) -> None:

        #load sprites
        Maze.load_sprites()
    
        # initialise pacgums
        excluded = {Pacman.player.home_pos} | {g.home_pos for g in Ghost.ghosts}
        Maze.pellets = Pacgum.place_pacgums(Maze.grid, excluded)

        # START GAME LOOP
        clock = pygame.time.Clock()
        while not Session.session.game_over and not Session.session.next_level:

            # display background on main game window and initialise main area
            Game.window.blit(Game.background, (0, 0))
            Game.main_area.fill((0, 0, 0, 0))

            # poll for events
            Game.events()

            # DISPLAY GAME AREA
            # fill the game area with a color to wipe away anything from last frame
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
                    Pacman.player.score += Config.points_per_ghost * Pacman.player.points_multiplier
                    Pacman.player.points_multiplier *= 2
                else:
                    if g.ghost.mood != Mood.DEAD and Pacman.player.dead == 0:
                        Pacman.player.dead = 1
                        Ghost.move_ghosts_to_home_position()

            # decrease time
            if Game.remain_time <= 0:
                Game.loose = True
            elif Pacman.player.dead == 0:
                Game.remain_time -= 1 / Game.fps

            # update score arera
            Game.update_score_area()

            # Display the 2 areas in the main area
            Game.main_area.blit(Game.score_area, (0, 0))
            Game.main_area.blit(Game.game_area, (0, Game.area_score_height))

            # if Game Over, verify the number of lives left
            if Game.loose:
                Pacman.player.lives -= 1
                if Pacman.player.lives == 0 or Game.remain_time <= 0:
                    Session.session.game_over = True
                    Game.main_area.blit(Game.game_over_area, (0, Game.area_score_height))
                else:
                    Pacman.player.init_start_position()
                    Game.loose = False

            # Display the resume area
            if Game.resume:
                Game.main_area.blit(Game.resume_area, (0, Game.area_score_height))

            # display the main area and flip() the display to put your work on screen
            Game.window.blit(Game.main_area, Game.main_area_center)
            pygame.display.flip()

            # waiting loop for game over
            # if Pacman.player.lives == 0 or Game.remain_time <= 0:
            if Game.loose:
                Game.waiting_loop()

            # waiting loop for resume
            if Game.resume:
                Game.resume_loop()

            clock.tick(Game.fps)

    @classmethod
    def events(cls) -> None:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == QUIT:
                Session.session.game_over = True
            elif event.type == KEYDOWN \
                or event.type == JOYHATMOTION \
                or event.type == JOYAXISMOTION \
                or event.type == JOYBUTTONDOWN:
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
                if Session.session.cheat:
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
                    elif getattr(event, "key", None) == K_l \
                        or getattr(event, "button", None) == 10:
                        Session.session.next_level = True
                if event.type == JOYBUTTONDOWN and hasattr(Game, "joy"):
                    Game.joy.rumble(0, 1, 100)

    @classmethod
    def resume_loop(cls) -> None:
        key_down:bool = False
        Game.resume = False
        while not key_down:
            for event in pygame.event.get():
                if event.type == QUIT:
                    key_down = True
                    Session.session.game_over = True
                elif event.type == KEYDOWN or event.type == JOYBUTTONDOWN:
                    key_down = True
                    if getattr(event, "key", None) == K_ESCAPE or getattr(event, "button", None) == 11:
                        Session.session.game_over = True

    @classmethod
    def waiting_loop(cls) -> None:
        key_down:bool = False
        while not key_down:
            for event in pygame.event.get():
                if event.type == QUIT:
                    key_down = True
                    Session.session.game_over = True
                elif event.type == KEYDOWN or event.type == JOYBUTTONDOWN:
                    key_down = True

    @classmethod
    def input_loop(cls, window: pygame.Surface, area: pygame.Rect, font: pygame.font, max_char: int = 16) -> str:
        input_area = pygame.Surface(area.size, pygame.SRCALPHA)
        input_str: str = ""
        input_valid:bool = False
        while not input_valid:
            for event in pygame.event.get():
                if event.type == QUIT:
                    input_str = ""
                    input_valid = True
                elif event.type == TEXTINPUT:
                    if len(input_str) < max_char:
                        input_str += getattr(event, "text", "")
                elif event.type == KEYDOWN or event.type == JOYBUTTONDOWN:
                    if getattr(event, "key", None) == K_ESCAPE \
                        or getattr(event, "button", None) == 11:
                        input_str = ""
                        input_valid = True
                    elif getattr(event, "key", None) == K_RETURN \
                        or getattr(event, "button", None) == 0:
                        input_valid = True
                    elif getattr(event, "key", None) == K_BACKSPACE:
                        if len(input_str) > 0:
                            input_str = input_str[:-1]
            input_area.fill((255, 127, 0, 192))
            text = font.render(input_str, True, (255, 255, 0))
            input_area.blit(text, ((input_area.get_width() - text.get_width()) // 2, (input_area.get_height() - text.get_height()) // 2))
            window.blit(input_area, area.topleft)
            # pygame.display.flip()
            pygame.display.update(area)
        return (input_str.strip())

    @classmethod
    def update_score_area(cls) -> None:
        # update score area display
        Game.score_area.fill((0, 0, 48, 192))
        # display first line
        y = 8
        text = Game.font.render("SCORE", True, (255, 255, 0))
        Game.score_area.blit(text, (Game.main_area_width // 4 - text.get_width() // 2, y))
        text = Game.font.render("TIME", True, (255, 255, 0))
        Game.score_area.blit(text, (Game.main_area_width // 2 - text.get_width() // 2, y))
        font = pygame.font.Font(None, int(Game.font_size // 2))
        text = font.render("LEVEL", True, (255, 255, 0))
        Game.score_area.blit(text, (Game.main_area_width * 4 // 6 - text.get_width() // 2, y))
        font = pygame.font.Font(None, int(Game.font_size // 2))
        text = font.render("HI-SCORE", True, (255, 255, 0))
        Game.score_area.blit(text, (Game.main_area_width * 5 // 6 - text.get_width() // 2, y))
        # y += font.get_linesize() + 16
        # display second line
        # font = pygame.font.Font(None, Game.font_size)
        y = Game.area_score_height - Game.font.get_linesize()
        text = Game.font.render(f"{Pacman.player.score}", True, (255, 255, 0))
        Game.score_area.blit(text, (Game.main_area_width // 4 - text.get_width() // 2, y))
        text = Game.font.render(f"{int(Game.remain_time)}", True, (255, 255, 0))
        Game.score_area.blit(text, (Game.main_area_width // 2 - text.get_width() // 2, y))
         # display level
        font = pygame.font.Font(None, int(Game.font_size // 2))
        text = font.render(f"{Session.session.level}", True, (255, 255, 0))
        Game.score_area.blit(text, (Game.main_area_width * 4 // 6 - text.get_width() // 2, y - 16))
        # display hi-score
        font = pygame.font.Font(None, int(Game.font_size // 2))
        text = font.render("0123456789", True, (255, 255, 0))
        Game.score_area.blit(text, (Game.main_area_width * 5 // 6 - text.get_width() // 2, y - 16))
        # display remaining lives
        sprite: SpriteImage = SpPacman()
        anim: int = (pygame.time.get_ticks() // 250000) % sprite.nb_anim
        file = f"{getattr(sprite, f"spe{str(anim)}")}"
        live_image = pygame.image.load(f"{SpriteImage.directory}{file}").convert_alpha()
        x = Game.main_area_width - live_image.get_rect().width - 16
        y = Game.area_score_height - live_image.get_rect().height - 4
        for _ in range(Pacman.player.lives - 1):
            Game.score_area.blit(live_image, (x, y))
            x -= live_image.get_rect().width + 16
