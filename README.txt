## Synopsis

This project is an idea I had when I was thinking about country codes and how they work and was thinking that some of
them don't really make sense to me
Like British Virgin Islands being 'VGB' instead of 'BVI' and Central African Republic being 'CAF' instead of 'CAR'

My solution is based on syllable count and word count.
The way I've implemented it is based off of the following rules


1 syllable country = first 3 letters (Spain = spa)
2 syllable country = first 2 letters plus first letter of second syllable (Sweden = swd)
3 syllable country = first letter of each syllable (panama = pnm)
4+ syllables = first letter of the first three syllables(algeria = agr)

1 word = same rules as above
2 words = first 2 letters of first word + first letter of second word (American Samoa = ams)
3 words = first letter of each word (Bosnia and Herzegovina = bah)
4+ words = first letter of the first three words that aren't a connecting word (democratic republic of the congo = drc)

Connecting words would mess with the system so i removed them (of, and, the, etc)

## How the Code Works
main.py opens country_codes.json and loads all 240 countries and their existing data (dial code, ISO2, ISO3) into a dictionary.
For each country name, main.py calls make_code() from code_generator.py, passing the country name as a string.
code_generator.py calls split_words() from words.py to break the name into a list of words — splitting on spaces and hyphens. So "Democratic Republic of the Congo" becomes ["Democratic", "Republic", "of", "the", "Congo"].
code_generator.py counts the words and decides which word-count rule to apply:

1 word → passes it to the syllable rules
2 words → takes first 2 letters of word 1 + first letter of word 2
3 words → takes first letter of each word
4+ words → calls strip_connecting() from words.py to remove words like "of", "the", "and" until there are 3 content words left, then takes the first letter of each


If the name is one word, code_generator.py calls get_syllables() from definitions.py, which hands the word to pyphen and gets back a hyphenated string like "al-ge-ri-a", then splits it into a list like ["al", "ge", "ri", "a"].
code_generator.py counts the syllables and decides which syllable rule to apply,


A raw 3-letter code is returned back up to main.py and stored in raw_codes — a simple dictionary of {country_name: code}.
main.py passes raw_codes to resolve_collisions() in collision.py.
This loops through every code,
if a code hasn't been seen before it's kept as-is,
but if it's already been claimed by another country, the duplicate gets its last character replaced with a number (2, 3, 4...) until it finds a free slot.
main.py merges the new codes back into the original country data,
so each country entry now has its dial code, ISO2, ISO3, and new code all in one place.
main.py writes everything out to new_country_codes.json, and prints the full list of country names and their new codes to the console

i got the original list of codes in a html element from a website and put it into the codes file. i then made parser.py in order to convert from html to a more easily readable format
