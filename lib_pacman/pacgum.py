
# import random
# from collections import deque

# from .direction import Direction

# Pos = tuple[int, int]  # (col, row); grid[row][col]


# class Pacgum:
#     """Positions of the pacgums still on the board."""

#     def __init__(self, pacgums: set[Pos] | None = None,
#                  super_pacgums: set[Pos] | None = None) -> None:
#         self.pacgums: set[Pos] = set() if pacgums is None else pacgums
#         self.super_pacgums: set[Pos] = (
#             set() if super_pacgums is None else super_pacgums)
#  # for the tests
#     def __eq__(self, other: object) -> bool:
#         if not isinstance(other, Pacgum):
#             return NotImplemented
#         return (self.pacgums == other.pacgums
#                 and self.super_pacgums == other.super_pacgums)
#  # for the tests
#     def __repr__(self) -> str:
#         return (f"Pellets(pacgums={sorted(self.pacgums)}, "
#                 f"super_pacgums={sorted(self.super_pacgums)})")
    
# def reachable_cells(
#     grid: list[list[int]],
#     start: Pos,
# ) -> set[Pos]:
#     """Return cells reachable from start without crossing walls.

#     Return an empty set if start is outside the grid or on a 42 block.
#     """
#     if not grid or not grid[0]:
#         return set()  # should check this with exceptions, but for now, just return an empty set
#     height = len(grid)
#     width = len(grid[0])
#     col, row = start

#     if not (0 <= col < width and 0 <= row < height):
#         return set()  # should check this with exceptions, but for now, just return an empty set


#     if grid[row][col] == 15:
#         return set()  # should check this with exceptions, but for now, just return an empty set
        

#     directions = (
#         Direction.NORTH,
#         Direction.EST,
#         Direction.SOUTH,
#         Direction.WEST,
#     )

#     visited = {start}
#     queue = deque([start])
#     while queue:
#         col, row = queue.popleft()
#         cell = grid[row][col]

#         for direction in directions:
#             # Check whether the current cell has a wall
#             # in the direction we want to move.
#             if cell & direction.value:
#                 continue
#             # Calculate the neighboring cell.
#             next_col, next_row = direction.move_from((col, row))
#             # Check grid boundaries.
#             if not (
#                 0 <= next_col < width
#                 and 0 <= next_row < height
#             ):
#                 continue
#             neighbor = (next_col, next_row)
#             if neighbor in visited:
#                 continue

#             if grid[next_row][next_col] == 15:
#                 continue

#             visited.add(neighbor)
#             queue.append(neighbor)

#     return visited


# def corners(grid: list[list[int]]) -> list[Pos]:
#     """Return the four corner coordinates of the maze."""
#     if not grid or not grid[0]:
#         return [] # error handling 

#     height = len(grid)
#     width = len(grid[0])

#     return [
#         (0, 0),
#         (width - 1, 0),
#         (0, height - 1),
#         (width - 1, height - 1),
#     ]


# def eligible_cells(
#     grid: list[list[int]],
#     start: Pos,
#     excluded: set[Pos],
# ) -> list[Pos]:
#     """Return sorted cells eligible for regular pacgums.

#     Exclude the starting cell, the four corners, and excluded cells.
#     Only reachable, non-42 cells are eligible.
#     """
#     reachable = reachable_cells(grid, start)
#     forbidden = set(corners(grid))
#     forbidden.add(start)
#     forbidden.update(excluded)

#     return sorted(reachable - forbidden)

# def place_pacgums(
#     grid: list[list[int]],
#     count: int,
#     start: Pos,
#     excluded: set[Pos],
#     rng: random.Random,
# ) -> Pacgum:
#     """Place up to count regular pacgums and super-pacgums in the corners.

#     The grid is never modified. Regular pacgums are placed only in
#     eligible cells. Super-pacgums occupy the four corner coordinates.
#     """
#     available = eligible_cells(grid, start, excluded)

#     # Clamp the requested count to the available number of cells.
#     # If count is negative, treat it as zero. 
#     # If count is larger than the number of available cells, treat it as the number of available cells.
#     count = max(0, min(count, len(available)))

#     # Use the supplied RNG so callers can reproduce the placement.
#     selected = rng.sample(available, count)

#     return Pacgum(
#         pacgums=set(selected),
#         super_pacgums=set(corners(grid)),
#     )

# """Pacgum and super-pacgum placement (pure logic, no pygame)."""

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
    try:
        if not grid or not grid[0]:
            return []
         # should check how to add to log file
    except Exception as e:
            raise Error(f"The maze grid is empty.: {e}")

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
    try:
        if not grid or not grid[0]:
            return [] 
        # should check how to add to log file
    except Exception as e:
            raise Error(f"The maze grid is empty.: {e}") from e

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
