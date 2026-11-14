*This activity has been created as part of the 42 curriculum by sansaidi, sbeldjao.*

# Pac-Man

## Description

Inspired by the classic arcade game released by Namco in 1980, this project is a Python implementation of Pac-Man using Pygame.

The objective is to guide Pac-Man through randomly generated mazes, collect pacgums, avoid ghosts and achieve the highest possible score. The game features four ghosts with different behaviours, multiple levels, a high score system and an optional Cheat Mode.

## Instructions

### Requirements

- Python 3
- Pygame
- The provided A-Maze-ing package wheel

### Installation

Create a virtual environment and install the dependencies:

```bash
make install
```

### Run the game

```bash
make run
```

This launches the game using `config.json`.

To launch the game without explicitly providing a configuration file:

```bash
make noconfig
```

### Debug

```bash
make debug
```

### Additional Makefile commands

| Command | Description |
|---|---|
| `make exe` | Build a standalone executable using PyInstaller. |
| `make lint` | Run code quality checks. |
| `make lint-strict` | Run stricter code quality checks. |
| `make clean` | Remove Python cache files. |
| `make fclean` | Remove cache files and the virtual environment. |
| `make exe` | Create a unique executable file in dist directory. |

## Configuration

The game accepts an optional JSON configuration file as a command-line argument:

```bash
python3 pacman.py config.json
```

If no file is provided or the configuration cannot be loaded, the game uses its default values.

Full-line comments beginning with `#` or `//` are supported and removed before parsing the JSON content.

The following parameters can be configured:

| Parameter | Default | Description |
|---|---:|---|
| `width` | `16` | Maze width. |
| `height` | `16` | Maze height. |
| `pacgum` | `42` | Number of regular pacgums. |
| `spacgum` | `4` | Number of super pacgums. |
| `points_per_pacgum` | `10` | Points for collecting a regular pacgum. |
| `points_per_super_pacgum` | `50` | Points for collecting a super pacgum. |
| `points_per_ghost` | `200` | Points for eating a ghost. |

Configuration values are checked for valid types and ranges. Invalid or unknown parameters are reported, and their default values are retained.

## Gameplay and Implementation

### Player and Ghosts

The player controls Pac-Man using the keyboard or a compatible joystick. The `Pacman` class manages movement, speed, lives, scoring and interactions with collectibles.

The game includes four ghosts, each with a different targeting strategy:

- **Blinky:** targets Pac-Man's current position.
- **Pinky:** targets a position four cells ahead of Pac-Man.
- **Inky:** targets a position two cells ahead.
- **Clyde:** chases Pac-Man when far away and retreats towards its corner when nearby.

Ghost behaviour is controlled by different mood states, such as `CHASE`, `SCATTER`, `SCARED`, `HOME` and `DEAD`. A BFS-based pathfinding algorithm helps them find their way through the maze.

Collecting a super pacgum temporarily frightens the ghosts, allowing Pac-Man to eat them and earn extra points.

### Maze Generation and Pacgum Placement

The project uses the provided **A-Maze-ing** package to generate the mazes. It is included in the `wheels/` directory and used without modifying its source code.

The `Maze` class manages maze generation and rendering. The maze is represented as a grid of integers, with bitwise values describing the walls in each cell.

The `Pacgum` class handles collectible placement. Regular pacgums are randomly distributed across eligible cells, excluding walls, special cells, corners and character starting positions. Four super pacgums are placed in the maze corners.

A random seed is used to make maze and pacgum generation reproducible when the same inputs are provided.

### Gameplay Features

The `Game` class coordinates the gameplay loop, including movement, collisions, scoring, timers and graphical updates.

The game includes:

- Ten levels, with the possibility of choosing a starting level from the main menu.
- Increasing difficulty through maze dimensions, time limits and game speed.
- A pause screen and game-over and victory screens.
- Keyboard and joystick support.
- A score multiplier for eating successive frightened ghosts.
- An optional Cheat Mode with additional commands.

When all pacgums have been collected, the game advances to the next level. Completing the tenth level displays the victory screen.

### Bomb Mechanics

When Cheat Mode is enabled, pressing `X` places a bomb at Pac-Man's current position.

After a two-second countdown, the bomb explodes in a 3 × 3 area. Ghosts caught in the explosion are switched to the `DEAD` state, and the player earns points for each affected ghost.

### Controls

**Main menu**

| Key | Action |
|---|---|
| UP / DOWN | Navigate through menu entries. |
| ENTER | Select an option. |
| Digits | Enter a starting level. |
| BACKSPACE | Delete the last digit. |
| ESCAPE | Exit the game. |

**During gameplay**

- Arrow keys: move Pac-Man.
- ESCAPE: pause or resume the game.

A compatible joystick is also supported.

**Cheat Mode**

The following commands are available only when Cheat Mode is enabled:

| Key | Action |
|---|---|
| SPACE | Temporarily increase Pac-Man's speed. |
| X | Place a bomb. |
| R | Make ghosts move towards random positions. |
| F | Frighten all ghosts. |
| D | Set ghosts to the `DEAD` state. |
| H | Send ghosts back home. |
| S | Put ghosts to sleep. |
| C | Set ghosts to chase mode. |
| L | Skip to the next level. |

## High Score System

The `Hiscore` class manages the game's high score records, which are stored in a JSON file named `hiscores.json`.

Each record contains the player's name, score, level and date. At the end of a game, players can enter their names to save their results.

Scores are sorted from highest to lowest, and the top 10 are displayed on the high score screen. This allows players to keep track of their best performances across different sessions.

## General Software Architecture

The project is organized around the main entry point `pacman.py` and the `lib_pacman` Python package.

The main modules are:

| Module | Responsibility |
|---|---|
| `session.py` | Manages application states, screens and level progression. |
| `game.py` | Coordinates gameplay, collisions, scoring and display. |
| `config.py` | Loads and validates configuration parameters. |
| `maze.py` | Generates and renders the maze. |
| `pacman.py` | Handles player movement and interactions. |
| `ghost.py` / `mood.py` | Manage ghost behaviour and mood states. |
| `pacgum.py` | Handles collectible placement. |
| `bomb.py` / `explosion.py` | Manage bombs and explosions. |
| `menu.py` / `display_menu.py` | Handle menu logic and display. |
| `instruction.py` | Displays game instructions. |
| `hiscore.py` | Manages high score records. |
| `sprite.py` / `sprite_image.py` | Handle game sprites and graphical resources. |
| `error.py` | Handles custom errors and logging. |

The `Session` class connects the different components and controls the overall application flow. The `Game` class handles the active gameplay.

## Error Handling and Logging

The project includes a custom error-handling system for configuration, maze generation and other application errors.

Events and errors are recorded in `pacman.log`, with timestamps to help identify and investigate issues.

## Project Management

The project was developed over three weeks of effective work by two team members: `sansaidi` and `sbeldjao`.

Planning and task tracking documents, including the project timeline and final project summary, are available in the [`project_management/`](project_management/) directory.

## Resources

- [Pygame documentation](https://www.pygame.org/docs/)
- [Python documentation](https://docs.python.org/3/)
- The provided A-Maze-ing package and its documentation.
- [Pac-Man – Namco](https://en.wikipedia.org/wiki/Pac-Man)

**AI assistance:** we used Claude and Chatgpt to discuss project architecture and management, to review and debug our code and to design our pytest test suite. All code was written and understood by us; AI was not used to generate whole functions blindly.