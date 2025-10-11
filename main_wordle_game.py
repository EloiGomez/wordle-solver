import tkinter as tk
from tkinter import messagebox
import json
import random

# Load the word list from the JSON file
with open("words_dictionary.json", "r") as file:
    WORD_LIST = list(json.load(file).keys())  # Extracting the words (keys) as a list

# Global variable for the secret word
secret_word = ""  # Initialize secret_word as an empty string


# Function to update the window width based on the length of the secret word
def update_window_width(word_length):
    new_width = 50 * word_length + 100  # Width based on word length
    center_window()  # Recenter the window after resizing
    root.geometry(f"{new_width + 5}x600")  # Keep the height fixed at 600


# Center the window on the screen
def center_window():
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate x and y coordinates for the window
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the position of the window
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")


# Game logic to check the guess and provide feedback
def check_guess():
    guess = entry.get().lower()

    # Validate the guess length
    if len(guess) != len(secret_word):
        messagebox.showerror("Error", f"Guess must be {len(secret_word)} letters long!")
        return

    # Validate if it's a word in the word list
    if guess not in WORD_LIST:
        messagebox.showerror("Error", "Word not in the word list!")
        return

    # Create the result row with color feedback
    result_row = []
    for i, letter in enumerate(guess):
        if letter == secret_word[i]:
            result_row.append(("green", letter))  # Correct letter and position
        elif letter in secret_word:
            result_row.append(("yellow", letter))  # Correct letter but wrong position
        else:
            result_row.append(("gray", letter))  # Wrong letter

    # Display the guess and feedback
    display_guess(result_row)

    # Check if the user won
    if guess == secret_word:
        messagebox.showinfo("Congratulations!", "You guessed the word!")
        root.quit()

    # Clear the entry box for the next guess
    entry.delete(0, tk.END)


# Display the guessed word with colored feedback
def display_guess(result_row):
    guess_frame = tk.Frame(scrollable_frame)  # Attach guess frame to the scrollable frame
    guess_frame.pack(pady=5)

    for color, letter in result_row:
        label = tk.Label(guess_frame, text=letter, width=4, height=2, bg=color, fg="white",
                         font=("Helvetica", 18, "bold"))
        label.pack(side="left", padx=2)

    # Update the scroll region
    canvas.update_idletasks()  # Ensure all tasks are complete before adjusting the scroll region
    canvas.config(scrollregion=canvas.bbox("all"))  # Update scrollregion to encompass the frame


# Function to set the word manually
def set_word():
    global secret_word
    chosen_word = word_entry.get().lower()

    if len(chosen_word) < 3 or chosen_word not in WORD_LIST:
        messagebox.showerror("Error", "Please enter a valid word from the word list!")
    else:
        secret_word = chosen_word
        update_window_width(len(secret_word))  # Update the window width
        start_game()


# Start the game with either a random word or user-selected word
def start_game():
    for widget in scrollable_frame.winfo_children():  # Clear only the scrollable frame
        widget.destroy()
    create_game_interface()


# Start a new game with a random word of a specific length
def new_game():
    global secret_word
    length = length_entry.get()  # Get the desired length from the user input

    if not length.isdigit() or int(length) <= 0:
        messagebox.showerror("Error", "Please enter a valid length (positive number)!")
        return

    length = int(length)
    update_window_width(length)

    # Filter the words by length
    filtered_words = [word for word in WORD_LIST if len(word) == length]

    if not filtered_words:
        messagebox.showerror("Error", f"No words found with length {length}. Try another length!")
        return

    # Choose a random word from the filtered list
    secret_word = random.choice(filtered_words).lower()
    update_window_width(len(secret_word))  # Update the window width
    start_game()


# Create a window to allow choosing a word manually
def choose_word():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()  # Clear the scrollable frame

    instruction_label = tk.Label(scrollable_frame, text="Enter a word for the game:", font=("Helvetica", 18))
    instruction_label.pack(pady=20)

    global word_entry
    word_entry = tk.Entry(scrollable_frame, font=("Helvetica", 18), width=10, justify="center")
    word_entry.pack(pady=10)

    submit_button = tk.Button(scrollable_frame, text="Set Word", font=("Helvetica", 14), command=set_word)
    submit_button.pack(pady=10)


# Create the main game interface
def create_game_interface():
    title_label = tk.Label(scrollable_frame, text="Wordle Game", font=("Helvetica", 24, "bold"))
    title_label.pack(pady=20)

    instructions_label = tk.Label(scrollable_frame, text=f"Guess the {len(secret_word)}-letter word!",
                                  font=("Helvetica", 16))
    instructions_label.pack(pady=10)

    global entry
    entry = tk.Entry(scrollable_frame, font=("Helvetica", 18), width=10, justify="center")
    entry.pack(pady=20)

    guess_button = tk.Button(scrollable_frame, text="Submit Guess", font=("Helvetica", 14), command=check_guess)
    guess_button.pack()

    reset_button = tk.Button(scrollable_frame, text="New Game (Random Word)", font=("Helvetica", 14), command=new_game)
    reset_button.pack(pady=10)

    choose_word_button = tk.Button(scrollable_frame, text="Set Custom Word", font=("Helvetica", 14),
                                   command=choose_word)
    choose_word_button.pack(pady=10)

    # Adding input field for word length
    length_label = tk.Label(scrollable_frame, text="Enter word length for random word:", font=("Helvetica", 14))
    length_label.pack(pady=5)

    global length_entry
    length_entry = tk.Entry(scrollable_frame, font=("Helvetica", 14), width=5, justify="center")
    length_entry.pack(pady=5)


# Set up the main application window
root = tk.Tk()
root.title("Wordle Game")
root.geometry("300x600")  # Initial size of the window

# Create a canvas for scrolling
canvas = tk.Canvas(root)
canvas.pack(side="left", fill="both", expand=True)

# Create a scrollbar and attach it to the canvas
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure the canvas to work with the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Frame to hold the game elements
scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")  # Anchor the frame to the top-left of the canvas

# Bind the frame resize to the canvas
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))  # Update scrollregion to encompass the frame


scrollable_frame.bind("<Configure>", on_frame_configure)


# Bind mouse wheel for scrolling
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# Add mouse wheel binding depending on the platform
root.bind_all("<MouseWheel>", on_mouse_wheel)  # For Windows
root.bind_all("<Button-4>", on_mouse_wheel)  # For Linux (Scroll Up)
root.bind_all("<Button-5>", on_mouse_wheel)  # For Linux (Scroll Down)

# Start the initial interface
create_game_interface()
root.update_idletasks()  # Update the window to set initial size properly
root.geometry("400x600")  # Set an initial size to avoid 0x0

# Center the window on the screen
center_window()

# Run the tkinter event loop
root.mainloop()
