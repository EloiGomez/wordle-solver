// Wordle solver core: same logic as main_wordle_game_solver.py, used by the web page.
// A candidate is { word, weight }, where weight is how likely the word is to be the answer.

const FREQ_EXPONENT = 0.5;

// Feedback that Wordle would give for `guess` if `secret` were the answer
// ('g' = green, 'y' = yellow, 'r' = gray), handling repeated letters as the real game does.
function getFeedback(guess, secret) {
  const feedback = Array(guess.length).fill('r');
  const remaining = secret.split('');

  // First pass: greens use up their letter
  for (let i = 0; i < guess.length; i++) {
    if (guess[i] === secret[i]) {
      feedback[i] = 'g';
      remaining[i] = null;
    }
  }

  // Second pass: a letter is yellow only while there are unmatched copies in the secret
  for (let i = 0; i < guess.length; i++) {
    if (feedback[i] === 'r') {
      const j = remaining.indexOf(guess[i]);
      if (j !== -1) {
        feedback[i] = 'y';
        remaining[j] = null;
      }
    }
  }

  return feedback.join('');
}

// Reads the word list: one word per line, optionally followed by its Zipf frequency.
function parseWords(text) {
  return text.split('\n').filter(Boolean).map(line => {
    const [word, zipf] = line.trim().split(' ');
    return { word, weight: Math.pow(10, FREQ_EXPONENT * (zipf ? parseFloat(zipf) : 0)) };
  });
}

// Keep only the candidates that would have produced exactly this feedback for this guess
function filterWords(candidates, guess, feedback) {
  return candidates.filter(c => getFeedback(guess, c.word) === feedback);
}

// Expected information (in bits) of a guess: how evenly it splits the candidates into feedback patterns.
// H = -sum(p * log2(p)), where p is the weighted share of candidates that give each pattern.
function entropyOfGuess(guess, targets) {
  const counts = new Map();
  let total = 0;
  for (const t of targets) {
    const pattern = getFeedback(guess, t.word);
    counts.set(pattern, (counts.get(pattern) || 0) + t.weight);
    total += t.weight;
  }
  let h = 0;
  for (const n of counts.values()) {
    const p = n / total;
    h -= p * Math.log2(p);
  }
  return h;
}

// The guess with the highest entropy. For speed, only the 200 most likely candidates are tried as guesses
// and scored against the 1,000 most likely answers.
function bestGuess(candidates, maxGuesses = 200, maxTargets = 1000) {
  const ranked = [...candidates].sort((a, b) => b.weight - a.weight);
  if (ranked.length <= 2) return { word: ranked[0].word, entropy: 0 };
  const targets = ranked.slice(0, maxTargets);
  let best = null;
  for (const g of ranked.slice(0, maxGuesses)) {
    const entropy = entropyOfGuess(g.word, targets);
    if (best === null || entropy > best.entropy) best = { word: g.word, entropy };
  }
  return best;
}

// Plays a whole game against a known secret and returns the steps taken
function solve(allCandidates, secret, firstGuess = null, maxAttempts = 10) {
  let candidates = allCandidates;
  const steps = [];
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const guess = attempt === 1 && firstGuess ? firstGuess : bestGuess(candidates).word;
    const feedback = getFeedback(guess, secret);
    candidates = filterWords(candidates, guess, feedback);
    steps.push({ guess, feedback, remaining: candidates.length });
    if (feedback === 'ggggg') break;
  }
  return steps;
}

const WordleSolver = { getFeedback, parseWords, filterWords, entropyOfGuess, bestGuess, solve };
if (typeof module !== 'undefined') module.exports = WordleSolver;
