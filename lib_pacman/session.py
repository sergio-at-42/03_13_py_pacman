
from enum import Enum

import pygame

from lib_pacman.menu import Menu, MenuEntry
from lib_pacman.display_menu import MenuView
from lib_pacman.game import Game


class SessionState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    HIGHSCORES = "highscores"
    INSTRUCTIONS = "instructions"


class Session:
    def __init__(self) -> None:
        self.state = SessionState.MENU
        self.running = True
        self.menu = Menu(levels_count=10)
        self.menu_view = None
        self.game = None
        self.screen = None
        self.clock = None

    def run(self) -> None:
        """Initialize Pygame and run the main loop."""

        pygame.init()

        self.screen = pygame.display.set_mode((Game.window_width, Game.window_height))
        pygame.display.set_caption("Pac-Man")

        self.clock = pygame.time.Clock()
        self.menu_view = MenuView()

        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            # Update the game state based on the current session state
            self.update()

            # Draw the current state (menu, game, etc.)
            self.draw()

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
            # À connecter après le refactoring de Game
            pass

    def handle_menu_input(self, event: pygame.event.Event) -> None:
        """Handle keyboard events in the menu."""

        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            self.running = False

        elif event.key == pygame.K_UP:
            self.menu.up()

        elif event.key == pygame.K_DOWN:
            self.menu.down()

        elif event.key == pygame.K_BACKSPACE:
            self.menu.backspace()

        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            action = self.menu.enter()

            if action is not None:
                self.on_menu_entry(action)

        else:
            self.menu.type_char(event.unicode)

    def on_menu_entry(self, entry: MenuEntry) -> None:
        """Translate a menu action into a session state change."""

        if entry == MenuEntry.START:
            level = self.menu.level
            cheat = self.menu.cheat_mode

            # À connecter après le refactoring de Game
            # self.game = Game(level=level, cheat_mode=cheat)
            # self.state = SessionState.PLAYING

            print(f"Starting game: level={level}, cheat={cheat}")

        elif entry == MenuEntry.HIGHSCORES:
            self.state = SessionState.HIGHSCORES

        elif entry == MenuEntry.INSTRUCTIONS:
            self.state = SessionState.INSTRUCTIONS

        elif entry == MenuEntry.EXIT:
            self.running = False

    def update(self) -> None:
        """Update the active screen."""

        if self.state == SessionState.PLAYING:
            # À connecter après le refactoring de Game
            pass

    # def draw(self) -> None:
    #     """Draw the screen corresponding to the current state."""

    #     if self.state == SessionState.MENU:
    #         self.menu_view.draw(self.screen, self.menu)

    #     elif self.state == SessionState.HIGHSCORES:
    #         self.screen.fill("black")
    #         # La vue des scores sera ajoutée ici.

    #     elif self.state == SessionState.INSTRUCTIONS:
    #         self.screen.fill("black")
    #         # La vue des instructions sera ajoutée ici.

    #     elif self.state == SessionState.PLAYING:
    #         # À connecter après le refactoring de Game
    #         pass

    def draw(self):
        if self.state == SessionState.MENU:
            self.menu_view.draw(self.screen, self.menu)

        elif self.state == SessionState.HIGHSCORES:
            self.draw_simple_screen("HIGH SCORES") # pour tester
    #         # La vue des scores sera ajoutée ici.


        elif self.state == SessionState.INSTRUCTIONS:
            self.draw_simple_screen("INSTRUCTIONS") # pour tester
    #         # La vue des instructions sera ajoutée ici.

        elif self.state == SessionState.PLAYING:
            pass
        # tester instruction et highscores
    def draw_simple_screen(self, title):
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
            center=(self.screen.get_width() // 2, self.screen.get_height() - 50)
        )

        self.screen.blit(hint_surface, hint_rect)

if __name__ == "__main__":
    session = Session()
    session.run()
