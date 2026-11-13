# nominal-learning

The docs for Learning, Nominal's site of workshops and guides on test and measurement. Pages are
MyST Markdown in `docs/`, built with Sphinx and
[nominal-sphinx-theme](https://github.com/nominal-io/nominal-sphinx-theme).

The site has three tabs:

- **Workshops**: `docs/index.md` and `docs/test-stand-workshop/`.
- **Guides**: `docs/guides/`, deep dives with worked examples and cited sources.
- **Reference**: `docs/reference/glossary.md`.

- Before writing or editing any page, load the `nominal-docs:nominal-docs` skill. It holds the
  writing rules: accuracy, confidentiality, audience, style, terms and examples.
- If that skill isn't available, stop and tell your human. To install it, run
  `claude plugin marketplace add nominal-io/nominal-sphinx-theme`, then
  `claude plugin install nominal-docs@nominal`.
- Read [README.md](README.md) for how the docs are built and deployed.
- Everything in `docs/` is published, including `%` comments.

## Building and checking

Build before calling the work done.

- `just build` builds the docs into `docs/_build/dirhtml`. Warnings fail the build, as in CI.
- `just serve` serves a live preview.

## Conventions

- Styles, extensions and settings that other repos using the theme also need go in
  nominal-sphinx-theme, not into this repo. The `{gloss}` role is an exception for now: it's
  copied from the docs hub, in `docs/_ext/link_titles.py`, `docs/_static/gloss.js` and
  `docs/_static/gloss.css`.
- Link a glossary term with `{gloss}`. A term matches its glossary heading, with or without the
  heading's parenthesized part, so `{gloss}`DUT`` doesn't match "Device under test (DUT)".
- Cite sources as MyST footnotes, `[^name]`, defined under the page's last heading,
  `## References`. `docs/_static/cite.js` shows each source in a popup on hover. Put entry points
  for further reading in a `## Further reading` section above it. A footnote label can't match a
  heading's anchor.
- Write in-the-loop acronyms in title case: HiL, SiL, MiL, PiL.
- Before adding a Sphinx extension or tool, compare the alternatives (maintenance, and
  compatibility with Sphinx, MyST and the theme) and say why you chose one.
