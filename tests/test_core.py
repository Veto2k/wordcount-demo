"""Tests for the wordcount core."""

import pytest

from wordcount.core import Report, most_common, normalise, word_count

SAMPLE = "The quick brown fox jumps over the lazy dog. The dog barks."


def test_normalise_lowercases_and_strips_punctuation():
    assert normalise("Hello, World!") == ["hello", "world"]


def test_normalise_keeps_apostrophes():
    assert normalise("it's fine") == ["it's", "fine"]


def test_word_count_counts_repeats():
    counts = word_count(SAMPLE)
    assert counts["the"] == 3
    assert counts["dog"] == 2


def test_word_count_can_drop_stop_words():
    counts = word_count(SAMPLE, drop_stop_words=True)
    assert "the" not in counts
    assert counts["dog"] == 2


def test_most_common_orders_by_frequency_then_alphabetically():
    assert most_common(SAMPLE, limit=2) == [("dog", 2), ("barks", 1)]


def test_most_common_rejects_bad_limit():
    with pytest.raises(ValueError):
        most_common(SAMPLE, limit=0)


def test_report_build():
    report = Report.build(SAMPLE, limit=3)
    assert report.total_words == 12
    assert report.unique_words == 9
    assert len(report.top) == 3


def test_lexical_density_of_empty_text_is_zero():
    assert Report.build("").lexical_density == 0.0


def test_lexical_density_is_a_ratio():
    assert 0 < Report.build(SAMPLE).lexical_density <= 1


def test_intentional_failure():
    assert word_count("a a b")["a"] == 99
