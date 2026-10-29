"""Regenerates word_frequencies.json from words_dictionary.json.

Needs the wordfreq package (pip install wordfreq). The solver itself does not need it:
it only reads the JSON file this script produces.
"""
import json

from wordfreq import zipf_frequency

with open("words_dictionary.json", "r") as file:
    words = json.load(file)

frequencies = {}
for word in words:
    zipf = zipf_frequency(word, "en")  # log10 of occurrences per billion words
    if zipf > 0:
        frequencies[word] = round(zipf, 2)

with open("word_frequencies.json", "w") as file:
    json.dump(frequencies, file, separators=(",", ":"), sort_keys=True)

print(f"{len(frequencies)} of {len(words)} words have a frequency")
