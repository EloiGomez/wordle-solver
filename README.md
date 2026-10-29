# Wordle Solver

Interactive Python helper that narrows down the possible answers of a Wordle game from the feedback of each guess and suggests the next guess.

## How it works
1. Loads an English word list from `words_dictionary.json` and keeps the words of the length you choose.
2. You enter a guess (or let the program suggest one) and the feedback you got:
   - `g` green: the letter is in that exact position,
   - `y` yellow: the letter is in the word but not in that position,
   - `r` gray: the letter is not in the word (or there are no more copies of it).
3. `filter_words` keeps only the candidates that would have produced exactly that feedback (`get_feedback` reproduces Wordle's rules, including repeated letters).
4. The suggested guess is the one with the highest **expected information**: `entropy_of_guess` measures how evenly a guess splits the remaining candidates into feedback patterns, `H = -Σ p·log2(p)`, and `best_guess` picks the highest. For speed with large lists it tries a random sample of candidates as guesses and scores them against a random sample of possible answers.

When fewer than 100 candidates remain, they are printed.

## Run
```bash
python main_wordle_game_solver.py
```
No external packages are needed.

## Results
Average attempts on 5-letter words (500 simulated games, same secret words for both strategies, large word list with many rare words):

| Strategy | Average attempts | Solved in ≤ 6 |
|---|---|---|
| Random candidate | 5.00 | 88 % |
| Highest entropy | **4.46** | **95 %** |

## Notes
- The entropy-based guess selection and the repeated-letter fix in `get_feedback` were written with AI assistance (Claude Code); the original solver and the Discord bots are my own code.
- Ideas: use a smaller list of common Wordle words, evaluate all guesses instead of a sample, or choose guesses with a two-step lookahead.
