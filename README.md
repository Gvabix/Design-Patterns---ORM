# ORM Design Patterns Project

This project implements an ORM (Object-Relational Mapping) system using various design patterns in Python. The goal of this project is to provide a simplified interface for interacting with a database, utilizing design patterns like Facade, Strategy, and Factory.

## Project Structure

### 1. **database.py**

This file contains the logic for database configuration, connection pooling, and query execution. It implements the **Facade** design pattern to simplify database interactions.

#### Key Classes:
- **DatabaseConfiguration**: Manages and validates the database configuration.
- **DatabaseConnectionPool**: Handles the pooling of database connections to optimize performance.
- **QueryExecutor**: Executes SQL queries on the database.
- **DatabaseFacade**: Provides a simplified interface for interacting with the database. This is the main class for configuring, connecting, and executing queries.

#### Usage:
```python
from database import DatabaseFacade

# Initialize the database facade
db_facade = DatabaseFacade()

# Configure the database
db_facade.configure("example.db")

# Execute a query
db_facade.execute_query("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
```

### 2. **schema.py**
This file defines the structure for creating database tables and columns using the Factory design pattern.
#### Key Classes:
- **Column**: Represents a single database column with a name, type, and optional attributes (e.g., primary_key, not_null, default).
- **ColumnFactory**: A factory for creating columns of different types (e.g., INTEGER, VARCHAR).
- **Table**: Represents a database table and holds columns.
- **TableFactory**: A factory for creating tables with dynamically generated columns.

 #### Usage:
 ```python
from schema import Table, ColumnFactory

# Create a table with columns
user_table = Table("users")
user_table.add_column(ColumnFactory.create_integer_column("id", primary_key=True))
user_table.add_column(ColumnFactory.create_string_column("name", length=50))

# Print the table schema
print(str(user_table))
```
### 3. **crud.py**
This file implements the Strategy design pattern for CRUD operations (Create, Read, Update, Delete).
#### Key Classes:
- **CRUDOperation**: An abstract base class for CRUD operations.
- **CreateOperation**: Handles creating records in the database.
- **ReadOperation**: Handles reading records from the database.
- **UpdateOperation**: Handles updating records in the database.
- **DeleteOperation**: Handles deleting records from the database.
- **CRUDContext**: The context class that uses a strategy to perform the current CRUD operation.

#### Usage:
```python
from crud import CRUDContext, CreateOperation, ReadOperation

# Create a CRUD context with a CreateOperation strategy
crud = CRUDContext(CreateOperation())

# Execute a create operation
crud.execute(db_facade.connect(), {
    "table": "users",
    "fields": ["name"],
    "values": ["Alice"]
})

# Change strategy to ReadOperation
crud.set_strategy(ReadOperation())

# Execute a read operation
users = crud.execute(db_facade.connect(), {
    "table": "users",
    "fields": ["id", "name"],
    "condition": "age IS NULL"
})
print(users)
```

### **migration.py**
This file is responsible for managing database migrations. It ensures the database schema can evolve over time by adding or altering columns and tables.

#### Key Classes:
- **Migration**: Handles database schema migrations (e.g., adding columns or modifying tables).

#### Usage:
```python
from migration import Migration

# Initialize the migration object
migration = Migration(db_facade)

# Create the migrations table (if it doesn't exist)
migration.create_migrations_table()

# Apply a migration to add a new column
migration.apply("ALTER TABLE users ADD COLUMN age INTEGER")
```
