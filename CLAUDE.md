# nominal-learning

The docs for Learning, Nominal's site of workshops and guides on test and measurement. Pages are
MyST Markdown in `docs/`, built with Sphinx and
[nominal-sphinx-theme](https://github.com/nominal-io/nominal-sphinx-theme).

The site has three tabs:

- **Workshops**: `docs/index.md`, `docs/test-stand-workshop/`, `docs/integration-workshop/` and
  `docs/demo-workshop/`.
- **Guides**: `docs/guides/`, deep dives with worked examples and cited sources, and notebooks.
- **Reference**: `docs/reference/glossary.md`, and `docs/reference/sample-data/`, the docs of
  `learning.data`.

The guides are grouped into categories, each a captioned toctree in `docs/index.md`, a block on
`docs/guides/index.md`, and a landing page at `docs/guides/<category>/index.md`. Keep the three in
step. A category's notebooks are in its folder, and its landing page lists them. README.md, "Notebooks"
and "Sample data", covers the notebooks and `src/learning/data/`. `shelved/` holds guides taken off the site for now,
outside `docs/` so they aren't built. Nothing on the site links to them.

The guides and the glossary are general-purpose learning on industrial topics. Test and
measurement serves every industry, such as oil and gas, aerospace and manufacturing, so "test"
isn't a word to avoid. What to avoid is framing a topic around a generic test stand, which makes it
read as if it doesn't apply anywhere else. A dyno or a fluids panel can be a worked example,
introduced as one, but the topic, the leads and the definitions stay general. Name the example's
specifics, such as an e-axle as the dyno's DUT, only where they matter to the point.

- Before writing or editing any page, load the `nominal-docs:nominal-docs` skill, and follow it.
  Its rules are required, not suggestions: accuracy, confidentiality, audience, style, terms and
  examples.
- Sources are required. See [Sources](#sources).
- If that skill isn't available, stop and tell your human. To install it, run
  `claude plugin marketplace add nominal-io/nominal-sphinx-theme`, then
  `claude plugin install nominal-docs@nominal`.
- Read [README.md](README.md) for how the docs are built and deployed.
- Everything in `docs/` is published, including `%` comments.

## Building and checking

Build before calling the work done.

- `just build` builds the docs into `docs/_build/dirhtml`. Warnings fail the build, as in CI.
- `just serve` serves a live preview.
- `just check` and `just test` check the Python code and the notebooks' code, and test
  `learning.data`. Run them after changing either.

## Sources

Sources are required. Every claim on a page cites a source that says what the claim says. If
you can't find a source for a claim, take the claim out. The exception is details of the example
systems the guides use, such as a dyno or a fluids panel, which come from those systems'
manuals.

What your human tells you about their own experience, such as how one lab they worked at named
its systems, is a lead to research, not a source. Don't build a page around it. Find what
standards and published practice say, cite that, and note where practice differs.

- Cite sources as MyST footnotes, `[^name]`, defined under the page's last heading,
  `## References`. `docs/_static/cite.js` shows each source in a popup on hover.
- Put entry points for further reading in a `## Further reading` section above it.
- A footnote label can't match a heading's anchor.

## Conventions

- Styles, extensions and settings that other repos using the theme also need go in
  nominal-sphinx-theme, not into this repo. The `{gloss}` role is an exception for now: it's
  copied from the docs hub, in `docs/_ext/link_titles.py`, `docs/_static/gloss.js` and
  `docs/_static/gloss.css`.
- Link a glossary term with `{gloss}`. A term matches its glossary heading, with or without the
  heading's parenthesized part, so `{gloss}`DUT`` doesn't match "Device under test (DUT)".
- Write in-the-loop acronyms in title case: HiL, SiL, MiL, PiL.
- Before adding a Sphinx extension or tool, compare the alternatives (maintenance, and
  compatibility with Sphinx, MyST and the theme) and say why you chose one.
