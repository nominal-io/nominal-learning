"""Sphinx config for the Nominal Learning docs."""

import os
import sys
from pathlib import Path

from nominal_sphinx_theme import intersphinx, theme_options

HERE = Path(__file__).resolve().parent

# _ext holds link_titles, copied from the docs hub's projects/_ext/ for its {gloss} role, and
# gallery, for the notebook-gallery directive on the category pages
sys.path.insert(0, str(HERE / "_ext"))

project = "Learning"
copyright = "Nominal, Inc."

# link_titles makes {gloss} terms, and shows Markdown link titles and card image alt text on hover
extensions = [
    "myst_nb",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx_design",
    "sphinx_copybutton",
    "nominal_sphinx_theme",
    "link_titles",
    "gallery",
]

# {gloss} terms link to reference/glossary.md, styled by gloss.css, with the popup from gloss.js.
# Citations are MyST footnotes ([^name]); cite.js shows each one's source in a popup, styled by cite.css.
nominal_glossary = "reference/glossary"
html_static_path = ["_static"]
html_css_files = ["gloss.css", "cite.css", "notebooks.css"]
html_js_files = [("gloss.js", {"defer": "defer"}), ("cite.js", {"defer": "defer"}), "image-zoom.js"]

exclude_patterns = ["_build", "**/.ipynb_checkpoints", "**/rf_radio_data"]

# -- Notebooks: MyST Markdown files with a kernelspec in their front matter ----------------------
# The cache re-runs only notebooks whose code changed.
nb_execution_mode = "cache"
nb_execution_cache_path = str(HERE / "_build" / ".jupyter_cache")
nb_execution_raise_on_error = True
nb_execution_show_tb = True  # print a failing cell's traceback, not only the log file's path
nb_execution_timeout = 600  # per cell; uploads wait for Nominal to ingest the data
# The notebooks under guides/ create resources in the Nominal workspace of the "default" profile, so
# a build runs them only when asked: set LEARNING_RUN_NOTEBOOKS=1. Otherwise they render with their
# code and no outputs. The sample data pages under reference/ need no profile, so they always run.
if not os.environ.get("LEARNING_RUN_NOTEBOOKS"):
    nb_execution_excludepatterns = ["guides/*.md", "guides/*/*.md"]

# Run the notebooks in this environment's kernel. A `python3` kernel in the user's own Jupyter folder
# would otherwise win, and it can point at another project's environment.
os.environ["JUPYTER_PATH"] = str(Path(sys.prefix) / "share" / "jupyter")
# Plotly figures as HTML (plotly.js from its CDN), so they render on the page and stay interactive.
# The kernels that run the notebooks inherit this; interactive Jupyter is unaffected.
os.environ["PLOTLY_RENDERER"] = "notebook_connected"
# The sample data pages download into a folder of their own, so a build never depends on what is cached.
os.environ["LEARNING_CACHE"] = str(HERE / "_build" / "samples-cache")

# The theme replaces the UUIDs in executed outputs with stand-ins, so published pages show no real IDs.
# Local builds keep the real ones, so you can follow a card's link to the resource; CI, which
# publishes, scrambles them. Set CI=1 to scramble locally.
nominal_scramble_output_ids = bool(os.environ.get("CI"))

# -- Autodoc: the learning.data reference pages, written from its docstrings --------------------
autodoc_member_order = "bysource"
autodoc_preserve_defaults = True
python_use_unqualified_type_names = True
add_module_names = False
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_rtype = False

# References such as {py:class}`~nominal.core.Asset` and [assets](inv:nominal:std:doc#guides/assets),
# and the names in code cells, link to the Python client's and instro's docs.
intersphinx_mapping = {
    **intersphinx("nominal", "instro"),
    "python": ("https://docs.python.org/3", None),
    "pandas": ("https://pandas.pydata.org/docs", None),
}

# each captioned sidebar group folds under its caption, starting open
nominal_sidebar_open = True

html_theme = "shibuya"
html_theme_options = theme_options(
    youtube_url="https://www.youtube.com/@nominal-io/shorts",
    nav_links=[
        {"title": "Workshops", "url": "index"},
        {"title": "Guides", "url": "guides/index"},
        {"title": "Reference", "url": "reference/glossary"},
    ],
)
