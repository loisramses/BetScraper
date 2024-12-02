import sqlite3

conn = sqlite3.connect('bets.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sports(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
)
''')