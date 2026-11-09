from __future__ import annotations
import pygame
import json
from datetime import datetime

from .config import Config
from .error import Error


class Hiscore():

    file_name: str = "highscores.json"
    all: list[Hiscore] = []
    window:pygame.Surface
    background: pygame.Surface
    hiscore_area:pygame.Surface

    def __init__(self, player: str, score: int, date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")) -> None:
        self.player: str = player
        self.score: int = score
        self.date: str = date
        Hiscore.all.append(self)

    @classmethod
    def read_file(cls) -> None:
        Hiscore.set_file_name()
        try:
            with open(Hiscore.file_name, "r") as hiscore_file:
                hiscore_json = json.load(hiscore_file)
                Hiscore.all.clear()
                for hs in hiscore_json:
                    Hiscore(hs["player"], hs["score"], hs["date"])
                Hiscore.all.sort(key=lambda player: player.score, reverse=True)
        except FileNotFoundError:
            Error("[error]No Hi-Score file found.")
        except json.decoder.JSONDecodeError:
            Error("[error]JSON Hi-Score file corrupted.")

    @classmethod
    def set_file_name(cls) -> None:
        try:
            with open(Config.highscore_file_name, "r"):
                Hiscore.file_name = Config.highscore_file_name
        except FileNotFoundError:
            Error(f"[error]<{Config.highscore_file_name}>  not found. "
                f"<{Hiscore.file_name}> used for Hi-Scores.")

    @classmethod
    def display(cls) -> None:
        from .session import Session
        from .game import Game
        if len(Hiscore.all) == 0:
            Hiscore.read_file()
 
        Hiscore.window = Session.session.window
        Hiscore.background = pygame.Surface(Hiscore.window.get_size(), pygame.SRCALPHA)
        bg: pygame.image = pygame.image.load(f"{Config.hiscore_bg}")
        Hiscore.background.blit(bg, ((Hiscore.background.get_width() - bg.get_width()) // 2, 0))

        Hiscore.hiscore_area = pygame.Surface((864, 896), pygame.SRCALPHA)
        Hiscore.hiscore_area.fill((0, 0, 48, 192))
        # display first line
        y = 64
        font = pygame.font.Font(None, 96)
        text = font.render("H I - S C O R E S", True, (255, 127, 0))
        Hiscore.hiscore_area.blit(text, ((Hiscore.hiscore_area.get_width() - text.get_width()) // 2, y))
        y = 224
        line:int = 0
        for hs in Hiscore.all[0:10]:
            pygame.draw.line(Hiscore.hiscore_area, (255, 127, 0), (32, y + 64 * line - 12), (832, y + 64 * line - 12), 2)
            font = pygame.font.Font(None, 64)
            text = font.render(f"{hs.player}", True, (255, 255, 0))
            Hiscore.hiscore_area.blit(text, (Hiscore.hiscore_area.get_width() // 2 - 400, y + 64 * line))
            text = font.render(f"{hs.score}", True, (255, 255, 0))
            Hiscore.hiscore_area.blit(text, (Hiscore.hiscore_area.get_width() // 2 + 400 - text.get_width(), y + 64 * line))
            line += 1
        # pygame.draw.line(Hiscore.hiscore_area, (192, 192, 0), (400, y + 64 * line - 12), (800, y + 64 * line - 12), 4)

        Hiscore.window.blit(Hiscore.background, (0, 0))
        Hiscore.window.blit(Hiscore.hiscore_area, ((Hiscore.window.get_width() - Hiscore.hiscore_area.get_width()) // 2, 64))
        pygame.display.flip()
        Game.waiting_loop()
