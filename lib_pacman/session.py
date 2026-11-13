from __future__ import annotations
from random import randint, seed
from enum import Enum

import pygame

from .error import Error
from .config import Config
from .hiscore import Hiscore
from .instruction import Instruction
from .maze import Maze
from lib_pacman.menu import Menu, MenuEntry
from lib_pacman.display_menu import MenuView


class SessionState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    HIGHSCORES = "highscores"
    INSTRUCTIONS = "instructions"


class Session:

    session: Session

    def __init__(self) -> None:
        Config()
        Session.session = self
        self.state = SessionState.MENU
        self.running = True
        self.menu = Menu(levels_count=10)
        # self.game = None
        self.fps: int = 60
        self.menu_view: MenuView
        self.window: pygame.Surface
        self.screen: pygame.Surface
        self.clock: pygame.time.ClockType

        self.level: int = 1
        self.level_time: int = 90
        self.next_level: bool = False
        self.game_over: bool = False
        self.cheat: bool = True
        self.background_image = pygame.image.load(f"{Config.menu_bg}")
        Maze()

    def run(self) -> None:
        """Initialize Pygame and run the main loop."""

        pygame.init()
        # joystick init
        pygame.joystick.init()
        # if pygame.joystick.get_count() > 0:
        #     joy = pygame.joystick.Joystick(0)
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        bg_center_x = int((
            self.window.get_width() - self.background_image.get_width()) / 2)
        pygame.display.set_caption("Pac-Man")
        self.screen = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)

        self.clock = pygame.time.Clock()
        self.menu_view = MenuView()

        while self.running:
            # background display
            self.window.blit(self.background_image, (bg_center_x, 0))

            for event in pygame.event.get():
                self.handle_event(event)

            # Draw the current state (menu, game, etc.)
            self.draw()

            self.window.blit(self.screen, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_event(self, event: pygame.event.Event) -> None:
        """Dispatch events according to the current state."""

        if event.type == pygame.QUIT:
            self.running = False
            return

        if self.state == SessionState.MENU:
            self.handle_menu_input(event)

        elif self.state == SessionState.HIGHSCORES:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = SessionState.MENU

        elif self.state == SessionState.INSTRUCTIONS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = SessionState.MENU

        elif self.state == SessionState.PLAYING:
            self.state = SessionState.MENU

    def handle_menu_input(self, event: pygame.event.Event) -> None:
        """Handle keyboard events in the menu."""

        if event.type != pygame.KEYDOWN \
            and event.type != pygame.JOYHATMOTION \
            and event.type != pygame.JOYAXISMOTION \
                and event.type != pygame.JOYBUTTONDOWN:
            return

        if getattr(event, "key", None) == pygame.K_ESCAPE \
                or getattr(event, "button", None) == 11:
            self.running = False

        # elif getattr(event, "key", None) == pygame.K_UP \
        #     or (getattr(
        #         event, "hat", None) == 0 and getattr(
        #             event, "value", None) == (0, 1)) or (getattr(
        #                 event, "axis", None) == 1 and getattr(
        #                     event, "value", None) < -0.9):
        #     self.menu.up()

        # elif getattr(event, "key", None) == pygame.K_DOWN \
        #     or (getattr(event, "hat", None) == 0 and getattr(
        #         event, "value", None) == (0, -1)) or (getattr(
        #             event, "axis", None) == 1 and getattr(
        #                 event, "value", None) > 0.9):
        #     self.menu.down()

        value = getattr(event, "value", None)

        if (
            getattr(event, "key", None) == pygame.K_UP
            or (
                getattr(event, "hat", None) == 0
                and value == (0, 1)
            )
            or (
                getattr(event, "axis", None) == 1
                and isinstance(value, (int, float))
                and value < -0.9
            )
        ):
            self.menu.up()

        elif (
            getattr(event, "key", None) == pygame.K_DOWN
            or (
                getattr(event, "hat", None) == 0
                and value == (0, -1)
            )
            or (
                getattr(event, "axis", None) == 1
                and isinstance(value, (int, float))
                and value > 0.9
            )
        ):
            self.menu.down()

        elif getattr(event, "key", None) == pygame.K_BACKSPACE:
            self.menu.backspace()

        elif getattr(event, "key", None) in (pygame.K_RETURN, pygame.K_SPACE) \
                or getattr(event, "button", None) == 0:
            action = self.menu.enter()

            if action is not None:
                self.on_menu_entry(action)

        else:
            self.menu.type_char(getattr(event, "unicode", ""))

    def on_menu_entry(self, entry: MenuEntry) -> None:
        """Translate a menu action into a session state change."""

        if entry == MenuEntry.START:

            self.state = SessionState.PLAYING

        elif entry == MenuEntry.HIGHSCORES:
            self.state = SessionState.HIGHSCORES

        elif entry == MenuEntry.INSTRUCTIONS:
            self.state = SessionState.INSTRUCTIONS

        elif entry == MenuEntry.EXIT:
            self.running = False

    def draw(self) -> None:
        if self.state == SessionState.MENU:
            self.menu_view.draw(self.screen, self.menu)

        elif self.state == SessionState.HIGHSCORES:
            Hiscore.display()
            self.state = SessionState.MENU

        elif self.state == SessionState.INSTRUCTIONS:
            Instruction.display()
            self.state = SessionState.MENU

        elif self.state == SessionState.PLAYING:
            # start game
            self.game_session()
            self.state = SessionState.MENU

    def draw_simple_screen(self, title: str) -> None:
        self.screen.fill("black")

        title_font = pygame.font.Font(None, 70)
        text_surface = title_font.render(title, True, "yellow")

        text_rect = text_surface.get_rect(
            center=(self.screen.get_width() // 2, 100)
        )

        self.screen.blit(text_surface, text_rect)

        hint_font = pygame.font.Font(None, 30)
        hint_surface = hint_font.render(
            "Press ESC to return to menu",
            True,
            "white"
        )

        hint_rect = hint_surface.get_rect(
            center=(
                self.screen.get_width() // 2, self.screen.get_height() - 50)
        )

        self.screen.blit(hint_surface, hint_rect)

    def game_session(self) -> None:
        from .game import Game
        from .pacman import Pacman
        # initialise level
        self.game_over = False
        self.next_level = False
        self.level = self.menu.level
        self.cheat = self.menu.cheat_mode
        self.new_level()
        # initialise Pacman
        Pacman.player = Pacman()
        Error.write_log(
            f"[info]Starting game: level={self.level}, cheat={self.cheat}")
        # write starting game in log file
        while not self.game_over:
            Game()
            if self.next_level:
                if self.level < 10:
                    self.level += 1
                    self.new_level()
                    self.next_level = False
                else:
                    Game.main_area.blit(
                        Game.victory_area, (0, Game.area_score_height))
                    Game.window.blit(Game.main_area, Game.main_area_center)
                    pygame.display.flip()
                    Game.waiting_loop()
                    self.game_over = True
        if Game.loose or self.next_level:
            Hiscore.input()

    def new_level(self) -> None:
        if self.level == 1:
            self.level_time = 90
            self.fps = Config.fps
        else:
            seed()
            Config.width = randint(9, 32)
            Config.height = randint(9, 20)
            Config.pacgum = randint(1, Config.width * Config.height - 22)
            self.level_time = Config.pacgum // 2 + 60
            if self.level >= 8:
                self.fps = int(Config.fps * 2)
            elif self.level >= 5:
                self.fps = int(Config.fps * 1.5)
        Maze.new_maze()
