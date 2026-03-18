"""
words.py
Handles splitting country names into words and stripping connecting words.
"""

import re

CONNECTING_WORDS = {
    "of", "and", "the", "a", "an", "in", "on", "at", "to",
    "for", "with", "by", "from", "or", "nor", "but", "de",
    "da", "du", "des", "le", "la", "les", "el", "los", "las",
    "van", "von", "und", "et", "e", "y",
}


def split_words(name):
    """Split a country name into words. Treats hyphens as word boundaries."""
    return re.split(r"[\s\-]+", name.strip())


def strip_connecting(words):
    """
    Remove connecting words from a list, returning only content words.
    Used when a name has 4+ words.
    """
    return [w for w in words if w.lower() not in CONNECTING_WORDS]


def is_connecting(word):
    """Check if a single word is a connecting word."""
    return word.lower() in CONNECTING_WORDS
