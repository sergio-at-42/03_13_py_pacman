from lib_pacman.menu import Menu, MenuEntry
from .config import Config
import pygame


class MenuView:
    def __init__(self) -> None:
        pygame.font.init()

        self.title_font = pygame.font.Font(None, 80)
        self.entry_font = pygame.font.Font(None, 50)
        self.hint_font = pygame.font.Font(None, 28)

        self.text_color = pygame.Color("white")
        self.selection_color = pygame.Color("yellow")
        self.background_color = pygame.Color((0, 0, 0, 128))
        self.level_frame_color = pygame.Color("gray")
        self.hint_color = pygame.Color("gray")

    def draw(self, surface: pygame.Surface, menu: Menu,
             top_scores: list[int] | None = None) -> None:
        """Draw the complete main menu."""

        # pygame.draw.rect(surface, self.background_color, surface.get_rect())
        surface.fill(self.background_color)

        self.draw_title(surface)
        self.draw_entries(surface, menu)
        self.draw_hints(surface)

        if top_scores is not None:
            self.draw_top_scores(surface, top_scores)

    def draw_title(self, surface: pygame.Surface) -> None:
        """Draw the game title at the top of the menu."""
        # Récupérer la largeur de la surface avec surface.get_width().
        # Rendre le texte "PAC-MAN".
        # Centrer le texte horizontalement.
        width = surface.get_width()
        title_text = self.title_font.render("PAC-MAN", True, self.text_color)
        draw_centered_text(surface, title_text, width // 2, 50)

    def draw_entries(self, surface: pygame.Surface, menu: Menu) -> None:
        """Draw the menu entries, highlighting the selected one."""
        # Parcourir menu.entries avec enumerate().
        # Comparer l'index à menu.selected.
        # Utiliser menu.label(entry) pour obtenir le texte.
        # Appliquer une couleur différente à la ligne sélectionnée.
        
        width = surface.get_width()

        for index, entry in enumerate(menu.entries):
            color = self.selection_color if index == menu.selected else self.text_color

            entry_text = self.entry_font.render(menu.label(entry), True, color)
            

            # Position du texte
            y = 150 + index * 60

            if entry == MenuEntry.LEVEL:
                # draw_centered_text(surface, entry_text, width // 2, y)
                entry_rect = entry_text.get_rect(midright=(width // 2 - 15, y))
                surface.blit(entry_text, entry_rect)


                # Afficher le champ de saisie à droite de LEVEL
                self.draw_level_input(surface, menu, y - 20)

            else:
                draw_centered_text(surface, entry_text, width // 2, y)
            

    def draw_level_input(self, surface: pygame.Surface,
                         menu: Menu, y: int) -> None:
        """Draw the level input box and the current input string."""
        # Dessiner un rectangle pour le niveau.
        # Rendre le texte du niveau avec menu.level_input.
        # Centrer le texte dans le rectangle.
        width = surface.get_width()
        frame_color = (
        self.selection_color
        if menu.entries[menu.selected] == MenuEntry.LEVEL
        else self.level_frame_color
    )
        # level_rect = pygame.Rect(width // 2 - 50, y, 100, 40)
        level_rect = pygame.Rect(width // 2 + 5, y, 100, 40)
        pygame.draw.rect(surface, frame_color, level_rect, 2)
        level_text = self.entry_font.render(menu.level_input, True, self.text_color)
        level_text_rect = level_text.get_rect(center=level_rect.center)
        surface.blit(level_text, level_text_rect)

    def draw_hints(self, surface: pygame.Surface) -> None:
        """Draw the key hints at the bottom of the menu."""
        hint_text = self.hint_font.render("UP / DOWN: Navigate     ENTER: Select",
        True,
        self.hint_color
        )
        draw_centered_text(surface, hint_text, surface.get_width() // 2, surface.get_height() - 30)

    def draw_top_scores(self, surface: pygame.Surface,
                        scores: list[int] | None = None) -> None:
        """Draw the top scores on the menu."""
        # Dessiner les scores en haut à droite de l'écran.
        width = surface.get_width()
        for index, score in enumerate(scores):
            score_text = self.hint_font.render(f"{index + 1}. {score}", True, self.text_color)
            score_rect = score_text.get_rect(topright=(width - 20, 20 + index * 30))
            surface.blit(score_text, score_rect)

# on peut la transmettre dans display utils sert a centrer le texte sur l'écran
def draw_centered_text(surface: pygame.Surface,
    text_surface: pygame.Surface,
    center_x: int,
    center_y: int) -> None:
    """Draw a text surface centered at the given coordinates."""

    text_rect = text_surface.get_rect(center=(center_x, center_y))
    surface.blit(text_surface, text_rect)