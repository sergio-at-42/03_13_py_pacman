from random import randrange
from .pm_config import PmConfig
from .maze import Maze
# from .pm_ghost_strategy import PmGhostStrategy
from .pm_sprite import PmSpGhost, PmSpBlinky, PmSpPinky, PmSpInky, PmSpClyde
from .mood import Mood
from .direction import Direction


class PmGhost():

    def __init__(self) -> None:
        self.name: str = "Gogo"
        self.color: int = 0xffffff
        self.home_pos: tuple[int, int] = (0, 0)
        self.corner_pos: tuple[int, int] = (0, 0)
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.pos
        self.target_pos: tuple[int, int] = self.corner_pos
        self.direction: Direction = Direction.STOP
        self.speed: float = 1
        self.mood: Mood = Mood.RIDE
        # self.strategy: PmGhostStrategy = PmGhostStrategy(self)
        self.between_pos: float = 0
        self.sprite_pos: tuple[int, int] = (40, 40)
        self.sprite: PmSpGhost = PmSpGhost(self)

    def move(self, pos: tuple[int, int] = ()) -> None:
        from .pm_game import PmGame
        self.between_pos = (self.between_pos 
                            + abs(self.direction.move()[0] * self.speed)
                            + abs(self.direction.move()[1] * self.speed))
        if self.between_pos >= Maze.cell_size:
            self.between_pos = 0
            self.pos = self.next_pos
        self.sprite_pos = self.convert_pos(self.pos)
        self.sprite_pos = tuple([
                            self.sprite_pos[0] + self.direction.move()[0] * self.between_pos,
                            self.sprite_pos[1] + self.direction.move()[1] * self.between_pos])

        if pos != ():
            self.mood = Mood.GO
            self.target_pos = pos

        if self.pos == self.next_pos:
            # self.strategy.next_move()
            if self.mood is Mood.RIDE:
                self.target_pos = (randrange(PmConfig.width), randrange(PmConfig.height))
            elif self.mood is Mood.SCATTER:
                self.target_pos = self.corner_pos
            elif self.mood is Mood.DEAD:
                self.target_pos = self.home_pos
            elif self.mood is Mood.SCARED:
                pass
            elif self.mood is Mood.CHASE:
                self.target_pos = PmGame.player.pos
    
            if self.mood is Mood.SLEEP:
                self.direction = Direction.STOP
            else:
                col, row = self.pos
                next_directions = 15 - Maze.grid[row][col] - self.direction.inverse()
                if next_directions in (1, 2, 4, 8):
                    self.direction = Direction(next_directions)
                elif next_directions == 0:
                    self.direction = Direction(self.direction.inverse())
                else:
                    self.bfs()
            self.next_pos = self.direction.move_from(self.pos)

    def bfs(self) -> None:
        next_cells: dict[tuple[int, int]: Direction] = {}
        visited_cells: set[tuple[int, int]] = set()
        visited_cells.add(self.pos)
        col, row = self.pos
        start_cell = 15 - Maze.grid[row][col] - self.direction.inverse()
        if start_cell & Direction.NORTH.value:
            next_cells[Direction.NORTH.move_from(self.pos)] = Direction.NORTH
        if start_cell & Direction.EST.value:
            next_cells[Direction.EST.move_from(self.pos)] = Direction.EST
        if start_cell & Direction.SOUTH.value:
            next_cells[Direction.SOUTH.move_from(self.pos)] = Direction.SOUTH
        if start_cell & Direction.WEST.value:
            next_cells[Direction.WEST.move_from(self.pos)] = Direction.WEST
        
        search_pos: tuple[int, int] = list(next_cells.keys())[0]
        
        while search_pos != self.target_pos and len(next_cells) != 0:
            # print(next_cells)
            visited_cells.add(search_pos)
            col, row = search_pos
            search_pos_exit = 15 - Maze.grid[row][col]
            if search_pos_exit & Direction.NORTH.value:
                next_pos = Direction.NORTH.move_from(search_pos)
                if next_pos not in visited_cells:
                    next_cells[next_pos] = next_cells[search_pos]
            if search_pos_exit & Direction.EST.value:
                next_pos = Direction.EST.move_from(search_pos)
                if next_pos not in visited_cells:
                    next_cells[next_pos] = next_cells[search_pos]
            if search_pos_exit & Direction.SOUTH.value:
                next_pos = Direction.SOUTH.move_from(search_pos)
                if next_pos not in visited_cells:
                    next_cells[next_pos] = next_cells[search_pos]
            if search_pos_exit & Direction.WEST.value:
                next_pos = Direction.WEST.move_from(search_pos)
                if next_pos not in visited_cells:
                    next_cells[next_pos] = next_cells[search_pos]
            del next_cells[search_pos]
            if len(next_cells) != 0:
                search_pos = list(next_cells.keys())[0]
            else:
                search_pos = self.target_pos
        if len(next_cells) == 0:
            self.direction = Direction(self.direction.inverse())
        else:
            self.direction = next_cells[search_pos]
            
        # self.direction = next_cells[search_pos]

    def convert_pos(self, grid_pos: tuple[int, int]) -> tuple[int, int]:
        grid_x: int = 0
        grid_y: int = 0
        grid_x, grid_y = grid_pos
        return ((grid_x * Maze.cell_size + 8, grid_y * Maze.cell_size + 8))


