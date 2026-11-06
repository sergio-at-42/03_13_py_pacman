#!/usr/bin/env python3

from lib_pacman import Game, Config, Error


def main() -> None:
    Error.log_new_pacman()
    Config()
    Game()
    Error.log_game_over()


if __name__ == "__main__":
    main()
