---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Install

{.lead}
`learning.data` has no dependencies of its own. Each format's library is an extra that you install when you
read that format. Its package, `nominal-learning`, is not published to PyPI, so install it from its repository:

```bash
pip install 'nominal-learning @ git+https://github.com/nominal-io/nominal-learning'          # paths only
pip install 'nominal-learning[med] @ git+https://github.com/nominal-io/nominal-learning'     # + wfdb and pandas
pip install 'nominal-learning[rf] @ git+https://github.com/nominal-io/nominal-learning'      # + numpy
pip install 'nominal-learning[aero] @ git+https://github.com/nominal-io/nominal-learning'    # + pandas
pip install 'nominal-learning[all] @ git+https://github.com/nominal-io/nominal-learning'
```

With `uv`, use `uv add 'nominal-learning[med]' --git https://github.com/nominal-io/nominal-learning`.
Inside this repository, `uv sync` installs it with every extra.

The extras set minimum versions only, such as `pandas>=2.0`, so they do not conflict with the versions your
project pins.

## What needs an extra

Paths work with no extras. `native` and `df` import their library the first time you use them. Without it
installed, they raise an error that names the extra to install:

```{code-cell} ipython3
import sys

import learning.data as nd
from learning.data import MissingExtraError

sys.modules["wfdb"] = None  # stands in for a project that did not install the extra

try:
    nd.med.ecg_mitbih_119.native
except MissingExtraError as error:
    print(error)
```

## Where downloads go

Most files ship in the package. A larger file downloads the first time you use its dataset, and is checked
against the sha256 in the dataset's manifest. Downloads go in `LEARNING_CACHE`, or in
`$XDG_CACHE_HOME/learning` (`~/.cache/learning` by default). `learning.data.cache_dir()`
returns the folder in use.

When a dataset is hosted in a private GitHub repository, set `LEARNING_TOKEN` or `GITHUB_TOKEN` to a
token that can read it. The token is sent only to GitHub.
