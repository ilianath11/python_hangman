import random
import time
from hangman_create_and_populate_database import choose_random_word
from hangman_score_database import insert_data, get_highscore, display_highscore_info


DIFFICULTY_INDEX = {'easy': 1, 'hard': 2, 'impossible': 3}
MAX_TRIES = {'easy': 10, 'hard': 5, 'impossible': 1}


def display_word(hidden_word):
    """Display the hidden word with underscores for unknown letters."""
    return ' '.join(hidden_word).upper()


def update_hidden_word(word, hidden_word, guess):
    """
    Update the hidden word based on the user's guess.
    :param word:
    :param hidden_word:
    :param guess:
    """
    for i in range(len(word)):
        if word[i] == guess:
            hidden_word[i] = guess


def check_highscore(time_score):
    """
    Check if the user got a high score based on the elapsed time
    :param time_score:
    :return: True
    """
    current_highscore = get_highscore()

    if float(time_score) < float(current_highscore):
        print('Congrats, you got a high score!')
        return True


def display_hangman(tries):
    hangman_stages = [
        """
           --------
           |      |
           |      O
           |     \|/
           |      |
           |     / |
           ------
        """,
        """
           --------
           |      |
           |      O
           |     \|/
           |      |
           |     / 
           ------
        """,
        """
           --------
           |      |
           |      O
           |     \|/
           |      |
           |      
           ------
        """,
        """
           --------
           |      |
           |      O
           |     \|
           |      |
           |     
           ------
        """,
        """
           --------
           |      |
           |      O
           |      |
           |      |
           |     
           ------
        """,
        """
           --------
           |      |
           |      O
           |    
           |      
           |     
           ------
        """,
        """
           --------
           |      |
           |      
           |    
           |      
           |     
           ------
        """,
        """  
           --------
           |
           |
           |
           |
           |
           ------
        """,
        """  
           |
           |
           |
           |
           |
           ------
        """,
        """
           
           
                      
          ------
        """
    ]
    print(hangman_stages[tries])



def play_game(difficulty):
    """
    Method to start a new game
    :param difficulty: The level of difficulty that the user selected
    :return:
    """
    diff_index = DIFFICULTY_INDEX[difficulty]
    tries = MAX_TRIES[difficulty]
    guessed_letters = []

    # Choose a random word from the database, based on the level of difficulty
    random_word = choose_random_word(diff_index)
    hidden_word = ['_'] * len(random_word)
    playername = input('Enter your player name: ')
    start_time = time.time()

    while tries > 0:
        print(display_word(hidden_word))
        user_character = input('Enter a letter: ').lower()

        if not user_character.isalpha() or len(user_character) > 1:
            print('Error, please enter a valid letter')
        elif user_character in random_word:
            update_hidden_word(random_word, hidden_word, user_character)
            print(display_word(hidden_word))
            if '_' not in hidden_word:
                print('You won!')
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"player name: {playername}")
                print(f"Elapsed time: {elapsed_time}")
                if not check_highscore(elapsed_time):
                    h_input = input('Would you like to see the current high score? ').lower()
                    if h_input == 'yes':
                        display_highscore_info()
                    else:
                        pass

                return True, playername, elapsed_time
        else:
            tries -= 1
            guessed_letters.append(user_character.upper())
            display_hangman(tries)
            print(display_word(hidden_word))
            print("Guessed letters: ", guessed_letters)
            print(f'Wrong, try again. You have {tries} tries left')
            if tries == 0:
                print(f'You lost. The word was {random_word.upper()}')
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Elapsed time: {elapsed_time}")
                return False, playername, elapsed_time


def main():
    """
    Main function to run the word-guessing game.
    """
    user_diff_input = ''

    while user_diff_input.lower() != 'quit':
        user_diff_input = input('Select a difficulty level (easy, hard, or impossible): ')

        if user_diff_input.lower() in DIFFICULTY_INDEX:
            won, playername, elapsed_time = play_game(user_diff_input.lower())
            if won:
                insert_data(user_diff_input, elapsed_time, playername)
        elif user_diff_input.lower() != 'quit':
            print('Please enter a valid difficulty level')


if __name__ == "__main__":
    main()
