import random
import sqlite3

DB_FILENAME = 'hangman.db'


def get_connection():
    """
    Connects to the sqlite database of the game
    :return: Returns a connection to the SQLite database
    """
    return sqlite3.connect(DB_FILENAME)


def create_database():
    conn = get_connection()
    # Create a table to store words for each difficulty level
    try:
        conn.execute('''CREATE TABLE words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            difficulty INTEGER NOT NULL,
            word TEXT NOT NULL UNIQUE
        );''')
        print("Table people created successfully")
    except sqlite3.OperationalError as a:
        print(f"WARNING: {a}")
    conn.commit()
    conn.close()


def insert_word(difficulty, a_word):
    """
    Insert a word into the database for a specific difficulty level.
    :param difficulty: The level of difficulty
    :param a_word: The word to add
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Insert the word into the database
        cursor.execute('INSERT INTO words(difficulty, word) VALUES (?, ?)', (difficulty, a_word))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Word '{a_word}' already exists for difficulty level '{difficulty}'")
    conn.close()


def get_words_by_difficulty(difficulty):
    """
    Retrieve all words for a specific difficulty level from the database
    :param difficulty: The level of difficulty
    :return: A list with all words for the specific difficulty level
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Retrieve all words for a specific difficulty level
    cursor.execute('SELECT word FROM words WHERE difficulty = ?', (difficulty,))
    words = cursor.fetchall()
    conn.close()
    # Return a list with only the word from the specific difficulty
    return [w[0] for w in words]


def choose_random_word(difficulty):
    """
    Choose a random word from the given difficulty level
    :param difficulty: The difficulty level
    :return: A random word from the database for the given difficulty level
    """
    return random.choice(get_words_by_difficulty(difficulty))


if __name__ == "__main__":
    create_database()

    easy_list = ['cat', 'dog', 'play', 'orange', 'green', 'night', 'number', 'plant', 'snow', 'python', ]
    hard_list = ['forecast', 'licence', 'dependent', 'prepare', 'addition', 'remember', 'overview', 'experience',
                 'practice', 'descent']
    impossible_list = ['hypothesis', 'decorative', 'hospitality', 'identification', 'constitutional', 'confrontation',
                       'prescription', 'civilization', 'constellation', 'extraterrestrial']

    # Insert words for different difficulty levels
    for word in easy_list:
        insert_word(1, word)
    for word in hard_list:
        insert_word(2, word)
    for word in impossible_list:
        insert_word(3, word)
