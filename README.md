# nominal-learning

The docs for Learning, Nominal's workshops, guides and notebooks on test and measurement: MyST Markdown
pages in `docs/`, built with Sphinx and
[nominal-sphinx-theme](https://github.com/nominal-io/nominal-sphinx-theme). The repo also holds
`learning.data`, the sample datasets that the notebooks use.

## Running locally

Needs Python 3.12+, [uv](https://docs.astral.sh/uv/) and [just](https://just.systems).

```bash
just install      # the docs toolchain, the notebooks' dependencies, JupyterLab and Jupytext
just build        # build into docs/_build/dirhtml; warnings fail it, as in CI
just serve        # live preview on http://127.0.0.1:8000 (`just serve 8001` for another port)
just notebook     # open the docs folder in JupyterLab, where .md files open as notebooks
just check        # lint and type-check the Python code, and check the notebooks' code formatting
just fix          # format the Python code and the notebooks' code
just test         # test learning.data; `just test -m network` also downloads real files
```

## Layout

```text
docs/                       the site: workshops, guides, notebooks and reference
docs/guides/<category>/     a category's landing page and its notebooks
docs/guides/notebooks/      Running the notebooks, and the notebooks that fit no category
docs/reference/sample-data/ the learning.data docs
docs/_ext/                  the {gloss} role
docs/_static/thumbnails/    the category pages' card pictures, drawn by gen/guide_thumbnails.py
src/learning/data/          the sample datasets: `from learning.data.rf import sigmf_synthetic`
gen/                        scripts that generate datasets and thumbnails, for traceability
tests/                      tests of learning.data
.jupyter/                   makes JupyterLab open .md files as notebooks
```

## Notebooks

A notebook is a MyST Markdown file with a `kernelspec` in its front matter, edited in JupyterLab
through Jupytext. Most guides in `docs/guides/` are notebooks: their prose is Markdown, and code cells
work through what the prose explains, plotting with `learning.style.set_matplotlib_style()`. A notebook
that isn't a guide goes in its category's folder under `docs/guides/`. Add a new page to the category's
toctree in `docs/index.md`, and add a card for it to the category's `index.md`. A card's picture is a
screenshot from the notebook, or a thumbnail that `gen/guide_thumbnails.py` draws (`just gen-thumbnails`).
Add its dependencies with `uv add --group notebooks <package>`.

`just build` runs every notebook, so the published pages show their outputs. The exception is a
notebook whose code cells connect to Nominal with a profile: it creates resources in that profile's
workspace, so the build runs it only when `LEARNING_RUN_NOTEBOOKS=1` is set, and otherwise renders it
with its code and no outputs. Keep a guide's code cells free of Nominal connections, so it always runs;
show Nominal code there as a plain `python` block.

## Sample data

`learning.data` holds sample datasets, grouped by domain (`aero`, `med`, `rf`). It has no
dependencies of its own; install the extras for the formats you read, such as
`nominal-learning[med]`. `docs/reference/sample-data/` documents it.

```bash
just gen-flight   # regenerate the simulated flight telemetry
just hash-files src/learning/data/aero/flight_dc   # print its [[files]] manifest entries
```

## Workflows

| Workflow | Runs | Does |
|---|---|---|
| `deploy-docs.yml` | Pushes to `main`, and by hand | Builds the docs and deploys them to this repo's GitHub Pages |
| `docs.yml` | Pull requests | Checks the code, tests `learning.data`, builds the docs with warnings as errors, links a preview, and runs `docs-gate / gate` |
| `bump-theme.yml` | Daily, and by hand | Opens a PR that moves the theme pin in `uv.lock` to the theme's newest commit |

The theme's README, "CI", has how the bump, the gate and the preview work.

## Publishing on dev.nominal.io

dev.nominal.io pulls the docs from this repo's latest GitHub Pages upload. To publish them there,
add a `[[project]]` to its `sites.toml`, and the project to its `[groups]`:

```toml
[[project]]
project = "learning"                # the URL, /learning/
repo = "nominal-io/nominal-learning"
workflow = "deploy-docs.yml"
```
