from mazegenerator import MazeGenerator

# N, E, S, W = 1, 2, 4, 8

# def show(grid: list[list[int]]) -> None:
#     h, w = len(grid), len(grid[0])
#     for y in range(h):
#         top = mid = ""
#         for x in range(w):
#             c = grid[y][x]
#             top += "+" + ("---" if c & N else "   ")
#             mid += ("|" if c & W else " ") + (" # " if c == 15 else "   ")
#         print(top + "+")
#         print(mid + ("|" if grid[y][w - 1] & E else " "))
#     print("".join("+---" if grid[h - 1][x] & S else "+   " for x in range(w)) + "+")

# show(MazeGenerator(size=(15, 15), perfect=False, seed=42).maze)
def load_maze(width: int, height: int, seed: int) -> list[list[int]]:
    """Return the grid, or raise MazeLoadError with a human-readable message."""
    try:
        gen = MazeGenerator(size=(width, height), perfect=False, seed=seed)
        return gen.maze
    except Exception as e:
        raise MazeLoadError(f"Failed to load maze: {e}") from e #class MazeLoadError(Exception)
    