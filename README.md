# Wordle Solver

Interactive Python helper that narrows down the possible answers of a Wordle game from the feedback of each guess and suggests the next guess.

## How it works
1. Loads an English word list from `words_dictionary.json` and keeps the words of the length you choose.
2. You enter a guess (or let the program suggest one) and the feedback you got:
   - `g` green: the letter is in that exact position,
   - `y` yellow: the letter is in the word but not in that position,
   - `r` gray: the letter is not in the word (or there are no more copies of it).
3. `filter_words` keeps only the candidates that would have produced exactly that feedback (`get_feedback` reproduces Wordle's rules, including repeated letters).
4. The suggested guess is the one with the highest **expected information**. `entropy_of_guess` measures how evenly a guess splits the remaining candidates into feedback patterns, `H = -Σ p·log2(p)`, and `best_guess` picks the highest.
5. Not all words are equally likely answers. `word_frequencies.json` stores how common each word is, and every candidate is weighted by `10 ** (0.5 · zipf frequency)`, so `house` counts far more than `aalii` when computing `p`. Without that file the solver treats all words equally.

When fewer than 100 candidates remain, they are printed. For speed, only the 200 most likely candidates are tried as guesses and scored against the 1,000 most likely answers.

## Try it online
**https://eloigomez.github.io/wordle-solver/** — a web version (JavaScript port of the solver, in `docs/`):
- **Help me solve:** type the guess you played, click the tiles to set the colours Wordle gave you, and get the next suggestion plus the most likely answers.
- **Watch it solve:** enter a secret word (or pick a random one) and watch the solver find it step by step.

## Run in the terminal
```bash
python main_wordle_game_solver.py
```
No external packages are needed. `make_word_frequencies.py` regenerates `word_frequencies.json` (it needs `pip install wordfreq`), and `make_web_words.py` regenerates the word list used by the web version.

## Results
Average attempts on 5-letter words (300 simulated games, same secret words for every strategy). The secret words are drawn from the 2,500 most frequent 5-letter words, similar to the common words Wordle uses:

| Strategy | Average attempts | Solved in ≤ 6 |
|---|---|---|
| Random candidate | 5.25 | 81 % |
| Highest entropy, all words equally likely | 4.56 | 91 % |
| Highest entropy, weighted by word frequency | **3.87** | **99 %** |

Other weight exponents (0.25 and 1.0) gave 3.78 and 3.80, so the result is not very sensitive to it. If the secret is a very rare word, the weighted solver does worse than the uniform one, because it assumes common words are more likely.

## Notes
- The entropy-based guess selection, the word-frequency weighting, the web version and the repeated-letter fix in `get_feedback` were written with AI assistance (Claude Code); the original terminal solver and the Discord bots are my own code.
- The JavaScript version gives the same first guess (`share`) and about 3.8 attempts on average in the same kind of simulation.
- Ideas: evaluate all guesses instead of a subset, combine entropy with the probability that the guess itself is the answer, or look two steps ahead.
