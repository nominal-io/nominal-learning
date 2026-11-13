# nominal-school

Nominal Technical Content's docs: MyST Markdown pages in `docs/`, built with Sphinx and
[nominal-sphinx-theme](https://github.com/nominal-io/nominal-sphinx-theme).

## Running locally

Needs Python 3.12+, [uv](https://docs.astral.sh/uv/) and [just](https://just.systems).

```bash
just install      # install the docs toolchain
just build        # build into docs/_build/dirhtml; warnings fail it, as in CI
just serve        # live preview on http://127.0.0.1:8000 (`just serve 8001` for another port)
```

## Workflows

| Workflow | Runs | Does |
|---|---|---|
| `deploy-docs.yml` | Pushes to `main`, and by hand | Builds the docs and deploys them to this repo's GitHub Pages |
| `docs.yml` | Pull requests | Builds the docs with warnings as errors, links a preview, and runs `docs-gate / gate` |
| `bump-theme.yml` | Daily, and by hand | Opens a PR that moves the theme pin in `uv.lock` to the theme's newest commit |

The theme's README, "CI", has how the bump, the gate and the preview work.

## Publishing on dev.nominal.io

dev.nominal.io pulls the docs from this repo's latest GitHub Pages upload. To publish them there,
add a `[[project]]` to its `sites.toml`, and the project to its `[groups]`:

```toml
[[project]]
project = "school"                  # the URL, /school/
repo = "nominal-io/nominal-school"
workflow = "deploy-docs.yml"
```
