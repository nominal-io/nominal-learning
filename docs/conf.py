"""Sphinx config for the Nominal Learning docs."""

import sys
from pathlib import Path

from nominal_sphinx_theme import theme_options

# link_titles, copied from the docs hub's projects/_ext/ for its {gloss} role
sys.path.insert(0, str(Path(__file__).resolve().parent / "_ext"))

project = "Learning"
copyright = "Nominal, Inc."

# link_titles makes {gloss} terms, and shows Markdown link titles and card image alt text on hover
extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx_copybutton",
    "nominal_sphinx_theme",
    "link_titles",
]

# {gloss} terms link to reference/glossary.md, styled by gloss.css, with the popup from gloss.js.
# Citations are MyST footnotes ([^name]); cite.js shows each one's source in a popup, styled by cite.css.
nominal_glossary = "reference/glossary"
html_static_path = ["_static"]
html_css_files = ["gloss.css", "cite.css"]
html_js_files = [("gloss.js", {"defer": "defer"}), ("cite.js", {"defer": "defer"})]

exclude_patterns = ["_build"]

html_theme = "shibuya"
html_theme_options = theme_options(
    youtube_url="https://www.youtube.com/@nominal-io/shorts",
    nav_links=[
        {"title": "Workshops", "url": "index"},
        {"title": "Guides", "url": "guides/index"},
        {"title": "Reference", "url": "reference/glossary"},
    ],
)
