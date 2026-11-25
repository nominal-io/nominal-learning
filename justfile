# Recipes run in PowerShell on Windows (no bash or cygpath needed) and sh elsewhere.
[windows]
set shell := ["powershell.exe", "-NoLogo", "-NoProfile", "-Command"]

# list the recipes
default:
    @just --list

# install the docs toolchain, the notebooks' dependencies, JupyterLab and Jupytext (Python 3.12+)
install:
    uv sync
    @just _jupyterlab-settings

# make this environment's JupyterLab open .md files as notebooks
_jupyterlab-settings:
    uv run python -c "import pathlib, shutil; d = pathlib.Path('.venv/share/jupyter/lab/settings'); d.mkdir(parents=True, exist_ok=True); shutil.copy('.jupyter/overrides.json', d)"

# open the docs folder in JupyterLab, where .md files open as notebooks
notebook *args: _jupyterlab-settings
    uv run jupyter lab docs {{args}}

# build the docs into docs/_build/dirhtml; warnings fail it, as in CI. Set LEARNING_RUN_NOTEBOOKS=1 to run the guides' notebooks too
build:
    uv run sphinx-build -E -W --keep-going -j auto -b dirhtml docs docs/_build/dirhtml

# live-preview the docs on http://127.0.0.1:<port>, rebuilding on edits (`just serve 8001` for another port)
serve port="8000":
    uv run --with sphinx-autobuild sphinx-autobuild -j auto -b dirhtml --port {{port}} --watch src --ignore docs/_build --re-ignore ipynb_checkpoints --re-ignore rf_radio_data docs docs/_build/dirhtml

# lint the Python code, check its types, and check the formatting of notebook code | fix with `just fix`
check:
    uv run ruff check
    uv run ruff format --check
    uv run mypy
    uv run python scripts/format_notebooks.py --check

# format the Python code and notebook code (note: mutates the notebooks)
fix:
    uv run ruff check --fix
    uv run ruff format
    uv run python scripts/format_notebooks.py

# run the tests of learning.data; `just test -m network` also downloads real files
test *args:
    uv run pytest {{args}}

# regenerate learning.data's aero/flight_dc telemetry; then update its sha256 in dataset.toml with `just hash-files`
gen-flight:
    uv run --group gen python gen/aero_flight_dc.py

# redraw the thumbnails on the category pages' cards, in docs/_static/thumbnails/
gen-thumbnails:
    uv run --group gen python gen/guide_thumbnails.py

# print [[files]] manifest entries for a dataset folder, such as src/learning/data/aero/flight_dc
hash-files folder:
    uv run python scripts/hash_files.py "{{folder}}"
