from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class CRUDCommand(Command):
    def __init__(self, connection, data):
        self.connection = connection
        self.data = data
        self.last_executed = None

    def commit(self):
        self.connection.commit()

class CreateCommand(CRUDCommand):
    def execute(self):
        query = f"INSERT INTO {self.data['table']} ({', '.join(self.data['fields'])}) VALUES ({', '.join(['?' for _ in self.data['fields']])})"
        cursor = self.connection.execute(query, tuple(self.data['values']))
        self.last_executed = cursor.lastrowid
        self.commit()
        return self.last_executed

    def undo(self):
        if self.last_executed:
            query = f"DELETE FROM {self.data['table']} WHERE id = ?"
            self.connection.execute(query, (self.last_executed,))
            self.commit()

class ReadCommand(CRUDCommand):
    def execute(self):
        query = f"SELECT {', '.join(self.data['fields'])} FROM {self.data['table']} WHERE {self.data['condition']}"
        return self.connection.execute(query).fetchall()

    def undo(self):
        # Read operations don't need to be undone
        pass

class UpdateCommand(CRUDCommand):
    def execute(self):
        # Store the old values before updating
        select_query = f"SELECT {', '.join(self.data['fields'])} FROM {self.data['table']} WHERE {self.data['condition']}"
        self.last_executed = self.connection.execute(select_query).fetchall()
        
        query = f"UPDATE {self.data['table']} SET {', '.join([f'{field}=?' for field in self.data['fields']])} WHERE {self.data['condition']}"
        self.connection.execute(query, tuple(self.data['values']))
        self.commit()
        return True

    def undo(self):
        if self.last_executed:
            fields_str = ', '.join([f'{field}=?' for field in self.data['fields']])
            query = f"UPDATE {self.data['table']} SET {fields_str} WHERE {self.data['condition']}"
            for old_values in self.last_executed:
                self.connection.execute(query, old_values)
            self.commit()

class DeleteCommand(CRUDCommand):
    def execute(self):
        # Store the deleted data for potential undo
        select_query = f"SELECT * FROM {self.data['table']} WHERE {self.data['condition']}"
        self.last_executed = self.connection.execute(select_query).fetchall()
        
        query = f"DELETE FROM {self.data['table']} WHERE {self.data['condition']}"
        self.connection.execute(query)
        self.commit()
        return True

    def undo(self):
        if self.last_executed:
            fields = [description[0] for description in self.connection.execute(f"SELECT * FROM {self.data['table']} LIMIT 0").description]
            placeholders = ', '.join(['?' for _ in fields])
            fields_str = ', '.join(fields)
            query = f"INSERT INTO {self.data['table']} ({fields_str}) VALUES ({placeholders})"
            for deleted_row in self.last_executed:
                self.connection.execute(query, deleted_row)
            self.commit()

class CommandInvoker:
    def __init__(self):
        self.command_history = []

    def execute_command(self, command):
        result = command.execute()
        self.command_history.append(command)
        return result

    def undo_last(self):
        if self.command_history:
            command = self.command_history.pop()
            command.undo()
