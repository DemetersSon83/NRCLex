import json
from pathlib import Path

import pytest

from nrclex import NRCLex


def _write_lexicon(path: Path) -> Path:
    lexicon = {
        "happy": ["positive", "joy"],
        "sad": ["negative", "sadness"],
        "wow": ["surprise", "anticipation"],
    }
    path.write_text(json.dumps(lexicon), encoding="utf-8")
    return path


def test_repeated_tokens_scale_counts(tmp_path: Path) -> None:
    lexicon_path = _write_lexicon(tmp_path / "lexicon.json")
    analyzer = NRCLex(lexicon_file=lexicon_path)

    analyzer.load_token_list(["happy", "happy", "sad"])

    assert analyzer.raw_emotion_scores == {
        "positive": 2,
        "joy": 2,
        "negative": 1,
        "sadness": 1,
    }
    assert analyzer.affect_frequencies["positive"] == pytest.approx(2 / 6)
    assert analyzer.affect_frequencies["sadness"] == pytest.approx(1 / 6)


def test_no_matches_stable_zero_frequencies(tmp_path: Path) -> None:
    lexicon_path = _write_lexicon(tmp_path / "lexicon.json")
    analyzer = NRCLex(lexicon_file=lexicon_path)

    analyzer.load_token_list(["unknown", "tokens"])

    assert analyzer.raw_emotion_scores == {}
    assert all(v == 0.0 for v in analyzer.affect_frequencies.values())
    assert len(analyzer.top_emotions) == 10


def test_empty_token_list_stable_behavior(tmp_path: Path) -> None:
    lexicon_path = _write_lexicon(tmp_path / "lexicon.json")
    analyzer = NRCLex(lexicon_file=lexicon_path)

    analyzer.load_token_list([])

    assert analyzer.affect_list == []
    assert analyzer.affect_dict == {}
    assert analyzer.raw_emotion_scores == {}
    assert all(v == 0.0 for v in analyzer.affect_frequencies.values())


def test_default_constructor_loads_bundled_lexicon() -> None:
    analyzer = NRCLex()
    assert "abandon" in analyzer.__lexicon__


def test_relative_missing_lexicon_falls_back_to_bundled() -> None:
    analyzer = NRCLex(lexicon_file="does_not_exist.json")
    assert "abandon" in analyzer.__lexicon__


def test_missing_absolute_custom_path_raises() -> None:
    with pytest.raises(FileNotFoundError):
        NRCLex(lexicon_file=Path("/tmp/definitely_missing_nrclex_lexicon.json"))
