# ORM Design Patterns Project

This project implements a custom Object-Relational Mapping (ORM) system using Python. The ORM system allows you to interact with databases in an object-oriented way, making it easier to manipulate and query data without directly writing SQL queries. It employs three key design patterns to structure the codebase and simplify the development process: Factory, Command, and Decorator.

The core of the ORM system is built around the Record class, which serves as a base for model classes. These model classes represent database tables, and the Record class provides methods to handle database operations like creating, updating, deleting, and querying records.

## Design Patterns Use:

### 1. Factory Pattern
- Description:
The Factory Pattern is used to create objects without specifying the exact class of the object that will be created. It defines an interface for creating objects, but it is the subclasses or concrete classes that decide which object to instantiate.

- Usage in this project:
The ColumnFactory class is a factory that creates column definitions for the ORM model classes. The factory methods (create_integer_column, create_string_column, etc.) generate decorators that can be used to define columns with specific properties like type, primary key, nullability, etc.
  
### 2. Command Pattern
- Description:
The Command Pattern encapsulates a request as an object, thereby allowing users to parameterize clients with queues, requests, and operations. It separates the responsibility of issuing commands from the responsibility of executing them, allowing for operations to be undone or logged.

- Usage in this project:
The Command pattern is implemented in the CRUDCommand, CreateCommand, ReadCommand, UpdateCommand, and DeleteCommand classes. Each command represents a database operation, encapsulating it as an object that can be executed and undone. The CommandInvoker class is responsible for executing commands and managing their history for potential undo operations.
  
### 3. Facade Pattern
- Description:
The Facade Pattern provides a simplified interface to a complex subsystem. It defines a higher-level interface that makes the subsystem easier to use, by hiding the complexities of the subsystem from the user.

- Usage in this project:
The DatabaseFacade class serves as a facade for the database operations, providing a simplified interface for interacting with the database. It hides the complexity of managing connections, configurations, and query executions. The user only needs to call the configure, connect, and execute_query methods.
## Project Structure

### 1. **database.py**
This file contains the DatabaseFacade class, which provides a simple interface for connecting to and interacting with the database. It abstracts the complexity of establishing a database connection, executing queries, and managing transactions.
#### Key Classes:
- DatabaseConfiguration: This class manages the configuration of the database, specifically the database URL. It validates that the URL is not empty.
- DatabaseConnectionPool: Manages a pool of database connections, ensuring that connections are reused and that the system doesn't exceed a predefined number of simultaneous connections.
- QueryExecutor: Contains a static method for executing SQL queries on a database connection. It handles operational errors such as "already exists" warnings.
- DatabaseFacade: This is the main entry point for database operations. It combines the functionality of DatabaseConfiguration, DatabaseConnectionPool, and QueryExecutor to provide a high-level interface for configuring, connecting, and executing queries.


### 2. **decorators.py**
This file defines the structure for creating database tables and columns using the Factory design pattern.
#### Key Classes:
- ColumnFactory: A factory that creates column decorators for defining fields in ORM models. The methods allow for the creation of integer, string, float, boolean, and datetime columns, with properties like primary key, nullability, and default values.
- table: A decorator used to mark a class as a database table. It automatically extracts column definitions from the class and generates the corresponding SQL table schema.

### 3. **crud.py**
This file implements the Strategy design pattern for CRUD operations (Create, Read, Update, Delete).
#### Key Classes:
- Command: An abstract base class that defines the structure of all CRUD commands, including execute and undo methods.
- CRUDCommand: A concrete implementation of the Command class. It represents a generic CRUD operation and stores the data and connection required for execution.
- CreateCommand, ReadCommand, UpdateCommand, DeleteCommand: These are concrete implementations of the CRUDCommand class. Each class encapsulates a specific database operation (Create, Read, Update, Delete). They implement the execute and undo methods for each operation.
- CommandInvoker: This class manages the execution and undoing of commands. It maintains a history of executed commands and can undo the last operation.


### 4. **model.py**
- Record: This is the base class for ORM models. It contains methods for interacting with database records (e.g., save, delete, select) and is responsible for creating the corresponding SQL queries.
- User: This is an example of an ORM model class. It uses the @table decorator to define its associated table and the ColumnFactory to define its columns. The save method uses the CommandInvoker to execute the CreateCommand or UpdateCommand.

### 5. **test.ipynb*
This file demonstrates how to use the ORM to interact with the database. It shows how to create a User table, insert records, update records, select data, and delete records. It also shows how the CommandInvoker can be used to execute and undo CRUD operations
