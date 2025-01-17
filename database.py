import sqlite3
from queue import Queue

class DatabaseConfiguration:
    def __init__(self, database_url: str):
        self.database_url = database_url

    def validate(self):
        if not self.database_url:
            raise ValueError("Database URL cannot be empty.")

class DatabaseConnectionPool:
    def __init__(self, max_connections: int = 5):
        self.pool = Queue(max_connections)
        self.max_connections = max_connections

    def initialize_pool(self, database_url: str):
        for _ in range(self.max_connections):
            connection = sqlite3.connect(database_url)
            self.pool.put(connection)

    def get_connection(self):
        if self.pool.empty():
            raise ConnectionError("No available connections.")
        return self.pool.get()

    def return_connection(self, connection):
        self.pool.put(connection)

class QueryExecutor:
    @staticmethod
    def execute_query(connection, query: str, params=None):
        cursor = connection.cursor()
        try:
            cursor.execute(query, params or ())
            connection.commit()
            return cursor.fetchall()
        except sqlite3.OperationalError as e:
            if "already exists" in str(e):
                print(f"Warning: {e}")
            else:
                raise

class DatabaseFacade:
    def __init__(self):
        self.config = None
        self.pool = None

    def configure(self, database_url: str, max_connections: int = 5):
        self.config = DatabaseConfiguration(database_url)
        self.config.validate()
        self.pool = DatabaseConnectionPool(max_connections)
        self.pool.initialize_pool(database_url)

    def connect(self):
        if not self.pool:
            raise ConnectionError("Database not configured.")
        return self.pool.get_connection()

    def execute_query(self, query: str, params=None):
        connection = self.connect()
        try:
            result = QueryExecutor.execute_query(connection, query, params)
        finally:
            self.pool.return_connection(connection)
        return result
