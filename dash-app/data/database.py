# data/database.py

import psycopg2
from config.settings import DATABASE_CONFIG

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(**DATABASE_CONFIG)
            print("Connection to PostgreSQL successful")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def fetch_data(self, query, params=None):
        data = []
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                data = cursor.fetchall()
        except Exception as e:
            print(f"Error fetching data: {e}")
        return data

    def close(self):
        if self.connection:
            self.connection.close()
