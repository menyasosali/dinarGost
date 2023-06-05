import sqlite3


def save_text_to_database(text):
    conn = sqlite3.connect("recognized_text.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS recognized_text (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)")
    c.execute("INSERT INTO recognized_text (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()
