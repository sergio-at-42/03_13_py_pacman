from pm_ghost_strategy import PmGhostStrategy

class PmGhost():

    def __init__(self, name: str = "Gogo",
                 color: int = 0xFFFFFF,
                 home_pos: tuple[int, int] = (7, 7),
                 corner_pos: tuple[int, int] = (7, 7),
                 strategy: PmGhostStrategy = PmGhostStrategy()
                ) -> None:
        self.name: str = name
        self.color: int = color
        self.home_pos: tuple[int, int] = home_pos
        self.corner_pos: tuple[int, int] = corner_pos
        self.pos: tuple[int, int] = self.home_pos
        self.strategy: PmGhostStrategy = strategy

    def chase(self) -> None:
        self.move_to(self.strategy)

    def escape(self) -> None:
        self.move_to(self.home_pos)

    def scatter(self) -> None:
        self.move_to(self.corner_pos)

    def move_to(self, pos: tuple[int, int]) -> None:
        self.pos = (0, 0)