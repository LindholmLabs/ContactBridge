import sqlite3

class DatabaseRepository:
    DATABASE_FILE = 'messages.db'

    def __init__(self):
        self.initialize_db()

    def initialize_db(self):
        conn = sqlite3.connect(self.DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message_content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                relevance NUMERIC
            );
            """
        )
        conn.commit()
        conn.close()

    def save_message(self, name, email, subject, message_content, relevance):
        conn = sqlite3.connect(self.DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO messages (name, email, subject, message_content, relevance)
            VALUES (?, ?, ?, ?, ?)
            """, (name, email, subject, message_content, relevance)
        )
        conn.commit()
        conn.close()

    def fetch_messages(self):
        conn = sqlite3.connect(self.DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages ORDER BY timestamp DESC")
        messages = cursor.fetchall()
        conn.close()
        return messages