from database import DatabaseFacade
from schema import Table, ColumnFactory
from migration import Migration
from crud import CRUDContext, CreateOperation, ReadOperation, UpdateOperation, DeleteOperation

# Inicjalizacja bazy danych
db_facade = DatabaseFacade()
db_facade.configure("example1.db")

# Tworzymy tabelę "users"
user_table = Table("users")
user_table.add_column(ColumnFactory.create_integer_column("id", primary_key=True))
user_table.add_column(ColumnFactory.create_string_column("name", length=50))
user_table.add_column(ColumnFactory.create_string_column("email", length=100))
db_facade.execute_query(str(user_table))  # Tworzymy tabelę

# Migracja - dodanie nowej kolumny
migration = Migration(db_facade)
migration.create_migrations_table()

# Sprawdzamy, czy kolumna 'age' już istnieje
if not migration.column_exists("users", "age"):
    migration.apply("ALTER TABLE users ADD COLUMN age INTEGER")  # Dodajemy kolumnę 'age'

# Operacje CRUD
crud = CRUDContext(CreateOperation())
crud.execute(db_facade.connect(), {
    "table": "users",
    "fields": ["name", "email"],
    "values": ["Alice", "alice@example.com"]
})

# Odczyt użytkowników
crud.set_strategy(ReadOperation())
users = crud.execute(db_facade.connect(), {
    "table": "users",
    "fields": ["id", "name", "email"],
    "condition": "age IS NULL"
})

print(users)  # Wypisujemy użytkowników

# Zakończenie
db_facade.pool.get_connection().close()
