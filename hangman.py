import random

def hangman():
    # List of words for the game
    word_list = ["python", "hangman", "programming", "computer", "keyboard", "developer", "algorithm"]
    
    # Select a random word from the list
    secret_word = random.choice(word_list)
    
    # Initialize variables
    guessed_letters = []
    max_attempts = 6
    attempts_left = max_attempts
    word_completion = "_" * len(secret_word)
    
    print("Welcome to Hangman!")
    print(f"The word has {len(secret_word)} letters. You have {attempts_left} attempts to guess it.")
    print(word_completion)
    
    while attempts_left > 0 and "_" in word_completion:
        # Get user input
        guess = input("Guess a letter: ").lower()
        
        # Validate input
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
            continue
        
        # Check if letter was already guessed
        if guess in guessed_letters:
            print(f"You already guessed the letter '{guess}'. Try another one.")
            continue
        
        # Add the guess to the list of guessed letters
        guessed_letters.append(guess)
        
        # Check if the guess is in the secret word
        if guess in secret_word:
            print(f"Good guess! '{guess}' is in the word.")
            
            # Update the word completion
            new_completion = ""
            for i in range(len(secret_word)):
                if secret_word[i] == guess:
                    new_completion += guess
                else:
                    new_completion += word_completion[i]
            word_completion = new_completion
        else:
            attempts_left -= 1
            print(f"Sorry, '{guess}' is not in the word. You have {attempts_left} attempts left.")
        
        # Display current progress
        print(word_completion)
        print(f"Guessed letters: {', '.join(guessed_letters)}")
        
        # Draw hangman (optional visual)
        draw_hangman(max_attempts - attempts_left)
    
    # Game over message
    if "_" not in word_completion:
        print(f"Congratulations! You guessed the word '{secret_word}'!")
    else:
        print(f"Game over! The word was '{secret_word}'.")

def draw_hangman(wrong_attempts):
    """Optional visual representation of hangman"""
    stages = [
        """
           ------
           |    |
           |
           |
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |    |
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |   /|
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   /
           |
        --------
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           |
        --------
        """
    ]
    
    if wrong_attempts < len(stages):
        print(stages[wrong_attempts])

if __name__ == "__main__":
    hangman()
