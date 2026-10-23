#!/usr/bin/env python3

from lib_pacman import PmGame, PmError


def main() -> None:
    PmError.log_new_pacman()
    game:PmGame = PmGame()
    PmError.log_game_over()


if __name__ == "__main__":
    main()
