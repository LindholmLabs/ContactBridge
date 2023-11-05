import math
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

    def get_all_messages(self):
        conn = sqlite3.connect(self.DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, relevance, message_content FROM messages ORDER BY timestamp DESC")
        messages = cursor.fetchall()
        conn.close()
        return messages

    def get_messages(self, page, page_size):
        conn = sqlite3.connect(self.DATABASE_FILE)
        cursor = conn.cursor()

        total_messages = cursor.execute('SELECT COUNT(*) FROM messages').fetchone()[0]
        offset = (page - 1) * page_size
        total_pages = math.ceil(total_messages / page_size)

        paginated_messages = cursor.execute(
            'SELECT id, email, relevance, message_content FROM messages ORDER BY timestamp DESC LIMIT ? OFFSET ?',
            (page_size, offset)
        ).fetchall()

        conn.close()
        return paginated_messages, total_pages
