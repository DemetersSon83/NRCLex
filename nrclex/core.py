"""Core NRCLex implementation."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from importlib import resources
from itertools import chain
import json
from pathlib import Path
from typing import Dict, Iterable, Optional, Union

DEFAULT_LEXICON_FILENAME = "nrc_en.json"
EMOTION_ORDER = (
    "fear",
    "anger",
    "anticipation",
    "trust",
    "surprise",
    "positive",
    "negative",
    "sadness",
    "disgust",
    "joy",
)


@lru_cache(maxsize=None)
def _load_bundled_lexicon() -> Dict[str, list[str]]:
    """Load the bundled NRC lexicon once and cache it."""
    data_path = resources.files("nrclex.data").joinpath(DEFAULT_LEXICON_FILENAME)
    with data_path.open("r", encoding="utf-8") as json_file:
        return json.load(json_file)


@lru_cache(maxsize=None)
def _load_lexicon_from_path(path: str) -> Dict[str, list[str]]:
    """Load a lexicon JSON file from a specific filesystem path once."""
    with Path(path).open("r", encoding="utf-8") as json_file:
        return json.load(json_file)


class NRCLex:
    """NRC emotion lexicon wrapper for tokenized text or raw text via TextBlob."""

    def __init__(self, lexicon_file: Optional[Union[str, Path]] = DEFAULT_LEXICON_FILENAME):
        self.__lexicon__ = self._resolve_lexicon(lexicon_file)

    def _resolve_lexicon(self, lexicon_file: Optional[Union[str, Path]]) -> Dict[str, list[str]]:
        """Resolve the lexicon source with a robust packaged fallback."""
        if lexicon_file is None:
            return _load_bundled_lexicon()

        candidate = Path(lexicon_file)
        if candidate.exists():
            return _load_lexicon_from_path(str(candidate.resolve()))

        value = str(lexicon_file)
        if value == DEFAULT_LEXICON_FILENAME or not candidate.is_absolute():
            return _load_bundled_lexicon()

        raise FileNotFoundError(
            f"Lexicon file '{lexicon_file}' was not found. "
            f"Pass an existing path, or use None/{DEFAULT_LEXICON_FILENAME!r} for the bundled lexicon."
        )

    def _build_word_affect(self) -> None:
        """Build affect attributes for the currently loaded tokens."""
        lexicon = self.__lexicon__
        words = self.words

        matched_words = [word for word in words if word in lexicon]
        affect_list = list(chain.from_iterable(lexicon[word] for word in matched_words))
        affect_dict = {word: lexicon[word] for word in matched_words}

        affect_frequencies = Counter(affect_list)
        total = sum(affect_frequencies.values())
        affect_percent = {emotion: 0.0 for emotion in EMOTION_ORDER}
        if total:
            for emotion, count in affect_frequencies.items():
                affect_percent[emotion] = float(count) / float(total)

        self.affect_list = affect_list
        self.affect_dict = affect_dict
        self.raw_emotion_scores = dict(affect_frequencies)
        self.affect_frequencies = affect_percent

    def _compute_top_emotions(self) -> None:
        """Compute top emotions from affect frequencies."""
        emo_dict = self.affect_frequencies
        max_value = max(emo_dict.values())
        self.top_emotions = [
            (emotion, score)
            for emotion, score in emo_dict.items()
            if score == max_value
        ]

    def load_token_list(self, token_list: Iterable[str]) -> None:
        """Load pre-tokenized text for affect analysis."""
        self.text = ""
        self.words = list(token_list)
        self.sentences = []
        self._build_word_affect()
        self._compute_top_emotions()

    def load_raw_text(self, text: str) -> None:
        """Load raw text and tokenize/lemmatize with TextBlob before analysis."""
        self.text = text
        try:
            from textblob import TextBlob
        except ImportError as exc:
            raise ImportError("TextBlob is required for load_raw_text(). Install NRCLex with its dependencies.") from exc

        blob = TextBlob(self.text)
        self.words = [w.lemmatize() for w in blob.words]
        self.sentences = list(blob.sentences)
        self._build_word_affect()
        self._compute_top_emotions()
