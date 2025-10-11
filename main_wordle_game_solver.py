import json
import random
from collections import Counter
from unidecode import unidecode

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

# Function to filter words based on feedback
def filter_words(possible_words, guess, feedback):
    green_letters = {}  # To track letters in green positions
    yellow_letters = {}  # To track yellow letters (appears, but in different positions)
    gray_letters = set()  # To track letters that should be excluded

    # Step 1: First pass to collect green and gray positions
    for i, (color, letter) in enumerate(zip(feedback, guess)):
        if color == 'g':  # Green, exact match required
            green_letters[i] = letter
        elif color == 'r':  # Gray, mark it for exclusion unless in a green/yellow position
            gray_letters.add(letter)

    # Step 2: Handle yellow letters (they appear in the word but not at their current position)
    for i, (color, letter) in enumerate(zip(feedback, guess)):
        if color == 'y':
            # Add to yellow but make sure it doesn't exist at the current position
            if letter not in yellow_letters:
                yellow_letters[letter] = []
            yellow_letters[letter].append(i)

    # Step 3: Filter words
    filtered_words = []
    for word in possible_words:
        # Check for green positions
        match = all(word[i] == letter for i, letter in green_letters.items())
        if not match:
            continue  # Word doesn't satisfy green letter positions

        # Check yellow letters (must be in word but not in the yellow-marked positions)
        for letter, positions in yellow_letters.items():
            if letter not in word:
                match = False
                break
            if any(word[pos] == letter for pos in positions):
                match = False
                break
        if not match:
            continue  # Word doesn't satisfy yellow letter conditions

        # Check for gray letters (letter must not be in the word unless it's green/yellow)
        if any(letter in word and letter not in green_letters.values() and letter not in yellow_letters for letter in gray_letters):
            continue  # Word contains gray letter, which it shouldn't

        # If all conditions are met, add word to the filtered list
        filtered_words.append(word)

    return filtered_words

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
                # Make a guess (randomly choosing from the possible words)
                guess = random.choice(possible_words)
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
                    # Make a guess (randomly choosing from the possible words)
                    guess = random.choice(possible_words)
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
                guess = random.choice(possible_words)
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
