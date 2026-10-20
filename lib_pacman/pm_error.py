from datetime import datetime


class PmError(Exception):
    """Base class for Pacman related errors."""

    log_file_name: str = "pacman.log"
    new_pacman: bool = True

    def __init__(self, log_msg: str) -> None:
        super().__init__(log_msg)
        if self.new_pacman:
            self.new_pacman = not (self.log_new_pacman())
        self.write_log(log_msg)

    @classmethod
    def write_log(cls, log_msg) -> bool:
        write_ok: bool = False
        try:
            with open(cls.log_file_name, "a") as log_file:
                log_file.write(f"{log_msg}"
                    f"\t{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n")
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
        banner_new_pacman: str = ("\n"
            "🙄🙄🙄🙄🙄🙄🙄🙄🙄🙄🙄🙄🙄🙄🙄🙄🙄🙄🙄🙄🙄🙄🙄\n"
            "🟡            WELCOME TO PAC-MAN            🟡\n"
            f"🟡            {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}           🟡\n"
            "👻👻👻👻👻👻👻👻👻👻👻👻👻👻👻👻👻👻👻👻👻👻👻\n"
            "\n")
        write_ok: bool = False
        try:
            with open(cls.log_file_name, "a") as log_file:
                log_file.write(banner_new_pacman)
                write_ok = True
        except Exception:
            write_ok = False
        return (write_ok)


class WidthSmallFor42Error(PmError):
    """Base class for width for 42 related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Width too small for 42.")


class HeightToSmallFor42Error(PmError):
    """Base class for height for 42 related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Height too small for 42.")


class WidthLessThan2Error(PmError):
    """Base class for width related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Width to small. Must be over 2 ! "
                         " Auto configurated width.")


class HeightLessThan2Error(PmError):
    """Base class for height related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Height to small. Must be over 2 ! "
                         "Auto configurated height.")


class LivesLessThan1Error(PmError):
    """Base class for lives related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Lives to small. Must be over 0 ! "
                         "Auto configurated lives.")


class TimeLessThan0Error(PmError):
    """Base class for time related errors."""
    def __init__(self) -> None:
        super().__init__("[error]Time to small. Must be over 0 ! "
                         "Auto configurated times")
