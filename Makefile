# Virtual Environment
VENV = venv_pacman
# Python3 in virtual environment
PYTHON = $(VENV)/bin/python3
# PIP in virtual environment
PIP = $(VENV)/bin/pip

$(VENV):
	python3 -m venv $(VENV)

# Install activity dependencies using pip, uv, pipx, or any other package manager of your choice.
install : $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install --requirement pacman_requirements.txt

# Execute the main script of your activity (e.g., via Python interpreter).
run :$(VENV)
	@$(PYTHON) pacman.py config.json

# Run the main script in debug mode using Python’s built-in debugger (e.g., pdb).
debug : $(VENV)
	$(PYTHON) -m pdb pacman.py config.json

package : $(VENV)
	$(PYTHON) -m build

# Remove temporary files or caches (e.g., __pycache__, .mypy_cache) to keep the activity environment clean.
clean :
	rm --force --recursive __pycache__
	rm --force --recursive .mypy_cache

# Remove temporary files or caches and python virtual environment.
fclean : clean
	rm --force --recursive venv_pacman

# flake8 . and mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
lint :
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# flake8 . and mypy .
lint-strict :
	flake8 .
	mypy . --strict
