from __future__ import annotations
from typing import Any
import sys
from pathlib import Path
import json

from .error import Error, \
    WidthLessThan2Error, WidthSmallFor42Error, \
    HeightLessThan2Error, WidthSmallFor42Error, \
    LivesLessThan1Error, TimeLessThan0Error, \
    PacGumLessThan0Error, SuperPacGumLessThan0Error, \
    PacGumTooBigError , SuperPacGumTooBigError, \
    PointPerPacgumLessThan0Error, PointPerSuperPacgumLessThan0Error, \
    PointPerGhostLessThan0Error, ConfigTypeError, ConfigKeyError

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

    image_directory: str = "lib_pacman/images/"
    sprite_42: str = "tardis.png"
    sprite_pacgum: str = "pacgum.png"
    sprite_super: str = "super.png"
    logo: str = "pacman-logo.png"
    game_over: str = "game_over.png"
    victory: str = "victory.png"
    game_bg: str = "pac-man-background.jpg"
    menu_bg: str = "pac-man-smile.jpg"
    hiscore_bg: str = "pac-man-ce2.jpg"
    instruction_bg: str = "pac-man-ce2.jpg"
    # menu_bg: str = "pac-man-ce1.jpg"
    # menu_bg: str = "pac-man-ce2.jpg"
    pm_icon : str = "\U0001F6BD"
    argv: list[str] = sys.argv
    config_file_name: str = ""

    def __init__(self) -> None:
        Config.config_read_file()
        if getattr(sys, "frozen", False):
            # Exécution depuis un exécutable PyInstaller
            Config.image_directory = str(Path(sys._MEIPASS)) + "/" + Config.image_directory
        Config.sprite_42 = Config.image_directory + Config.sprite_42
        Config.sprite_pacgum = Config.image_directory + Config.sprite_pacgum
        Config.sprite_super = Config.image_directory + Config.sprite_super
        Config.logo = Config.image_directory + Config.logo
        Config.game_over = Config.image_directory + Config.game_over
        Config.victory = Config.image_directory + Config.victory
        Config.game_bg = Config.image_directory + Config.game_bg
        Config.menu_bg = Config.image_directory + Config.menu_bg
        Config.hiscore_bg = Config.image_directory + Config.hiscore_bg
        Config.instruction_bg = Config.image_directory + Config.instruction_bg

    @classmethod
    def config_read_file(cls) -> None:
        Config.file_from_argv()
        config_dict: dict[str, Any] = {}
        try:
            with open(Config.config_file_name, "r") as config_json_file:
                config_json: str = ""
                config_line: str = ""
                config_line = config_json_file.readline()
                while config_line:
                    if not config_line.strip().startswith(("#", "//")):
                        config_json += config_line
                    config_line = config_json_file.readline()
                config_dict = json.loads(config_json)
                Config.set_values(config_dict)
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
            try:
                if hasattr(Config, key):
                    config_key_type: type = type(getattr(Config, key))
                    if isinstance(value, type(getattr(Config, key))):
                        if Config.verify_value(key, value):
                            setattr(Config, key, value)
                    else:
                        raise ConfigTypeError(key, value, config_key_type)
                else:
                    raise ConfigKeyError(key)
            except Error:
                pass

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
                        raise PacGumLessThan0Error
                    if value > (Config.width * Config.height - 22):
                        raise PacGumTooBigError
                case "spacgum":
                    if value < 0:
                        raise SuperPacGumLessThan0Error
                    if value > (Config.width * Config.height - 22 - Config.pacgum):
                        raise SuperPacGumTooBigError
                case "points_per_pacgum":
                    if value < 0:
                        raise PointPerPacgumLessThan0Error
                case "points_per_super_pacgum":
                    if value < 0:
                        raise PointPerSuperPacgumLessThan0Error
                case "points_per_ghost":
                    if value < 0:
                        raise PointPerGhostLessThan0Error
                case _:
                    value_ok = False
        except Error:
            value_ok = False
        return (value_ok)
