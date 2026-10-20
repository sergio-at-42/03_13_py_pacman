*This activity has been created as part of the 42 curriculum by [sansaidi], [sbeldjao].*

# A COMPLETER (base sur le README.md de A_MAZE_ING)

# Pac-Man

## Description

First released in 1980 by Namco, Pac-Man quickly became a cultural icon and one of the most influential video games of all time. Designed by Toru Iwatani, its goal was to create a game that could appeal to women and casual players, contrasting with the space shooters of the era. The game introduced the now-famous ghost AI, each with unique behaviors (Blinky chases, Pinky ambushes, Inky is unpredictable, and Clyde is. . . weird).  
Pac-Man was also the first game to popularize the concept of a power-up — the Pacgum (or Power Pellets) that lets you eat the ghosts. The original arcade machine had 256 levels, but due to an integer overflow bug, level 256 was impossible to finish, known as the infamous “kill screen”.  

## Instructions

Requirements: Python 3.10+.

```bash
make install   # install dependencies
make run       # run with config.txt
make debug     # run with pdb
make clean     # remove caches
make lint      # flake8 + mypy
```

Or directly:
- Create a virtual environment and install dependencies:
```bash
python3 -m venv venv_pacman
source venv_pacman/bin/activate
pip install -r requirements.txt
```
- Run the program:
```bash
python3 pacman.py config.txt
```

`config.txt` can be replaced with any file following the format below.


## Configuration file format

One `KEY=VALUE` pair per line. Lines starting with `#` are comments.

| Key           | Description                     | Example              |
|---------------|----------------------------------|-----------------------|
| WIDTH         | Maze width (cells)               | `WIDTH=20`            |
| HEIGHT        | Maze height (cells)              | `HEIGHT=15`           |
| ENTRY         | Entry coordinates                | `ENTRY=0,0`           |
| EXIT          | Exit coordinates                 | `EXIT=19,14`          |
| OUTPUT_FILE   | Output filename                  | `OUTPUT_FILE=maze.txt`|
| PERFECT       | Perfect maze mode (True/False)   | `PERFECT=False`       |
| SEED          | Seed for reproducible generation | `SEED=42`             |

### Build the package from source
```bash
# In a virtualenv, from the root of the repository
python3 -m venv build_venv
source build_venv/bin/activate
pip install build
python -m build
# Output files will be in dist/
cp dist/mazegen-1.0.0-py3-none-any.whl .
cp dist/mazegen-1.0.0.tar.gz .
```

### Install the package
```bash
pip install mazegen-1.0.0-py3-none-any.whl
# or
pip install mazegen-1.0.0.tar.gz
```

## Maze generation algorithm

We used an **iterative depth-first search (recursive backtracker)**, with
each cell stored as a 4-bit integer (one bit per wall: N/E/S/W). Breaking a
wall is a simple bitwise operation, applied to both neighbouring cells at
once to guarantee consistent wall encoding.

We chose this algorithm because it maps directly onto the required output
format — the internal grid representation *is* the hexadecimal encoding, no
conversion step needed. It's also simple to reason about and to test in
isolation.

For the playable (non-perfect) mode, we start from the perfect maze and
"braid" it: open the four corners and the centre, add extra loops, then
target and remove real dead-ends one by one — always checking that no 3x3
area becomes fully open. The shortest path is found with a standard BFS,
which works identically on both modes regardless of loops.

## Reusable module

All the generation and solving logic lives in `mazegen.py`, a single,
dependency-free file built as `mazegen-*.whl` for later reuse via pip. It
exposes the `MazeGenerator` class:

```python
from mazegen import MazeGenerator

generator = MazeGenerator(width=20, height=15, entry=(0, 0), exit=(19, 14),
                           seed=42, perfect=False)
generator.generate()
path = generator.solution_path      # shortest path, as N/E/S/W letters
```

The rest of the project (`libmaze/`) handles config parsing and display, and
depends on this module — not the other way around.

## Resources

- ["Generating a Maze with DFS"](https://makeschool.org/mediabook/oa/tutorials/trees-and-mazes/generating-a-maze-with-dfs/) — introduced us to the bitwise wall representation
- Standard graph theory: spanning trees, BFS shortest path, cyclomatic number for counting independent loops
- **AI usage**: we used Claude to discuss algorithm design choices (bitwise vs. object-based wall representation, DFS vs. braiding for the Pac-Man mode), to review and debug our code (import structure, state bugs across re-generation), and to design our pytest test suite. All code was written and understood by us; AI was not used to generate whole functions blindly.

## Team and project management

- **sansaidi**: maze generation and solving algorithm, tests, packaging (mazegen), README
- **sbeldjao**: config parsing, terminal display, Makefile

**Planning**: initial plan was parsing/config → perfect maze generation →
display → non-perfect (Pac-Man) mode → path solving. Work was split so each
person owned one module (generator vs. display) and developed/tested it
independently. In practice, the generator and display phases overlapped more
than planned, since the display needed a working generator interface early to
start testing, which pushed some interface decisions earlier than expected.

**What worked well**: working on separate branches per module avoided merge
conflicts, and keeping the generator and display fully independent (one only
exposes data, the other only consumes it) made both parts testable in
isolation.

**What could be improved**: the interface between the two modules (parameter
names, coordinate conventions, how to access the solution) should have been
agreed on explicitly before starting, rather than discovered through
integration bugs afterward — clearer upfront communication would have saved
debugging time later.

Tools used: `pytest` for unit/integration tests, `maze_analyzer.py`
(provided) to cross-check maze validity independently of our own tests,
`flake8`/`mypy` for linting. 

