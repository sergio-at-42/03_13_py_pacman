
# import pygame
# import sys

# pygame.init()

# screen = pygame.display.set_mode((720, 720))
# pygame.display.set_caption("Start Menu Example")

# WHITE = (255,255,255)
# LIGHT = (170,170,170)
# DARK = (100,100,100)
# BG = (60,25,60)

# font = pygame.font.SysFont("Corbel", 40)

# def game():
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#         screen.fill((40, 40, 40))

#         text = font.render("Game Started!", True, WHITE)
#         screen.blit(text, (250, 350))

#         pygame.display.update()

# def start_menu():

#     while True:

#         screen.fill(BG)
#         mouse = pygame.mouse.get_pos()

#         play_button = pygame.Rect(300, 300, 140, 50)
#         quit_button = pygame.Rect(300, 380, 140, 50)

#         pygame.draw.rect(screen, LIGHT if play_button.collidepoint(mouse) else DARK, play_button)
#         pygame.draw.rect(screen, LIGHT if quit_button.collidepoint(mouse) else DARK, quit_button)

#         play_text = font.render("Play", True, WHITE)
#         quit_text = font.render("Quit", True, WHITE)

#         screen.blit(play_text, (335, 305))
#         screen.blit(quit_text, (335, 385))

#         for event in pygame.event.get():

#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#             if event.type == pygame.MOUSEBUTTONDOWN:

#                 if play_button.collidepoint(mouse):
#                     game()

#                 if quit_button.collidepoint(mouse):
#                     pygame.quit()
#                     sys.exit()

#         pygame.display.update()

# start_menu()


from enum import Enum


class MenuEntry(Enum):
    """Entries displayed in the main menu."""

    START = "Start Game"
    LEVEL = "Level"
    CHEAT = "Cheat mode"
    HIGHSCORES = "View Highscores"
    INSTRUCTIONS = "Instructions"
    EXIT = "Exit"


class Menu:
    """Manage menu navigation and player options."""

    def __init__(self, levels_count: int = 10) -> None:
        self.entries: list[MenuEntry] = list(MenuEntry)
        self.selected: int = 0
        self.levels_count: int = max(1, levels_count)
        self.level_input: str = ""
        self.cheat_mode: bool = False

    def current(self) -> MenuEntry:
        """Return the currently selected entry."""
        return self.entries[self.selected]

    def up(self) -> None:
        """Move the selection one entry up."""
        self.selected = (self.selected - 1) % len(self.entries)

    def down(self) -> None:
        """Move the selection one entry down."""
        self.selected = (self.selected + 1) % len(self.entries)

    @property
    def level(self) -> int:
        """Return a valid level, defaulting to level 1."""
        if not self.level_input:
            return 1
        return int(self.level_input)

    def type_char(self, char: str) -> None:
        """Add a digit to the level input if it is valid."""
       
        if self.current() != MenuEntry.LEVEL:
            return

        if len(char) != 1 or char not in "0123456789":
            return

        candidate = self.level_input + char

        if 1 <= int(candidate) <= self.levels_count:
            self.level_input = candidate

    def backspace(self) -> None:
        """Remove the last digit from the level input."""
        if self.current() == MenuEntry.LEVEL:
            self.level_input = self.level_input[:-1]

    def enter(self) -> MenuEntry | None:
        """Return an action, or update a menu option."""
        entry = self.current()

        if entry == MenuEntry.CHEAT:
            self.cheat_mode = not self.cheat_mode
            return None

        if entry == MenuEntry.LEVEL:
            return None #a voir encore comment faire pour que le niveau soit pris en compte dans le jeu

        return entry

    def label(self, entry: MenuEntry) -> str:
        """Return the text displayed for a menu entry."""
        if entry == MenuEntry.LEVEL:
            return f"Level : " # a voir encore comment faire pour que le niveau soit pris en compte dans le jeu

        if entry == MenuEntry.CHEAT:
            status = "ON" if self.cheat_mode else "OFF"
            return f"Cheat Mode: {status}"

        return entry.value

