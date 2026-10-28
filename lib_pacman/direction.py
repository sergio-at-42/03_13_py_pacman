from enum import Enum


class Direction(Enum):
    STOP = 0
    NORTH = 1
    EST = 2
    SOUTH = 4
    WEST = 8

    def move(self) -> tuple[int, int]:
        move: tuple[int, int] = (0, 0)
        match self.value:
            case 1:
                move = (0, -1)
            case 2:
                move = (1, 0)
            case 4:
                move = (0, 1)
            case 8:
                move = (-1, 0)
        return (move)

    def move_from(self, pos: tuple[int, int]) -> tuple[int, int]:
        return ((pos[0] + self.move()[0], pos[1] + self.move()[1]))

    def letter(self) -> str:
        lower_letter: str = "e"
        match self.value:
            case 1:
                lower_letter = "n"
            case 2:
                lower_letter = "e"
            case 4:
                lower_letter = "s"
            case 8:
                lower_letter = "w"
        return (lower_letter)

    def inverse(self) -> int:
        inverse_direction: int = 0
        match self.value:
            case 1:
                inverse_direction = 4
            case 2:
                inverse_direction = 8
            case 4:
                inverse_direction = 1
            case 8:
                inverse_direction = 2
        return (inverse_direction)
