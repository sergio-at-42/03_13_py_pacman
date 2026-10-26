#!/usr/bin/env python3

from lib_pacman import Game, Error


def main() -> None:
    Error.log_new_pacman()
    Game()
    Error.log_game_over()


if __name__ == "__main__":
    main()
