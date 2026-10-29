import json
import math
import random
from collections import Counter

WORD_LIST = []
# Load the word list from the JSON file
with open("words_dictionary.json", "r") as file:
    WORD_LIST = json.load(file)  # Load all words

spanish = True
#with open("Wordlist Spanish.txt", "r", encoding='utf-8') as file:
# with open("words.txt", "r", encoding='utf-8') as file:
#
#     for line in file:
#         word = line.strip()
#         WORD_LIST.append(unidecode(word))

# Feedback that Wordle would give for `guess` if `secret` were the answer
# ('g' = green, 'y' = yellow, 'r' = gray), with repeated letters handled as in the real game
def get_feedback(guess, secret):
    feedback = ['r'] * len(guess)
    remaining = list(secret)  # secret letters not yet matched

    # First pass: greens use up their letter
    for i, (g, s) in enumerate(zip(guess, secret)):
        if g == s:
            feedback[i] = 'g'
            remaining[i] = None

    # Second pass: a letter is yellow only while there are unmatched copies in the secret
    for i, g in enumerate(guess):
        if feedback[i] == 'r' and g in remaining:
            feedback[i] = 'y'
            remaining[remaining.index(g)] = None

    return ''.join(feedback)

# Keep only the words that would have produced exactly this feedback for this guess
def filter_words(possible_words, guess, feedback):
    return [word for word in possible_words if get_feedback(guess, word) == feedback]

# Expected information (in bits) of a guess: how evenly it splits the candidates into feedback patterns.
# H = -sum(p * log2(p)), where p is the share of candidates that would give each pattern.
def entropy_of_guess(guess, candidates):
    counts = Counter(get_feedback(guess, word) for word in candidates)
    total = len(candidates)
    return -sum((n / total) * math.log2(n / total) for n in counts.values())

# Choose the guess with the highest entropy. To keep it fast with large word lists, only a random sample
# of candidates is tried as guesses and scored against a random sample of possible answers.
def best_guess(candidates, max_guesses=200, max_targets=1000):
    if len(candidates) <= 2:
        return candidates[0]
    guesses = candidates if len(candidates) <= max_guesses else random.sample(candidates, max_guesses)
    targets = candidates if len(candidates) <= max_targets else random.sample(candidates, max_targets)
    return max(guesses, key=lambda g: entropy_of_guess(g, targets))

# Wordle Solver Function
def wordle_solver():
    # Ask the user for the desired word length
    word_length = input("Enter the length of the word to search (e.g., 5): ").strip()

    # Validate the word length input
    if not word_length.isdigit() or int(word_length) <= 0:
        print("Invalid word length. Please enter a positive integer.")
        return

    word_length = int(word_length)

    # Filter the word list based on the specified length
    if spanish: possible_words = [word for word in WORD_LIST if len(word) == word_length]
    else: possible_words = [word for word in WORD_LIST.keys() if len(word) == word_length]


    if not possible_words:
        print(f"No words found with length {word_length}.")
        return

    max_attempts = 10
    attempts = 0

    print("Welcome to the Wordle Solver!")
    print("Feedback colors: 'g' = green, 'y' = yellow, 'r' = gray.")

    while attempts < max_attempts:
        attempts += 1

        guess = None

        # Ask if the user wants to input their own guess or let the program choose
        while True:
            choice = input("Do you want to input your own guess? (yes/no): ").strip().lower()

            if choice == 'yes':
                guess = input(f"Enter your guess ({word_length} letters): ").strip().lower()
                # Validate the guess length
                if len(guess) != word_length or guess not in possible_words:
                    print(f"Invalid guess. Please enter a valid word of length {word_length} from the possible words.")
                    continue
                else:
                    break
            elif choice == 'no':
                # Make a guess (highest expected information among the possible words)
                guess = best_guess(possible_words)
                print(f"Attempt {attempts}: Guessing '{guess}'")
                break
            else:
                print("Invalid choice. Please type 'yes' or 'no'.")

        # Ask the user if they want to change their guess, and keep asking until they say "no"
        while True:
            if choice == 'yes': break
            change_guess = input("Do you want to change your guess? (yes/no): ").strip().lower()
            if change_guess == 'yes':
                # Ask if they want to input their own guess
                choice = input("Do you want to input your own guess? (yes/no): ").strip().lower()
                if choice == 'yes':
                    guess = input(f"Enter your guess ({word_length} letters): ").strip().lower()
                    # Validate the guess length
                    if len(guess) != word_length or guess not in possible_words:
                        print(f"Invalid guess. Please enter a valid word of length {word_length} from the possible words.")
                        continue
                    else:
                        print(f"Changing guess to: '{guess}'")
                        break
                elif choice == 'no':
                    # Make a guess (highest expected information among the possible words)
                    guess = best_guess(possible_words)
                    print(f"Attempt {attempts}: Guessing '{guess}'")
                    continue
                else:
                    print("Invalid choice. Please type 'yes' or 'no'.")
            elif change_guess == 'no':
                break
            else:
                print("Invalid choice. Please type 'yes' or 'no'.")

        # Input the feedback from the user
        feedback = input("Enter feedback (g/y/r for each letter, e.g., 'ggryy'): ").strip().lower()

        # Check for valid feedback length
        if len(feedback) != word_length or any(c not in 'gyr' for c in feedback):
            print(f"Invalid feedback. Please enter {word_length} letters using 'g' for green, 'y' for yellow, and 'r' for gray.")
            attempts -= 1  # Don't count this as an attempt
            continue

        # Filter possible words based on the feedback
        possible_words = filter_words(possible_words, guess, feedback)
        if len(possible_words) < 100:
            print("Possible words:", possible_words)

        # If the guess is correct
        if feedback == "g" * word_length:
            print("Found the secret word:", guess)
            break

        # If there are no possible words left, we cannot proceed
        if not possible_words:
            print("No possible words left. Choosing a new random word from the original list...")

            # Reset possible words and make a new guess
            possible_words = [word for word in WORD_LIST.keys() if len(word) == word_length]
            if possible_words:
                guess = best_guess(possible_words)
                print(f"New guess: '{guess}'")
                # Ask if the user wants to keep this new guess
                while True:
                    keep_guess = input("Do you want to keep this new guess? (yes/no): ").strip().lower()
                    if keep_guess == 'yes':
                        break
                    elif keep_guess == 'no':
                        guess = input(f"Enter your own guess ({word_length} letters): ").strip().lower()
                        # Validate the new guess
                        if len(guess) != word_length or guess not in possible_words:
                            print(f"Invalid guess. Please enter a valid word of length {word_length} from the possible words.")
                            attempts -= 1  # Don't count this as an attempt
                            continue
                        else:
                            break
                    else:
                        print("Invalid choice. Please type 'yes' or 'no'.")

                # Reset attempts to give another chance with the new guess
                attempts -= 1  # Don't count this as an attempt
            else:
                print("No more words available with that length.")
                break

    else:
        print("Failed to guess the word within the maximum attempts.")

# Example usage
if __name__ == "__main__":
    wordle_solver()
