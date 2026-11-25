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
docs/_ext/                  the {gloss} role and the notebook-gallery directive
src/learning/data/          the sample datasets: `from learning.data.rf import sigmf_synthetic`
gen/                        scripts that generate datasets, for traceability
tests/                      tests of learning.data
.jupyter/                   makes JupyterLab open .md files as notebooks
```

## Notebooks

A notebook is a MyST Markdown file with a `kernelspec` in its front matter, edited in JupyterLab
through Jupytext. Put it in its category's folder under `docs/guides/`, and add it to the category's
toctree in `docs/index.md`. The category page's `notebook-gallery` lists it. Add its dependencies with
`uv add --group notebooks <package>`.

The notebooks under `docs/guides/` create resources in the Nominal workspace of the `default`
profile, so `just build` runs them only when `LEARNING_RUN_NOTEBOOKS=1` is set. Otherwise they render
with their code and no outputs. The pages under `docs/reference/sample-data/` need no profile, so
they always run.

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
