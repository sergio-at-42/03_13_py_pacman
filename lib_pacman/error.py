from datetime import datetime
from typing import Any


class Error(Exception):
    """Base class for Pacman related errors."""

    log_file_name: str = "pacman.log"
    new_pacman: bool = True

    def __init__(self, log_msg: str) -> None:
        super().__init__(log_msg)
        if self.new_pacman:
            self.log_new_pacman()
        self.write_log(log_msg)

    @classmethod
    def write_log(cls, log_msg: str) -> bool:
        write_ok: bool = False
        try:
            with open(cls.log_file_name, "a") as log_file:
                msg_type, bracket, msg_text = log_msg.partition("]")
                msg_type += bracket
                log_file.write(f"{msg_type}"
                    f"\t{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
                    f"\t{msg_text}\n")
                write_ok = True
        except Exception:
            write_ok = False
        return (write_ok)

    @classmethod
    def read_log(cls) -> str:
        log: str = ""
        try:
            with open(cls.log_file_name, "r") as log_file:
                log = log_file.read()
        except Exception:
            log = ""
        return (log)

    @classmethod
    def log_new_pacman(cls) -> bool:
        msg: str = ("[info]"
                    f"\t{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
                    "\tNew Pac-Man game started 🙄👻\n")
        write_ok: bool = False
        try:
            with open(cls.log_file_name, "a") as log_file:
                log_file.write(msg)
                cls.new_pacman = False
                write_ok = True
        except Exception:
            write_ok = False
        return (write_ok)

    @classmethod
    def log_game_over(cls) -> bool:
        msg: str = ("[info]"
                    f"\t{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
                    "\tGame Over 🎮\n\n")
        write_ok: bool = False
        try:
            with open(cls.log_file_name, "a") as log_file:
                log_file.write(msg)
                write_ok = True
        except Exception:
            write_ok = False
        return (write_ok)
    

class ConfigTypeError(Error):
    """Base class for width for 42 related errors."""
    def __init__(self, key: str, value: Any, config_key_type) -> None:
        super().__init__(f"[error]Submit key <{key}> is type of <{type(key).__name__}>. "
                         f"<{config_key_type.__name__}> attended.")


class ConfigKeyError(Error):
    """Base class for width for 42 related errors."""
    def __init__(self, key: str) -> None:
        super().__init__(f"[error]Submit key <{key}> not exist in config.")


class WidthSmallFor42Error(Error):
    """Base class for width for 42 related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Width too small for 42.")


class HeightToSmallFor42Error(Error):
    """Base class for height for 42 related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Height too small for 42.")


class WidthLessThan2Error(Error):
    """Base class for width related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Width to small. Must be over 2 ! "
                         " Auto configurated width.")


class HeightLessThan2Error(Error):
    """Base class for height related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Height to small. Must be over 2 ! "
                         "Auto configurated height.")


class LivesLessThan1Error(Error):
    """Base class for lives related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Lives to small. Must be over 0 ! "
                         "Auto configurated lives.")


class TimeLessThan0Error(Error):
    """Base class for time related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Time to small. Must be over 0 ! "
                         "Auto configurated times")


class PacGumLessThan0Error(Error):
    """Base class for time related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Number of PacGum to small. Must be over 0 ! "
                         "Auto configurated number of PacGum")


class SuperPacGumLessThan0Error(Error):
    """Base class for time related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Number of Super-PacGum to small. "
                         "Must be over 0 ! "
                         "Auto configurated number of Super-PacGum")


class PointPerPacgumLessThan0Error(Error):
    """Base class for time related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Point per Pacgum to small. Must be over 0 ! "
                         "Auto configurated point per Pacgum to small")


class PointPerSuperPacgumLessThan0Error(Error):
    """Base class for time related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Point per Super-Pacgum to small. "
                         "Must be over 0 ! "
                         "Auto configurated point per Super-Pacgum")


class PointPerGhostLessThan0Error(Error):
    """Base class for time related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Point per ghost to small. Must be over 0 ! "
                         "Auto configurated point per ghost")


class MazeLoadError(Error):
    """Base class for maze loading related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Failed to load maze.")
