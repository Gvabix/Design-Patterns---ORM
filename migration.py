class Migration:
    def __init__(self, db):
        self.db = db

    def apply(self, migration_sql):
        self.db.execute_query(migration_sql)
        self.db.execute_query("INSERT INTO migrations (name) VALUES (?)", (migration_sql,))

    def get_applied_migrations(self):
        return self.db.execute_query("SELECT name FROM migrations").fetchall()

    def create_migrations_table(self):
        self.db.execute_query("CREATE TABLE IF NOT EXISTS migrations (id INTEGER PRIMARY KEY, name TEXT)")

    def column_exists(self, table_name, column_name):
        query = f"PRAGMA table_info({table_name})"
        columns = self.db.execute_query(query)
        return any(column[1] == column_name for column in columns)

