from random import randint, randrange
from .config import Config
from .maze import Maze
# from .pm_ghost_strategy import GhostStrategy
from .sprite import SpGhost, SpBlinky, SpPinky, SpInky, SpClyde
from .mood import Mood
from .direction import Direction


class Ghost():

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
        self.normal_speed: float = 1
        self.mood: Mood = Mood.RIDE
        self.mood_time: int = randint(960, 1440)
        self.between_pos: float = 0
        self.sprite_pos: tuple[int, int] = (40, 40)
        self.sprite: SpGhost = SpGhost(self)

    def strategy(self) -> tuple[int, int]:
        from .game import Game
        return (Game.player.pos)

    def move(self, pos: tuple[int, int] = (-1, -1)) -> None:
        from .game import Game
        # mood management of the ghost
        self.mood_time -= 1
        if self.mood_time == 0:
            if self.mood != Mood.CHASE:
                self.mood = Mood.CHASE
                self.mood_time = randint(960, 1440) # 16 to 24 seconds
            else:
                self.mood = Mood.SCATTER
                self.mood_time = randint(600, 960) # 10 to 16 seconds
            self.speed = self.normal_speed
        
        # determine the target position based on the ghost's mood
        if pos != (-1, -1):
            self.mood = Mood.GO
            self.target_pos = pos

        if self.pos == self.next_pos:
            if self.mood is Mood.RIDE:
                self.target_pos = (randrange(Config.width), randrange(Config.height))
            elif self.mood is Mood.SCATTER:
                self.target_pos = self.corner_pos
            elif self.mood is Mood.DEAD:
                self.mood_time = -1
                self.speed = 4
                self.target_pos = self.home_pos
                if self.pos == self.home_pos:
                    self.mood_time = 1
            elif self.mood is Mood.SCARED:
                px, py = Game.player.pos
                self.target_pos = (abs(Config.width - 1 - px), abs(Config.height - 1 - py))
                self.speed = 0.7
            elif self.mood is Mood.CHASE:
                self.target_pos = self.strategy()

            if self.mood is Mood.SLEEP:
                self.direction = Direction.STOP
            else:
                next_directions = Maze.cell_exit(self.pos) - self.direction.inverse()
                if next_directions in (1, 2, 4, 8):
                    self.direction = Direction(next_directions)
                elif next_directions == 0:
                    self.direction = Direction(self.direction.inverse())
                else:
                    self.bfs()
            self.next_pos = self.direction.move_from(self.pos)

        # compute the position in pixel between the origin of the cell and the ghost position in the cell
        self.between_pos = (self.between_pos 
                            + abs(self.direction.move()[0] * self.speed)
                            + abs(self.direction.move()[1] * self.speed))
        # verify if the ghost enter in a new cell
        if self.between_pos >= Maze.cell_size:
            self.between_pos = 0
            self.pos = self.next_pos
        # convertion of the cell position in sprite position for the ghost
        self.sprite_pos = self.convert_pos(self.pos)
        self.sprite_pos = (
            int(self.sprite_pos[0] + self.direction.move()[0] * self.between_pos),
            int(self.sprite_pos[1] + self.direction.move()[1] * self.between_pos))

    def bfs(self) -> None:
        next_cells: dict[tuple[int, int], Direction] = {}
        visited_cells: set[tuple[int, int]] = set()
        visited_cells.add(self.pos)
        start_cell = Maze.cell_exit(self.pos) - self.direction.inverse()
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
            # col, row = search_pos
            search_pos_exit = Maze.cell_exit(search_pos)
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
            
    def convert_pos(self, grid_pos: tuple[int, int]) -> tuple[int, int]:
        grid_x: int = 0
        grid_y: int = 0
        grid_x, grid_y = grid_pos
        return ((grid_x * Maze.cell_size + 8, grid_y * Maze.cell_size + 8))


