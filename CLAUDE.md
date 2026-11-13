# nominal-school

Nominal Technical Content's docs. Pages are MyST Markdown in `docs/`, built with Sphinx and
[nominal-sphinx-theme](https://github.com/nominal-io/nominal-sphinx-theme).

The site's name will be decided later. It is not "Nominal School". Until then, call it "Nominal
Technical Content".

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
  nominal-sphinx-theme, through a PR there, not into this repo.
- Before adding a Sphinx extension or tool, compare the alternatives (maintenance, and
  compatibility with Sphinx, MyST and the theme) and say why you chose one.
