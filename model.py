from database import DatabaseFacade
from crud import CreateCommand, ReadCommand, UpdateCommand, DeleteCommand


class Record:
    _table_name = None
    _columns = {}

    def __init__(self, **kwargs):
        if self._table_name is None or not self._columns:
            raise ValueError("Model must have a table name and columns defined.")

        self._data = {}
        self._is_new = True
        for key, value in kwargs.items():
            if key not in self._columns:
                raise AttributeError(f"Invalid column '{key}' for table '{self._table_name}'")
            self._data[key] = value

        if "id" in self._data and self._data["id"] is not None:
            self._is_new = False

    @classmethod
    def create_table_sql(cls):
        if not cls._table_name:
            raise ValueError(f"Table name is not defined for class {cls.__name__}. Use @table decorator.")

        columns = []
        for name, options in cls._columns.items():
            column_def = f"{name} {options['type']}"
            if options.get("primary_key", False):
                column_def += " PRIMARY KEY"
            if options.get("not_null", False):
                column_def += " NOT NULL"
            if options.get("default") is not None:
                column_def += f" DEFAULT {options['default']}"
            columns.append(column_def)

        sql = f"CREATE TABLE IF NOT EXISTS {cls._table_name} ({', '.join(columns)});"
        return sql

    @classmethod
    def create_table_in_db(cls, db: DatabaseFacade):
        query = cls.create_table_sql()
        db.execute_query(query)

    def save(self, connection, invoker):

        if self._is_new:
            # CREATE
            data = {
                "table": self._table_name,
                "fields": [k for k in self._data.keys() if k != "id"],
                "values": [v for k, v in self._data.items() if k != "id"]
            }
            command = CreateCommand(connection, data)
            self._data["id"] = invoker.execute_command(command)
            self._is_new = False
        else:
            # UPDATE
            data = {
                "table": self._table_name,
                "fields": [k for k in self._data.keys() if k != "id"],
                "values": [v for k, v in self._data.items() if k != "id"],
                "condition": f"id = {self._data['id']}"
            }
            command = UpdateCommand(connection, data)
            invoker.execute_command(command)

    def delete(self, connection, invoker):
        """Usuwa rekord z bazy danych."""
        if "id" not in self._data or self._data["id"] is None:
            raise ValueError("Cannot delete a record without an ID.")

        data = {
            "table": self._table_name,
            "condition": f"id = {self._data['id']}"
        }
        command = DeleteCommand(connection, data)
        invoker.execute_command(command)

        self._data = None

    @classmethod
    def select(cls, *fields, connection, invoker):
        if not fields:
            fields = ["*"]
        return QueryBuilder(cls, fields, connection, invoker)


class QueryBuilder:
    def __init__(self, model_cls, fields, connection, invoker):
        self.model_cls = model_cls
        self.fields = fields
        self.conditions = []
        self.connection = connection
        self.invoker = invoker

    def where(self, condition):
        self.conditions.append(condition)
        return self

    def execute(self):
        if self.fields == ["*"]:
            self.fields = list(self.model_cls._columns.keys())

        condition = " AND ".join(self.conditions) if self.conditions else "1=1"
        data = {
            "table": self.model_cls._table_name,
            "fields": self.fields,
            "condition": condition,
        }

        command = ReadCommand(self.connection, data)
        results = self.invoker.execute_command(command)

        return [self.model_cls(**dict(zip(self.fields, row))) for row in results]