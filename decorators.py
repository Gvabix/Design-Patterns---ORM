class ColumnFactory:
    @staticmethod
    def create_integer_column(name, primary_key=False, not_null=False, default=None):
        def decorator(func):
            func._column_name = name
            func._column_type = "INTEGER"
            func._primary_key = primary_key
            func._not_null = not_null
            func._default = default
            return func
        return decorator

    @staticmethod
    def create_string_column(name, length, not_null=False, default=None):
        def decorator(func):
            func._column_name = name
            func._column_type = f"VARCHAR({length})"
            func._primary_key = False
            func._not_null = not_null
            func._default = default
            return func
        return decorator


def table(name):
    def decorator(cls):
        cls._table_name = name
        cls._columns = {}

        for attr_name, attr in cls.__dict__.items():
            if hasattr(attr, "_column_name"):
                cls._columns[attr._column_name] = {
                    "type": attr._column_type,
                    "primary_key": getattr(attr, "_primary_key", False),
                    "not_null": getattr(attr, "_not_null", False),
                    "default": getattr(attr, "_default", None),
                }

        return cls
    return decorator
