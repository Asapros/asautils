from dataclasses import dataclass
from sqlite3 import connect
from types import SimpleNamespace

class Database:
    def __init__(self, path: str = ":memory:"):
        self.file = path
        self.connection = None
        self.cursor = None
        self.tables = {}

    def _require(connection: bool = False, cursor: bool = False):
        """Wrapper not allowing wrapped methods to be called when connection/cursor is not assigned"""
        def inner(func):
            def wrapper(self, *args, **kwargs):
                if (connection and self.connection is None) or (cursor and self.cursor is None):
                    raise ValueError("Connect to the database at the first place!")
                return func(self, *args, **kwargs)
            return wrapper
        return inner
    
    def connect(self):
        """Connecting to the database"""
        self.connection = connect(self.file)
        self.cursor = self.connection.cursor()

    @_require(connection=True)
    def disconnect(self):
        """Disconnecting from database"""
        self.connection.close()
        self.connection = None
        self.cursor = None

    @_require(connection=True)
    def commit(self):
        """Commit changes"""
        self.connection.commit()

    @_require(cursor=True)
    def create_table(self, name: str, model_class: dataclass, options = None):
        """Create a table"""
        template = """CREATE TABLE {}({})"""
        columns = ",".join([" ".join([varname, vartype]) for varname, vartype in zip(model_class.__annotations__.keys(), model_class.__annotations__.values())])
        content = columns if options is None else ",".join([columns, options])
        query = template.format(name, content)
        self.cursor.execute(query)
        self.tables[name] = model_class

    @_require(cursor=True)
    def insert(self, table: str, model: dataclass):
        """Insert a model to a table"""
        template = """INSERT INTO {} VALUES ({})"""
        query = template.format(table, ",".join(["?"]*len(model.__dataclass_fields__.keys())))
        values = [vars(model)[key] for key in model.__dataclass_fields__.keys()]
        return self.cursor.execute(query, values)

    @_require(cursor=True)
    def select(self, table: str, columns: list = ["*"], condition: str = None):
        """Fetch rows from a table. When there are too less columns to create a model, SimpleNamespace will be created instead"""
        model_class = self.tables.get(table, SimpleNamespace)
        template = """SELECT {} FROM {}{}"""
        query = template.format(",".join(columns), table, " WHERE {}".format(condition) if condition is not None else "")
        result = self.cursor.execute(query).fetchall()
        if columns == "*":
            template = """PRAGMA table_info("{}")"""
            query = template.format(table)
            columns = [column[1] for column in self.cursor.execute(query).fetchall()]

        models = []
        
        for row in result:
            kwargs = dict(zip(columns, row))
            try:
                model = model_class(**kwargs)
            except:
                model_class = SimpleNamespace
                model = model_class(**kwargs)
                
            models.append(model)

        return models

    @_require(cursor=True)
    def delete(self, table: str, condition: str = None):
        """Delete from a table"""
        template = """DELETE FROM {}{}"""
        query = template.format(table, " WHERE {}".format(condition) if condition is not None else "")
        self.cursor.execute(query)

    @_require(cursor=True)
    def update(self, table: str, values: dict, condition: str = None):
        """Changes values in the table."""
        template = """UPDATE {} SET {}{}"""
        update_values = ",".join(["{} = ?".format(key) for key in values.keys()])
        query = template.format(table, update_values, " WHERE {}".format(condition) if condition is not None else "")
        self.cursor.execute(query, list(values.values()))
