# Wordle Solver

Interactive Python helper that narrows down the possible answers of a Wordle game from the feedback of each guess.

## How it works
1. Loads an English word list from `words_dictionary.json` and keeps the words of the length you choose.
2. You enter a guess (or let the program pick a random candidate) and the feedback you got:
   - `g` green: the letter is in that exact position,
   - `y` yellow: the letter is in the word but not in that position,
   - `r` gray: the letter is not in the word (or there are no more copies of it).
3. `filter_words` keeps only the candidates that would have produced exactly that feedback (`get_feedback` reproduces Wordle's rules, including repeated letters), and the loop repeats (up to 10 attempts) until all letters are green.

When fewer than 100 candidates remain, they are printed.

## Run
```bash
python main_wordle_game_solver.py
```
No external packages are needed.

## Results
Picking each guess at random among the remaining candidates solves 5-letter words in **5.2 attempts on average** (300 simulated games, 82 % solved within 6 attempts, using the large word list in this repo, which includes many rare words).

## Ideas for improvement
- Pick the next guess by **expected information** (entropy of the feedback patterns over the remaining candidates) instead of at random, and compare the average number of attempts against the baseline above.
- Use a smaller list of common Wordle words.
