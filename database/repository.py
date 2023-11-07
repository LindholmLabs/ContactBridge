import os
import sqlite3


class DbRepository:
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(CURRENT_DIR, 'database.db')

    def __init__(self):
        self.connection = sqlite3.connect(self.DB_PATH, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.setup_database()

    def execute_query(self, query, parameters=(), expect_result=False):
        self.cursor.execute(query, parameters)

        if expect_result:
            return self.cursor.fetchall()
        else:
            self.connection.commit()

    def setup_database(self):
        with open(os.path.join(self.CURRENT_DIR, 'db.sql'), 'r') as sql_file:
            sql_script = sql_file.read()
        self.connection.executescript(sql_script)
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
