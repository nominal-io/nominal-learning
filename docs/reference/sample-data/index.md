---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Sample data

{.lead}
`learning.data` holds sample datasets for Nominal's open-source projects, grouped by domain: `aero`, `med` and `rf`.

Each dataset is a {py:class}`~learning.data.Dataset` with up to three ways to be accessed:

* as a file path, with {py:attr}`~learning.data.Dataset.path`
* as its format's own Python object, with {py:attr}`~learning.data.Dataset.native`
* as a pandas {py:class}`~pandas.DataFrame`, with {py:attr}`~learning.data.Dataset.df`

## Usage 
Import a dataset from its domain: {py:mod}`~learning.data.aero`, {py:mod}`~learning.data.med` or
{py:mod}`~learning.data.rf`. Importing reads only a small manifest; nothing is downloaded or parsed
until you use the dataset.

+++

### As Path

```{code-cell} ipython3
from learning.data.med import ecg_mitbih_119

ecg_mitbih_119.path  # a Path, to pass to your own loader
```

The same dataset as the Python object that its format's library returns, and as a DataFrame. A dataset
has each only where it makes sense; see {py:attr}`~learning.data.Dataset.forms`.

+++

### As Native

```{code-cell} ipython3
ecg_mitbih_119.native  # a wfdb.Record
```

### As Dataframe

```{code-cell} ipython3
ecg_mitbih_119.df.head()
```

To work with the domains as a group, import the package under a short name.
{py:func}`~learning.data.catalog` lists the datasets, and {py:func}`~learning.data.get` looks one up by id:

```{code-cell} ipython3
import learning.data as nd

nd.catalog("rf")
```

[Install](install.md) the package with the extras for the formats you read.
[Using the paths](paths.md) covers testing a file loader, and
[Using the loaded data](loaded.md) covers `native` and `df`, including
{py:class}`~learning.data.FormUnavailable`, which a dataset raises for a form it does not have.
The [catalog](catalog.md) lists every dataset, and [Adding a dataset](adding.md)
explains how to contribute one. The [API](api.md) is the full reference.
