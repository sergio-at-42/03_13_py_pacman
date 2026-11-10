from __future__ import annotations
from typing import Any
import sys
import json

from .error import Error, \
    WidthLessThan2Error, WidthSmallFor42Error, \
    HeightLessThan2Error, WidthSmallFor42Error, \
    LivesLessThan1Error, TimeLessThan0Error

class Config():

    highscore_file_name: str = "highscores.json"
    level: list[int] = []  # array of multiple levels ???
    width: int = 16
    height: int = 16
    lives: int = 3
    pacgum: int = 42
    spacgum: int = 4
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    fps: int = 60

    sprite_42: str = "lib_pacman/images/tardis.png"
    sprite_pacgum: str = "lib_pacman/images/pacgum.png"
    sprite_super: str = "lib_pacman/images/super.png"
    game_over: str = "lib_pacman/images/game_over.png"
    game_bg_l: str = "lib_pacman/images/pac-man-background-l.jpg"
    game_bg_r: str = "lib_pacman/images/pac-man-background-r.jpg"
    menu_bg: str = "lib_pacman/images/pac-man-smile.jpg"
    hiscore_bg: str = "lib_pacman/images/pac-man-ce2.jpg"
    instruction_bg: str = "lib_pacman/images/pac-man-ce2.jpg"
    # menu_bg: str = "lib_pacman/images/pac-man-ce1.jpg"
    # menu_bg: str = "lib_pacman/images/pac-man-ce2.jpg"
    pm_icon : str = "\U0001F6BD"
    argv: list[str] = sys.argv
    config_file_name: str = ""

    def __init__(self) -> None:
        Config.config_read_file()

    @classmethod
    def config_read_file(cls) -> None:
        Config.file_from_argv()
        config_file: dict[str, Any] = {}
        try:
            with open(Config.config_file_name, "r") as config_json_file:
                config_file = json.load(config_json_file)
                Config.set_values(config_file)
        except FileNotFoundError:
            Error("[error]No configuration file found.")
        except json.decoder.JSONDecodeError:
            Error("[error]JSON config file corrupted.")

    @classmethod
    def file_from_argv(cls) -> None:
        try:
            with open(Config.argv[1], "r"):
                Config.config_file_name = Config.argv[1]
        except IndexError:
            Error("[error]No configuration file provide. "
                f"Usage: {Config.argv[0].rpartition("/")[2]} <conf_file>. "
                "Default values used to create the Pac-Man.")
        except FileNotFoundError:
            Error(f"[error]<{Config.argv[1]}> is not a configuration file. "
                f"Usage: {Config.argv[0].rpartition("/")[2]} <conf_file>. "
                "Default values used to create the Pac-Man.")

    @classmethod
    def set_values(cls, config_file: dict[str, Any]) -> None:
        for key, value in config_file.items():
            if hasattr(Config, key):
                if isinstance(value, type(getattr(Config, key))):
                    if Config.verify_value(key, value):
                        setattr(Config, key, value)

    @classmethod
    def verify_value(cls, key: str, value: Any) -> bool:
        value_ok = True
        try:
            match key:
                case "width":
                    if value < 2:
                        raise WidthLessThan2Error
                    # if value < PATTERN_W + 2:
                    #     raise WidthSmallFor42Error
                case "height":
                    if value < 2:
                        raise HeightLessThan2Error
                    # if value < PATTERN_H + 2:
                    #     raise HeightToSmallFor42Error
                case "lives":
                    if value < 1:
                        raise LivesLessThan1Error
                case "level_max_time":
                    if value < 0:
                        raise TimeLessThan0Error
                case "pacgum":
                    if value < 0:
                        raise WidthLessThan2Error
                case "spacgum":
                    if value < 0:
                        raise WidthLessThan2Error
                case "points_per_pacgum":
                    if value < 0:
                        raise WidthLessThan2Error
                case "points_per_super_pacgum":
                    if value < 0:
                        raise WidthLessThan2Error
                case "points_per_ghost":
                    if value < 0:
                        raise WidthLessThan2Error
                case "seed":
                    if value < 0:
                        raise WidthLessThan2Error
                case "level_max_time":
                    if value < 0:
                        raise WidthLessThan2Error
                case _:
                    value_ok = False
        except Error:
            value_ok = False
        return (value_ok)