class PmBlinky(PmGhost):
    def __init__(self) -> None:
        super().__init__()
        self.name = "blinky"
        self.color: int = 0xff0000
        self.home_pos: tuple[int, int] = (PmConfig.width // 2 - 3, PmConfig.height // 2 - 2)
        self.corner_pos: tuple[int, int] = (0, 0)
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.pos
        self.speed = 1.5
        self.sprite = PmSpBlinky(self)


class PmPinky(PmGhost):
    def __init__(self) -> None:
        super().__init__()
        self.name = "pinky"
        self.color: int = 0xffc0c0
        self.home_pos: tuple[int, int] = (PmConfig.width // 2 - 2, PmConfig.height // 2 - 2)
        self.corner_pos: tuple[int, int] = (PmConfig.width-1, 0)
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.pos
        self.speed = 1
        self.sprite = PmSpPinky(self)


class PmInky(PmGhost):
    def __init__(self) -> None:
        super().__init__()
        self.name = "inky"
        self.color: int = 0x0000ff
        self.home_pos: tuple[int, int] = (PmConfig.width // 2 + 0, PmConfig.height // 2 - 2)
        self.corner_pos: tuple[int, int] = (PmConfig.width-1, PmConfig.height-1)
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.pos
        self.sprite = PmSpInky(self)


class PmClyde(PmGhost):
    def __init__(self) -> None:
        super().__init__()
        self.name = "clyde"
        self.color: int = 0xff7f00
        self.home_pos: tuple[int, int] = (PmConfig.width // 2 + 1, PmConfig.height // 2 - 2)
        self.corner_pos: tuple[int, int] = (0, PmConfig.height-1)
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.pos
        self.speed = 1.3
        self.sprite = PmSpClyde(self)




    # def move(self, pos: tuple[int, int] = ()) -> None:
    #     from .pm_game import PmGame
    #     if pos != ():
    #         self.mood = Mood.GO
    #         self.ghost.target_pos = pos
    #     if self.ghost.pos == self.ghost.next_pos:
    #         # self.strategy.next_move()
    #         if self.ghost.mood is Mood.RIDE:
    #             self.ghost.target_pos = (randrange(PmConfig.width), randrange(PmConfig.height))
    #         elif self.ghost.mood is Mood.SCATTER:
    #             self.ghost.target_pos = self.ghost.corner_pos
    #         elif self.ghost.mood is Mood.DEAD:
    #             self.ghost.target_pos = self.ghost.home_pos
    #         elif self.ghost.mood is Mood.SCARED:
    #             pass
    #         elif self.ghost.mood is Mood.CHASE:
    #             self.ghost.target_pos = PmGame.player.pos
    
    #         if self.ghost.mood is Mood.SLEEP:
    #             self.ghost.direction = Direction.STOP
    #         else:
    #             if grid - self.ghost.direction.inverse()
    #             self.bfs(self.ghost.target_pos)