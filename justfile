# Recipes run in PowerShell on Windows (no bash or cygpath needed) and sh elsewhere.
[windows]
set shell := ["powershell.exe", "-NoLogo", "-NoProfile", "-Command"]

# list the recipes
default:
    @just --list

# install the docs toolchain (Python 3.12+)
install:
    uv sync

# build the docs into docs/_build/dirhtml; warnings fail it, as in CI
build:
    uv run sphinx-build -E -W --keep-going -j auto -b dirhtml docs docs/_build/dirhtml

# live-preview the docs on http://127.0.0.1:<port>, rebuilding on edits (`just serve 8001` for another port)
serve port="8000":
    uv run --with sphinx-autobuild sphinx-autobuild -j auto -b dirhtml --port {{port}} docs docs/_build/dirhtml
