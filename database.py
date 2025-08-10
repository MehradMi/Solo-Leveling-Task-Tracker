import os
import sqlite3
import logging

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'dataset.db')

class Database():
    """Database class for initializing database instances"""
    def __init__(self):
        pass

    def init_database(self):
        """Initialize the database and create the tables if they don't already exist"""
        try:
            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cur = conn.cursor()

            # --- Table Creation: Users Table --- #
            cur.execute("""
                            CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            email TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                        """)
            conn.commit()
             
            # --- Table Creation: Characters Table --- #
            cur.execute("""
                            CREATE TABLE IF NOT EXISTS characters (
                            character_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            name TEXT NOT NULL,
                            class TEXT NOT NULL,
                            level INTEGER DEFAULT 1,
                            current_xp INTEGER DEFAULT 0,
                            xp_to_next_level INTEGER DEFAULT 100,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                            )
                        """)
            conn.commit()

            # --- Table Creation: Tasks Table --- #
            cur.execute("""
                            CREATE TABLE IF NOT EXISTS tasks (
                            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            character_id INTEGER NOT NULL,
                            title TEXT NOT NULL,
                            description TEXT,
                            difficulty TEXT CHECK(difficulty IN ('easy', 'medium', 'hard')),
                            xp_reward INTEGER NOT NULL,
                            status TEXT CHECK(status IN ('pending', 'completed')) DEFAULT 'pending',
                            start_time TIMESTAMP,
                            end_time TIMESTAMP,
                            FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
                            )
                        """)
            conn.commit()
            
            # --- Table Creation: Programs Table --- #
            cur.execute("""
                            CREATE TABLE IF NOT EXISTS programs (
                            program_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            executable_path TEXT,
                            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            last_seen TIMESTAMP
                            )
                        """)
            conn.commit()
            
            # --- Table Creation: Time Sessions Table --- #
            cur.execute("""
                            CREATE TABLE IF NOT EXISTS time_sessions (
                            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            program_id INTEGER NOT NULL,
                            character_id INTEGER NOT NULL,
                            start_time TIMESTAMP NOT NULL,
                            end_time TIMESTAMP,
                            duration_seconds INTEGER,
                            afk BOOLEAN DEFAULT 0,
                            FOREIGN KEY (program_id) REFERENCES programs(program_id) ON DELETE CASCADE,
                            FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
                            )
                        """)
            conn.commit()
            
            # --- Table Creation: Browser Tabs Table --- #
            cur.execute("""
                            CREATE TABLE IF NOT EXISTS browser_tabs (
                            tab_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            character_id INTEGER NOT NULL,
                            browser_name TEXT NOT NULL,
                            tab_title TEXT NOT NULL,
                            url TEXT,
                            start_time TIMESTAMP NOT NULL,
                            end_time TIMESTAMP,
                            duration_seconds INTEGER,
                            FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
                            )
                        """)
            conn.commit()
 
            # --- Table Creation: Achievements Table --- #
            cur.execute("""
                            CREATE TABLE IF NOT EXISTS achievements (
                            achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            character_id INTEGER NOT NULL,
                            title TEXT NOT NULL,
                            description TEXT,
                            xp_reward INTEGER NOT NULL,
                            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
                            )
                        """)
            conn.commit()
            
            # --- Table Creation: Leaderboard Table --- #
            cur.execute("""
                            CREATE TABLE IF NOT EXISTS leaderboard (
                            leaderboard_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            character_id INTEGER NOT NULL,
                            rank INTEGER NOT NULL,
                            level INTEGER NOT NULL,
                            xp INTEGER NOT NULL,
                            last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
                            )
                        """)
            conn.commit()

            conn.close()
            logger.info("Database Initialized Successfully!")

        except Exception as e:
            logger.error(f"Failed to initialize the database due to: {e}")
            raise