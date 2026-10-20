class PmError(Exception):
    """Base class for Pacman related errors."""
    log_file_name: str = "pacman.log"

    def write_log() -> None:
        pass

    def read_log() -> None:
        pass


class WidthSmallFor42Error(PmError):
    """Base class for width for 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Width too small for 42.")


class HeightToSmallFor42Error(PmError):
    """Base class for height for 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Height too small for 42.")


class WidthLessThan2Error(PmError):
    """Base class for width related errors."""
    def __init__(self) -> None:
        super().__init__("Width to small. Must be over 2 !"
                         " Auto configurated width.")


class HeightLessThan2Error(PmError):
    """Base class for height related errors."""
    def __init__(self) -> None:
        super().__init__("Height to small. Must be over 2 !"
                         "Auto configurated height.")


class LivesLessThan1Error(PmError):
    """Base class for lives related errors."""
    def __init__(self) -> None:
        super().__init__("Lives to small. Must be over 0 !"
                         "Auto configurated lives.")


class TimeLessThan0Error(PmError):
    """Base class for time related errors."""
    def __init__(self) -> None:
        super().__init__("Time to small. Must be over 0 !"
                         "Auto configurated times")