class Blinky(Ghost):
    def __init__(self) -> None:
        super().__init__()
        self.name = "blinky"
        self.color: int = 0xff0000
        self.corner_pos: tuple[int, int] = (0, 0)
        self.home_pos: tuple[int, int] = self.corner_pos #(Config.width // 2 - 3, Config.height // 2 - 2)
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.pos
        self.normal_speed = 1.5
        self.sprite = SpBlinky(self)

    def strategy(self) -> tuple[int, int]:
        from .game import Game
        px, py = Game.player.pos
        gx, gy = self.pos
        if abs(px - gx) + abs(py - gy) <= 4:
            self.speed = 2
        else:
            self.speed = self.normal_speed
        return (Game.player.pos)


class Pinky(Ghost):
    def __init__(self) -> None:
        super().__init__()
        self.name = "pinky"
        self.color: int = 0xffc0c0
        self.corner_pos: tuple[int, int] = (Config.width-1, 0)
        self.home_pos: tuple[int, int] = self.corner_pos #(Config.width // 2 - 2, Config.height // 2 - 2)
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.pos
        self.normal_speed = 1
        self.sprite = SpPinky(self)

    def strategy(self) -> tuple[int, int]:
        from .game import Game
        px, py = Game.player.pos
        dx, dy = Game.player.direction.move()
        px = px + dx * 4
        py = py + dy * 4
        return (Maze.limit((px, py)))


class Inky(Ghost):
    def __init__(self) -> None:
        super().__init__()
        self.name = "inky"
        self.color: int = 0x0000ff
        self.corner_pos: tuple[int, int] = (Config.width-1, Config.height-1)
        self.home_pos: tuple[int, int] = self.corner_pos #(Config.width // 2 + 0, Config.height // 2 - 2)
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.pos
        self.normal_speed: float = 1
        self.sprite = SpInky(self)

    def strategy(self) -> tuple[int, int]:
        from .game import Game
        px, py = Game.player.pos
        dx, dy = Game.player.direction.move()
        px = px + dx * 2
        py = py + dy * 2
        return (Maze.limit((px, py)))


class Clyde(Ghost):
    def __init__(self) -> None:
        super().__init__()
        self.name = "clyde"
        self.color: int = 0xff7f00
        self.corner_pos: tuple[int, int] = (0, Config.height-1)
        self.home_pos: tuple[int, int] = self.corner_pos #(Config.width // 2 + 1, Config.height // 2 - 2)
        self.pos: tuple[int, int] = self.home_pos
        self.next_pos: tuple[int, int] = self.pos
        self.normal_speed = 1.3
        self.sprite = SpClyde(self)

    def strategy(self) -> tuple[int, int]:
        from .game import Game
        px, py = Game.player.pos
        gx, gy = self.pos
        if abs(px - gx) + abs(py - gy) > 8:
            return (Game.player.pos)
        return (self.corner_pos)






    # def move(self, pos: tuple[int, int] = ()) -> None:
    #     from .pm_game import Game
    #     if pos != ():
    #         self.mood = Mood.GO
    #         self.ghost.target_pos = pos
    #     if self.ghost.pos == self.ghost.next_pos:
    #         # self.strategy.next_move()
    #         if self.ghost.mood is Mood.RIDE:
    #             self.ghost.target_pos = (randrange(Config.width), randrange(Config.height))
    #         elif self.ghost.mood is Mood.SCATTER:
    #             self.ghost.target_pos = self.ghost.corner_pos
    #         elif self.ghost.mood is Mood.DEAD:
    #             self.ghost.target_pos = self.ghost.home_pos
    #         elif self.ghost.mood is Mood.SCARED:
    #             pass
    #         elif self.ghost.mood is Mood.CHASE:
    #             self.ghost.target_pos = Game.player.pos
    
    #         if self.ghost.mood is Mood.SLEEP:
    #             self.ghost.direction = Direction.STOP
    #         else:
    #             if grid - self.ghost.direction.inverse()
    #             self.bfs(self.ghost.target_pos)