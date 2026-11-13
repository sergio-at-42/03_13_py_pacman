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
            return None

        return entry

    def label(self, entry: MenuEntry) -> str:
        """Return the text displayed for a menu entry."""
        if entry == MenuEntry.LEVEL:
            return "Level : "

        if entry == MenuEntry.CHEAT:
            status = "ON" if self.cheat_mode else "OFF"
            return f"Cheat Mode: {status}"

        return entry.value  # type: ignore
