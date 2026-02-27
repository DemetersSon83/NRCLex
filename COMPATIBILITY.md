# Compatibility Notes (vs NRCLex 4.0 behavior)

## Comparison method

Because external network access is unavailable in this environment, direct installation of `NRCLex==4.0` from PyPI was not possible. Instead, behavior was compared against the repository's 4.0 implementation logic using the same bundled lexicon data.

## Results

### `load_token_list`

For token list `['happy', 'sad', 'unknown', 'happy']`, the updated implementation produced identical values to the 4.0 logic for:

- `raw_emotion_scores`
- `affect_frequencies`
- `top_emotions`

### Constructor behavior (`NRCLex()`)

- **4.0 behavior:** default `lexicon_file='nrc_en.json'` required current working directory assumptions and could fail after installation.
- **Updated behavior:** `NRCLex()` now reliably loads bundled `nrclex/data/nrc_en.json` via `importlib.resources`.

This constructor change is intentional and improves install-time reliability without changing the public API.

## Metadata corrections (intentional)

- Removed stdlib entries (`collections`, `json`) from dependencies.
- Set `Requires-Python` to `>=3.9` to align with TextBlob support expectations.
