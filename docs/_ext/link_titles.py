"""Hover text (an HTML title) for links that Sphinx would otherwise render without one.

- {gloss}`ref name` links a term to its glossary entry, with the entry's first paragraph as hover text, which
  _static/gloss.js shows at once in a popup that links to the entry.
  {gloss}`ref names <ref name>` shows other text, such as a plural. The glossary page is the
  `nominal_glossary` setting (a docname); each `## Heading` there is a term, matched without case, with or
  without a trailing "(...)". An unknown term is a build warning.
  A project whose glossary is another project's sets `nominal_glossary` to that page's path from its own
  root (`../platform/reference/glossary`) and `nominal_glossary_url` to where the page is published
  (`/platform/reference/glossary/`); its terms then link there as site: links (site_links.py).
- A Markdown link's title, as in [ref name](glossary.md#ref-name "The name..."), shows on hover for links to other
  pages too. MyST keeps the title on the unresolved link, but resolving builds a new link and drops it; only the
  link's text node is copied across, so the title rides on that node and is put back afterwards.
- A sphinx-design card shows its image's alt text on hover. The card's link covers the whole card, so the image's
  own alt text never shows; a grid of icon cards can use it to carry a longer description than the card's text.
"""

import re
from pathlib import Path

from docutils import nodes
from myst_parser.mdit_to_docutils.base import default_slugify
from sphinx import addnodes
from sphinx.util import logging
from sphinx.util.docutils import ReferenceRole
from sphinx.util.nodes import make_refnode

logger = logging.getLogger(__name__)

_CARRIED = "nominal_link_title"
_GLOSS = "nominal-gloss"
# a "## Heading" line, a blank line, then the first paragraph
_ENTRY = re.compile(r"^## ([^\n]+)\n\n(.+?)(?=\n\n|\Z)", re.M | re.S)
_MARKUP = [(re.compile(r"!?\[([^\]]*)\]\([^)]*\)"), r"\1"), (re.compile(r"[`*]"), "")]
_cache = {}


def _glossary_path(env):
    return Path(env.srcdir) / f"{env.config.nominal_glossary}.md"


def _glossary(env):
    """Term (lowercase) -> (anchor, plain-text summary), reread whenever the glossary page changes."""
    path = _glossary_path(env)
    mtime = path.stat().st_mtime
    if path not in _cache or _cache[path][0] != mtime:
        terms = {}
        for heading, summary in _ENTRY.findall(path.read_text(encoding="utf-8")):
            for pattern, repl in _MARKUP:
                summary = pattern.sub(repl, summary)
            entry = (default_slugify(heading), " ".join(summary.split()))
            terms[heading.lower()] = entry
            terms[re.sub(r"\s*\(.*\)$", "", heading).lower()] = entry
        _cache[path] = (mtime, terms)
    return _cache[path][1]


class GlossaryRole(ReferenceRole):
    def run(self):
        entry = _glossary(self.env).get(self.target.lower())
        self.env.note_dependency(str(_glossary_path(self.env)))
        if entry is None:
            logger.warning("glossary term not found: %r", self.target, location=self.get_location())
            return [nodes.Text(self.title)], []
        anchor, summary = entry
        url = self.env.config.nominal_glossary_url
        if url:
            # another project's glossary: a site: link, which site_links.py makes relative
            ref = nodes.reference(self.rawtext, "", refuri=f"site:{url}#{anchor}", reftitle=summary, classes=["gloss"])
            ref += nodes.inline(self.title, self.title, classes=["xref", "gloss"])
            return [ref], []
        xref = addnodes.pending_xref(
            self.rawtext, refdomain="", reftype=_GLOSS, reftarget=anchor, refdoc=self.env.docname, gloss_title=summary
        )
        xref += nodes.inline(self.title, self.title, classes=["xref", "gloss"])
        return [xref], []


def _resolve_gloss(app, env, node, contnode):
    if node.get("reftype") != _GLOSS:
        return None
    ref = make_refnode(
        app.builder, node["refdoc"], env.config.nominal_glossary, node["reftarget"], contnode, node["gloss_title"]
    )
    ref["classes"].append("gloss")  # styled apart from links to content (_static/gloss.css)
    return ref


def _carry_titles(app, doctree):
    for xref in doctree.findall(addnodes.pending_xref):
        # MyST puts a link's title in "title" for links to other pages, "reftitle" elsewhere
        title = xref.get("title") or xref.get("reftitle")
        if not (title and len(xref) and isinstance(xref[0], nodes.Element)):
            continue
        # Resolving a link to another page keeps only the text node's children, so wrap them in one that carries it
        text = xref[0]
        carrier = nodes.inline("", "", *text.children, **{_CARRIED: title})
        del text[:]
        text += carrier


def _restore_titles(app, doctree, docname):
    for ref in doctree.findall(nodes.reference):
        carrier = next((n for n in ref.findall(nodes.inline) if n.get(_CARRIED)), None)
        if carrier is not None:
            ref["reftitle"] = carrier[_CARRIED]
    for card in doctree.findall(nodes.container):
        if "sd-card" not in card["classes"]:
            continue
        image = next(card.findall(nodes.image), None)
        if image is None or not image.get("alt"):
            continue
        for ref in card.findall(nodes.reference):
            if "sd-stretched-link" in ref["classes"]:
                ref["reftitle"] = image["alt"]


def setup(app):
    app.add_config_value("nominal_glossary", "glossary", "env")
    # set when nominal_glossary is another project's page: where that page is published (/platform/reference/glossary/)
    app.add_config_value("nominal_glossary_url", None, "env")
    app.add_role("gloss", GlossaryRole())
    app.connect("missing-reference", _resolve_gloss)
    app.connect("doctree-read", _carry_titles)
    app.connect("doctree-resolved", _restore_titles)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
