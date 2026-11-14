# Virtual Environment
VENV = venv_pacman
# Python3 in virtual environment
PYTHON = $(VENV)/bin/python3
# PIP in virtual environment
PIP = $(VENV)/bin/pip
# Wheel files
# MAZE_WHL ?= $(*.whl)


$(VENV):
	python3 -m venv $(VENV)

# Install activity dependencies using pip, uv, pipx, or any other package manager of your choice.
install : $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install --requirement pacman_requirements.txt
# 	$(PIP) -m pip install --force-reinstall $(MAZE_WHL)

# Execute the main script of Pac-Man with config.json.
run :$(VENV)
	@$(PYTHON) pacman.py config.json

# Execute the main script of Pac-Man without configuration file.
noconfig :$(VENV)
	@$(PYTHON) pacman.py

# Run the main script in debug mode using Python’s built-in debugger (e.g., pdb).
debug : $(VENV)
	$(PYTHON) -m pdb pacman.py config.json

exe : $(VENV)
	$(PIP) install pyinstaller
	rm --force --recursive build dist
	$(VENV)/bin/pyinstaller \
		--onefile \
		--name pacman \
		--add-data "lib_pacman:./lib_pacman" \
		--add-data "config.json:./config.json" \
		--noconfirm \
		pacman.py
	rm --force --recursive build
	rm --force pacman.spec
	@echo "Exec file ready in dist directory (launch with : ./dist/pacman config.json)"

# Remove temporary files or caches (e.g., __pycache__, .mypy_cache) to keep the activity environment clean.
clean :
	rm --force --recursive __pycache__
	rm --force --recursive lib_pacman/__pycache__
	rm --force --recursive .mypy_cache

# Remove temporary files or caches and python virtual environment.
fclean : clean
	rm --force --recursive venv_pacman
	rm --force --recursive dist
	rm --force --recursive build
	rm --force pacman.spec

# flake8 . and mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
lint :
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# flake8 . and mypy .
lint-strict :
	flake8 .
	mypy . --strict
