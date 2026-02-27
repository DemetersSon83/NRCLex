import pytest

textblob = pytest.importorskip("textblob")
from textblob import TextBlob
from textblob.exceptions import MissingCorpusError

from nrclex import NRCLex


@pytest.mark.integration
def test_load_raw_text_integration() -> None:
    try:
        _ = list(TextBlob("A tiny sentence.").sentences)
    except MissingCorpusError:
        pytest.skip("TextBlob corpora are not installed; skipping integration test")

    analyzer = NRCLex()
    analyzer.load_raw_text("I am happy but also sad.")

    assert "positive" in analyzer.affect_frequencies
    assert isinstance(analyzer.words, list)
