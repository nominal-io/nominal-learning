# learning.data API

```{eval-rst}
.. automodule:: learning.data
   :no-members:

.. autofunction:: learning.data.catalog
.. autofunction:: learning.data.get
.. autofunction:: learning.data.domains
.. autofunction:: learning.data.cache_dir
```

## Domains

Each domain module resolves dataset names when you import them, so there is no fixed list of attributes.
`dir()` of a domain lists its datasets; the {doc}`catalog <catalog>` shows them all.

```{eval-rst}
.. automodule:: learning.data.aero
.. automodule:: learning.data.med
.. automodule:: learning.data.rf
```

## Dataset

```{eval-rst}
.. autoclass:: learning.data.Dataset
   :members: from_dir, id, size, is_local, forms, paths, path, native, df, verify

.. autoclass:: learning.data.FileSpec
   :members:
```

## Errors

```{eval-rst}
.. autoexception:: learning.data.SamplesError
.. autoexception:: learning.data.ManifestError
.. autoexception:: learning.data.ChecksumError
.. autoexception:: learning.data.FormUnavailable
.. autoexception:: learning.data.MissingExtraError
```
