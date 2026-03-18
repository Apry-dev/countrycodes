"""
definitions.py
Core syllable utilities. All other modules import from here.
"""

import pyphen

dic = pyphen.Pyphen(lang='en_US')


def count_syllables(word):
    hyphenated = dic.inserted(word.lower())  # e.g. "beau-ti-ful"
    return hyphenated.count('-') + 1         # hyphens + 1 = syllable count


def get_syllables(word):
    """Return a list of syllable strings for a single word."""
    hyphenated = dic.inserted(word.lower())
    return hyphenated.split('-')


def syllables_from_word(word):
    count = count_syllables(word)
    parts = dic.inserted(word.lower())
    return {
        "word": word,
        "syllables": count,
        "breakdown": parts
    }
