#!/usr/bin/env python3

from lib_pacman import PmGame


def main() -> None:
    print("PACMAN")
    game:PmGame = PmGame()
    game.game_loop()


if __name__ == "__main__":
    main()
