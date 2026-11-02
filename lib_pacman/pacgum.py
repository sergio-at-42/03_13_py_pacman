import random
from .config import Config
from .error import Error

Pos = tuple[int, int]  # (col, row)


class Pacgum:
    """Positions of the pacgums still on the board."""
    def __init__(self, pacgums: set[Pos] | None = None,
                 super_pacgums: set[Pos] | None = None) -> None:
        self.pacgums: set[Pos] = set() if pacgums is None else pacgums
        self.super_pacgums: set[Pos] = (
            set() if super_pacgums is None else super_pacgums)

    # for the tests
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pacgum):
            return NotImplemented
        return (self.pacgums == other.pacgums
                and self.super_pacgums == other.super_pacgums)
    # for the tests
    def __repr__(self) -> str:
        return (f"Pellets(pacgums={sorted(self.pacgums)}, "
                f"super_pacgums={sorted(self.super_pacgums)})")

    @classmethod
    def corners(cls, grid: list[list[int]]) -> list[Pos]:
        """Return the four corner coordinates of the maze."""
        height = len(grid)
        width = len(grid[0])
        return [
            (0, 0),
            (width - 1, 0),
            (0, height - 1),
            (width - 1, height - 1),
            ]

    @classmethod
    def eligible_cells(cls,
        grid: list[list[int]],
        excluded: set[Pos],
        ) -> list[Pos]:
        """Return cells eligible for regular pacgums, in row-major order."""
        height = len(grid)
        width = len(grid[0])
        forbidden = set(cls.corners(grid)) | excluded
        available = []
        for row in range(height):
            for col in range(width):
                pos = (col, row)

                if grid[row][col] == 15:
                    continue

                if pos in forbidden:
                    continue
                available.append(pos)
        return available

    @classmethod
    def place_pacgums(cls, grid: list[list[int]], excluded: set[Pos]) -> Pacgum:

        count: int = Config.pacgum
        rng = random.Random(Config.seed)

        """Place regular pacgums and one super-pacgum per corner."""
        available = cls.eligible_cells(grid, excluded)
        # check if count is negative or larger than the number of available cells (count = config.pacgum)
        if count < 0:
            count = 0
        if count > len(available):
            count = len(available)
        # get a random sample of the available cells for the pacgums
        selected = rng.sample(available, count)
        return Pacgum(
            pacgums=set(selected),
            super_pacgums=set(cls.corners(grid))
            )
