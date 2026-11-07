#!/usr/bin/env python3

from lib_pacman import Session, Config, Error


class PacManGameSince1980():
    def __init__(self):
        Error.log_new_pacman()
        Config()
        # Game()
        session = Session()
        session.run()
        Error.log_game_over()


if __name__ == "__main__":
    PacManGameSince1980()
