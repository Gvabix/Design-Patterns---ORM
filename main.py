from database import DatabaseFacade
from decorators import table, ColumnFactory
from model import Record
from crud import CommandInvoker

db_facade = DatabaseFacade()
db_facade.configure("db3.db")
connection = db_facade.connect()
invoker = CommandInvoker()


@table("users")
class User(Record):
    @ColumnFactory.create_integer_column("id", primary_key=True)
    def id(self): pass

    @ColumnFactory.create_string_column("name", length=50, not_null=True)
    def name(self): pass

    @ColumnFactory.create_string_column("email", length=100, not_null=True)
    def email(self): pass


User.create_table_in_db(db_facade)

new_user = User(name="Ala", email="a@a.com")
new_user.save(connection, invoker)

new_user_2 = User(name="Ewa", email="w@w.com")
new_user_2.save(connection, invoker)

print("Select names:")
users = User.select("name", connection=connection, invoker=invoker).execute()
for user in users:
    print(str(user))

print("Select everything:")
users = User.select(connection=connection, invoker=invoker).execute()
for user in users:
    print(str(user))

new_user.email = "alice@gmail.com"
new_user.save(connection, invoker)

print("After changing Alice's email:")
users = User.select(connection=connection, invoker=invoker).execute()
for user in users:
    print(str(user))

new_user.delete(connection, invoker)

print("After deleting Alice ):")
users = User.select(connection=connection, invoker=invoker).execute()
for user in users:
    print(str(user))

