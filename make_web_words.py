"""Writes docs/words5.txt, the 5-letter words with their frequency, for the web version.

One word per line: "word zipf" (words without a frequency have no number).
Run after make_word_frequencies.py.
"""
import json

with open("words_dictionary.json", "r") as file:
    words = json.load(file)
with open("word_frequencies.json", "r") as file:
    frequencies = json.load(file)

lines = []
for word in sorted(w for w in words if len(w) == 5 and w.isalpha()):
    zipf = frequencies.get(word)
    lines.append(f"{word} {zipf}" if zipf else word)

with open("docs/words5.txt", "w") as file:
    file.write("\n".join(lines))

print(f"{len(lines)} words written to docs/words5.txt")
