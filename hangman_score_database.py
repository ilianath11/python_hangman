import sqlite3

db_file_name = 'hangman_scores.db'


def get_connection():
    """
    Connects to the sqlite database of the game
    :return: Returns a connection to the SQLite database
    """
    return sqlite3.connect(db_file_name)


def create_database():
    """
    Creates the hangman scores database
    """
    conn = get_connection()

    conn.execute('''CREATE TABLE IF NOT EXISTS scores(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    difficulty TEXT NOT NULL,
    time REAL, 
    player_name TEXT UNIQUE NOT NULL )''')

    conn.commit()
    conn.close()


def insert_data(difficulty, time, player_name):
    """
    Inserts player name, elapsed time and selected difficulty
    in the score database after the player wins the game
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO scores(difficulty, time, player_name) VALUES (?, ?, ?)', (difficulty,
                                                                                          time, player_name))
    conn.commit()
    conn.close()


def get_highscore():
    """
    Finds the current high score from the database
    :return: high_score_str
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT time FROM scores")
    time_scores = cursor.fetchall()
    high_score = min(time_scores)
    high_score_str = str(high_score)[1:-2]

    conn.commit()
    conn.close()

    return high_score_str


def display_highscore_info():
    """
    Prints the player name, elapsed time and selected difficulty
    level of the user that holds the current high score
    :return:
    """
    conn = get_connection()
    cursor = conn.cursor()

    elapsed_time = get_highscore()

    cursor.execute(f"SELECT * FROM scores WHERE time= {elapsed_time}")
    row = cursor.fetchone()

    print("DIFFICULTY:", row[1], "|", "TIME:", row[2], "|", "PLAYER NAME:", row[3])

    conn.commit()
    conn.close()



if __name__ == '__main__':
    create_database()
