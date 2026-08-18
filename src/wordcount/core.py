"""Word frequency helpers.

Deliberately small: the point of this package is to give the pipeline something
real to build, test, lint, and measure coverage against.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

WORD = re.compile(r"[a-z0-9']+")
STOP_WORDS = frozenset({"the", "a", "an", "and", "or", "of", "to", "in", "is", "it"})


def normalise(text):
    """Split text into lowercase word tokens."""
    return WORD.findall(text.lower())


def word_count(text, drop_stop_words=False):
    """Count how often each word appears in ``text``."""
    tokens = normalise(text)
    if drop_stop_words:
        tokens = [t for t in tokens if t not in STOP_WORDS]
    return dict(Counter(tokens))


def most_common(text, limit=5, drop_stop_words=True):
    """Return the ``limit`` most frequent words, highest first."""
    if limit < 1:
        raise ValueError("limit must be at least 1")
    counts = word_count(text, drop_stop_words=drop_stop_words)
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]


@dataclass(frozen=True)
class Report:
    """A summary of one body of text."""

    total_words: int
    unique_words: int
    top: list

    @property
    def lexical_density(self):
        """Ratio of unique words to total words, 0.0 for empty input."""
        if self.total_words == 0:
            return 0.0
        return round(self.unique_words / self.total_words, 4)

    @classmethod
    def build(cls, text, limit=5):
        counts = word_count(text)
        return cls(
            total_words=sum(counts.values()),
            unique_words=len(counts),
            top=most_common(text, limit=limit),
        )
