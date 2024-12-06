import sqlite3
from utils.maps import allowed_sports
from utils.my_types import BetTypes, OptionTypes

def get_connection(db_path: str):
    """Establishes a connection to the database."""
    return sqlite3.connect(db_path)

def close_connection(conn: sqlite3.Connection):
    """Closes a connection to the database."""
    conn.close()

def init_db(conn: sqlite3.Connection):
    cursor = conn.cursor()

    # BOOKMAKERS
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS bookmakers(
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     bookmaker_name TEXT UNIQUE NOT NULL
    # )
    # """)
        # bookmaker_id INTEGER NOT NULL,
        # FOREIGN KEY (bookmaker_id) REFERENCES bookmakers (id)

    # SPORTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
    """)
    
    # INSERT ALLOWED_SPORTS
    cursor.executemany("""
    INSERT INTO sports (name) 
    VALUES (?)
    ON CONFLICT (name) DO NOTHING;
    """, [(sport,) for sport in allowed_sports])

    # LEAGUES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leagues(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sport_id INTEGER NOT NULL,
        FOREIGN KEY (sport_id) REFERENCES sports (id)
    );
    """)

    # MATCHES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        participant1 TEXT NOT NULL,
        participant2 TEXT NOT NULL,
        url TEXT UNIQUE NOT NULL,
        league_id INTEGER NOT NULL,
        FOREIGN KEY (league_id) REFERENCES leagues (id)
    );
    """)

    # BET_TYPES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bet_types(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bet_type TEXT UNIQUE NOT NULL
    );
    """)

    # INSERT BET_TYPES
    cursor.executemany("""
    INSERT INTO bet_types (bet_type) 
    VALUES (?)
    ON CONFLICT (bet_type) DO NOTHING;
    """, [(bet_type.value,) for bet_type in BetTypes])

    # BETS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER NOT NULL,
        bet_type_id INTEGER NOT NULL,
        FOREIGN KEY (match_id) REFERENCES matches (id)
        FOREIGN KEY (bet_type_id) REFERENCES bet_types (id)
    );
    """)

    # OPTION_TYPES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS option_types(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        option_type TEXT UNIQUE NOT NULL
    );
    """)

    # INSERT OPTION_TYPES
    cursor.executemany("""
    INSERT INTO option_types (option_type) 
    VALUES (?)
    ON CONFLICT (option_type) DO NOTHING;
    """, [(option_type.value,) for option_type in OptionTypes])

    # OPTIONS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS options(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        arg FLOAT,
        odd FLOAT NOT NULL,
        option_type_id INTEGER NOT NULL,
        bet_id INTEGER NOT NULL,
        FOREIGN KEY (bet_id) REFERENCES bets (id)
        FOREIGN KEY (option_type_id) REFERENCES option_typeS (id)
    );
    """)
    
    # OPORTUNITIES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS oportunities(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_option_id INTEGER NOT NULL,
        second_option_id INTEGER NOT NULL,
        advantage FLOAT NOT NULL,
        FOREIGN KEY (first_option_id) REFERENCES options (id)
        FOREIGN KEY (second_option_id) REFERENCES options (id)
    );
    """)        
    conn.commit()

# def get_or_insert_bookmaker(cursor: sqlite3.Cursor, bookmaker: str):
#     cursor.execute("""
#     """)

def insert_league(cursor: sqlite3.Cursor, league_name: str, sport_id: int) -> int:
    cursor.execute("""
    INSERT INTO leagues (name, sport_id)
    VALUES (?, ?)
    RETURNING *;
    """, (league_name, sport_id))
    return cursor.fetchone()[0]

def insert_match(cursor: sqlite3.Cursor, match_name: str, participant1: str, participant2: str, url: str, league_id: int) -> int:
    cursor.execute("""
    INSERT INTO matches (name, participant1, participant2, url, league_id)
    VALUES (?, ?, ?, ?, ?)
    RETURNING *;
    """, (match_name, participant1, participant2, url, league_id))
    return cursor.fetchone()[0]

def insert_bet(cursor: sqlite3.Cursor, match_id: int, bet_type_id: int):
    cursor.execute("""
    INSERT INTO bets (match_id, bet_type_id)
    VALUES (?, ?)
    RETURNING *;
    """, (match_id, bet_type_id))
    return cursor.fetchone()[0]

def insert_option(cursor: sqlite3.Cursor, name: str, odd: float, option_type_id: int, bet_id: int, arg: float = None):
    cursor.execute("""
    INSERT INTO options (name, arg, odd, option_type_id, bet_id)
    VALUES (?, ?, ?, ?, ?)
    RETURNING *;
    """, (name, arg, odd, option_type_id, bet_id))
    return cursor.fetchone()[0]

def insert_oportunity(cursor: sqlite3.Cursor, second_option_id: int, first_option_id: int, advantage: int):
    cursor.execute("""
    INSERT INTO oportunities (second_option_id, first_option_id, advantage)
    VALUES (?, ?, ?)
    RETURNING *;
    """, (second_option_id, first_option_id, advantage))
    return cursor.fetchone()[0]

def get_sport(cursor: sqlite3.Cursor, sport_name: str) -> int:
    cursor.execute("""
    SELECT id FROM sports
    WHERE name = ?;
    """, (sport_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_option_type(cursor: sqlite3.Cursor, option_type: str) -> int:
    cursor.execute("""
    SELECT id FROM option_types
    WHERE option_type = ?;
    """, (option_type,))
    result = cursor.fetchone()
    return result[0] if result else None
