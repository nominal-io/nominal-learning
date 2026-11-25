"""Format the code in every notebook under docs/ with ruff, at 85 columns so it fits the page.

A notebook is a MyST Markdown file with ``kernelspec`` in its front matter. Jupytext passes each one
to ruff as an ``.ipynb``, so only the code cells change.

Usage: ``python scripts/format_notebooks.py [--check]``. With ``--check``, nothing changes, and the
script fails if a notebook needs formatting.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
RUFF = "ruff format --line-length 85 --stdin-filename notebook.ipynb"


def notebooks() -> list[Path]:
    """Return the notebooks under docs/, skipping the build output."""
    found = []
    for path in sorted(DOCS.rglob("*.md")):
        if "_build" in path.relative_to(DOCS).parts:
            continue
        text = path.read_text(encoding="utf-8")
        front_matter = text.split("\n---", 1)[0] if text.startswith("---") else ""
        if "\nkernelspec:" in front_matter:
            found.append(path)
    return found


def main() -> int:
    """Run jupytext over the notebooks, piping their code through ruff."""
    check = "--check" in sys.argv[1:]
    mode = ["--check", f"{RUFF} --check -"] if check else ["--pipe", f"{RUFF} -"]
    paths = [str(path) for path in notebooks()]
    command = [sys.executable, "-m", "jupytext", "--from", "myst", "--pipe-fmt", "ipynb", *mode, *paths]
    return subprocess.run(command).returncode


if __name__ == "__main__":
    sys.exit(main())
