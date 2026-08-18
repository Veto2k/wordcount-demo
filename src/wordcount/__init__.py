"""A tiny text-statistics library used as the pipeline's demo target."""

from .core import Report, most_common, normalise, word_count

__all__ = ["Report", "most_common", "normalise", "word_count"]
__version__ = "0.2.0"
