from crud import CreateCommand, ReadCommand, UpdateCommand, DeleteCommand
from crud import CommandInvoker
from database import DatabaseFacade
from schema import Table, ColumnFactory

# Example usage
db_facade = DatabaseFacade()
db_facade.configure("example.db")
connection = db_facade.connect()

# Create an invoker
invoker = CommandInvoker()

# Create the users table using Table and ColumnFactory
user_table = Table("users")
user_table.add_column(ColumnFactory.create_integer_column("id", primary_key=True))
user_table.add_column(ColumnFactory.create_string_column("name", length=50))
user_table.add_column(ColumnFactory.create_string_column("email", length=100))

# Create the table
connection.execute(str(user_table))
connection.commit()

# Create a new record
create_data = {
    "table": "users",
    "fields": ["name", "email"],
    "values": ["John Doe", "john@example.com"]
}
create_command = CreateCommand(connection, create_data)
new_id = invoker.execute_command(create_command)

# Read records
read_data = {
    "table": "users",
    "fields": ["id", "name", "email"],
    "condition": "id = " + str(new_id)
}
read_command = ReadCommand(connection, read_data)
results = invoker.execute_command(read_command)

print(results)

# Undo the last operation (if needed)
#invoker.undo_last()
