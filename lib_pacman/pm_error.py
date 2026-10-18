class PmError(Exception):
    """Base class for maze related errors."""


class WidthSmallFor42Error(PmError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Width too small for 42, need W=11 ")


class HeightToSmallFor42Error(PmError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Height too small for 42, needH=7")


class WidthLessThan2Error(PmError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Width to small. Must be over 2 !"
                         " Auto configurated width")


class HeightLessThan2Error(PmError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Height to small. Must be over 2 !"
                         "Auto configurated height")


class LivesLessThan1Error(PmError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Lives to small. Must be over 0 !"
                         "Auto configurated lives")


class TimeLessThan0Error(PmError):
    """Base class for entry point in 42 related errors."""
    def __init__(self) -> None:
        super().__init__("Times to small. Must be over 0 !"
                         "Auto configurated times")