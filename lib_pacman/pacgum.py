import random
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
    
def corners(grid: list[list[int]]) -> list[Pos]:
    """Return the four corner coordinates of the maze."""
    height = len(grid)
    width = len(grid[0])

    return [
        (0, 0),
        (width - 1, 0),
        (0, height - 1),
        (width - 1, height - 1),
    ]


def eligible_cells(
    grid: list[list[int]],
    excluded: set[Pos],
) -> list[Pos]:
    """Return cells eligible for regular pacgums, in row-major order."""
    height = len(grid)
    width = len(grid[0])
    forbidden = set(corners(grid)) | excluded
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


def place_pacgums(
    grid: list[list[int]],
    count: int,
    excluded: set[Pos],
    rng: random.Random,
) -> Pacgum:
    """Place regular pacgums and one super-pacgum per corner."""
    available = eligible_cells(grid, excluded)
    # check if count is negative or larger than the number of available cells (count = config.pacgum)
    if count < 0:
        count = 0
    if count > len(available):
        count = len(available)
    # get a random sample of the available cells for the pacgums
    selected = rng.sample(available, count)

    return Pacgum(
        pacgums=set(selected),
        super_pacgums=set(corners(grid)),
    )
