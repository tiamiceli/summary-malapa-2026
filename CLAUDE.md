Use python with uv as a package manager.

## Jupyter notebooks — commit outputs, strip metadata

Notebooks (`*.ipynb`) are committed **with their outputs**, but with churny
metadata (`execution_count`, per-cell metadata) stripped, using
[nbstripout](https://github.com/kynan/nbstripout) as a git *clean* filter.
`.gitattributes` (committed) wires `*.ipynb` to the filter, but the filter
itself lives in `.git/config` (per-clone, never committed), so it must be
configured in every clone:

```bash
uv run nbstripout --install --keep-output
# nbstripout's --install does NOT reliably bake in --keep-output, so set the
# clean command explicitly (this is what actually keeps the outputs):
git config filter.nbstripout.clean 'uv run --quiet nbstripout --keep-output'
git add --renormalize .
```

**Before committing any `.ipynb`:** confirm `git config filter.nbstripout.clean`
contains `--keep-output`. A correctly filtered staged notebook keeps its
`outputs` but has every `execution_count` set to `null` — check with
`git show :<file>.ipynb`. Without `--keep-output` the filter silently strips all
outputs on commit.
