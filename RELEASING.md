# Releasing NRCLex

## 1) Choose version bump

- Patch: bug fixes only, no compatibility changes.
- Minor: backward-compatible features/packaging improvements.
- Major: intentional breaking changes.

For this modernization, use at least a **minor** bump if you changed supported Python versions.

## 2) Update version

Update these files together:

1. `pyproject.toml` → `[project].version`
2. `nrclex/__init__.py` → `__version__`

## 3) Validate locally

```bash
python -m pip install --upgrade pip
pip install -e . pytest build twine
pytest -q -m "not integration"
python -m build
twine check dist/*
```

Optional integration tests (requires corpora):

```bash
python -m textblob.download_corpora
pytest -q
```

## 4) Verify artifacts

Ensure **both** files exist:

- `dist/NRCLex-<version>.tar.gz`
- `dist/NRCLex-<version>-py3-none-any.whl`

## 5) Publish

```bash
twine upload dist/*
```

## 6) Don't forget

- Confirm `from nrclex import NRCLex` works from a clean environment.
- Confirm `NRCLex()` loads bundled lexicon without manual file path.
- Confirm dependency metadata does **not** list stdlib modules.
- Confirm `Requires-Python` matches supported versions (>=3.9).
- Tag release in git and add release notes.
