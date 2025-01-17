class Column:
    def __init__(self, name, column_type, **kwargs):
        self.name = name
        self.column_type = column_type
        self.options = kwargs

    def __str__(self):
        # Handle specific options for SQL syntax
        options = []
        if self.options.get("primary_key"):
            options.append("PRIMARY KEY")
        if self.options.get("not_null"):
            options.append("NOT NULL")
        if "default" in self.options:
            options.append(f"DEFAULT {self.options['default']}")
        if "foreign_key" in self.options:
            options.append(f"FOREIGN KEY ({self.name}) REFERENCES {self.options['foreign_key']}")
        return f"{self.name} {self.column_type} {' '.join(options)}"

class ColumnFactory:
    @staticmethod
    def create_integer_column(name, primary_key=False):
        return Column(name, "INTEGER", primary_key=primary_key)

    @staticmethod
    def create_string_column(name, length):
        return Column(name, f"VARCHAR({length})")

class Table:
    def __init__(self, name):
        self.name = name
        self.columns = []

    def add_column(self, column: Column):
        self.columns.append(column)

    def __str__(self):
        columns_def = ", ".join(str(col) for col in self.columns)
        return f"CREATE TABLE IF NOT EXISTS {self.name} ({columns_def});"
