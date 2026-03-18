"""
code_generator.py
Applies the syllable and word-count ruleset to generate a 3-letter code
for any country name. Consults definitions.py and words.py.
"""

from definitions import get_syllables
from words import split_words, strip_connecting


def code_from_syllables(word):
    """
    Apply syllable rules to a single word → 3-letter string.

      1 syllable  → first 3 letters               (Spain   → SPA)
      2 syllables → first 2 letters + 1st letter of 2nd syllable (Sweden → SWD)
      3 syllables → first letter of each syllable  (Panama  → PNM)
      4+ syllables→ first letter of first 3 syllables (Algeria → AGI)
    """
    sylls = get_syllables(word)
    n = len(sylls)

    if n == 1:
        return word[:3].upper().ljust(3, word[0].upper())

    if n == 2:
        return (word[:2] + sylls[1][0]).upper()

    if n == 3:
        return "".join(s[0] for s in sylls).upper()


    return "".join(s[0] for s in sylls[:3]).upper()


def make_code(name):
    """
    Apply the full word-count + syllable ruleset to a country name.

      1 word  --> syllable rules
      2 words --> first 2 letters of word 1 + first letter of word 2
      3 words --> first letter of each word
      4+ words--> strip connecting words, take first letter of first 3 survivors
    """
    words = split_words(name)
    n = len(words)

    if n == 1:
        return code_from_syllables(words[0])

    if n == 2:
        return (words[0][:2] + words[1][0]).upper()

    if n == 3:
        return "".join(w[0] for w in words).upper()

    # 4+ words: strip connecting words, use first 3 survivors
    survivors = strip_connecting(words)[:3]
    return "".join(w[0] for w in survivors).upper()
