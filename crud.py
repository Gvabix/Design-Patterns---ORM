class CRUDOperation:
    def perform_operation(self, connection, data):
        raise NotImplementedError("This method should be overridden by subclasses.")

class CreateOperation(CRUDOperation):
    def perform_operation(self, connection, data):
        query = f"INSERT INTO {data['table']} ({', '.join(data['fields'])}) VALUES ({', '.join(['?' for _ in data['fields']])})"
        connection.execute(query, tuple(data['values']))

class ReadOperation(CRUDOperation):
    def perform_operation(self, connection, data):
        query = f"SELECT {', '.join(data['fields'])} FROM {data['table']} WHERE {data['condition']}"
        return connection.execute(query).fetchall()

class UpdateOperation(CRUDOperation):
    def perform_operation(self, connection, data):
        query = f"UPDATE {data['table']} SET {', '.join([f'{field}=?' for field in data['fields']])} WHERE {data['condition']}"
        connection.execute(query, tuple(data['values']))

class DeleteOperation(CRUDOperation):
    def perform_operation(self, connection, data):
        query = f"DELETE FROM {data['table']} WHERE {data['condition']}"
        connection.execute(query)

class CRUDContext:
    def __init__(self, strategy: CRUDOperation):
        self.strategy = strategy

    def set_strategy(self, strategy: CRUDOperation):
        self.strategy = strategy

    def execute(self, connection, data):
        return self.strategy.perform_operation(connection, data)
