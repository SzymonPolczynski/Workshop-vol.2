from psycopg2 import connect, OperationalError, errors
from psycopg2.errorcodes import DUPLICATE_DATABASE, DUPLICATE_TABLE

CREATE_DB = "CREATE DATABASE workshop"
CREATE_TABLE_USERS = """
    CREATE TABLE Users (
    id serial,
    username varchar (255),
    hashed_password varchar (80),
    PRIMARY KEY(id)
    );
    """
CREATE_TABLE_MSG = """
    CREATE TABLE Messages (
    id serial,
    from_id int,
    to_id int,
    creation_date timestamp default Now(),
    text varchar (255),
    PRIMARY KEY(id),
    FOREIGN KEY(from_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY(to_id) REFERENCES Users(id) ON DELETE CASCADE
    );
    """
USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"


def create_db():
    """Function creating database
        Informs user if database already exists"""
    try:
        cnx = connect(user=USER, password=PASSWORD, host=HOST)
        cnx.autocommit = True
        cursor = cnx.cursor()

        try:
            cursor.execute(CREATE_DB)
            print("Database successfully created!")
        except errors.lookup(DUPLICATE_DATABASE) as e:
            print(f"Database already exists: {e}")

        cursor.close()
        cnx.close()
    except OperationalError as e:
        print(f"Connection error: {e}")


def create_table():
    """Function adding tables to database
        Informs user if table already exists in database"""
    try:
        cnx = connect(user=USER, password=PASSWORD, host=HOST, database="workshop")
        cnx.autocommit = True
        cursor = cnx.cursor()
        try:
            cursor.execute(CREATE_TABLE_USERS)
            print("Table 'users' successfully created!")
        except errors.lookup(DUPLICATE_TABLE) as e:
            print(f"Table already exists: {e}")

        try:
            cursor.execute(CREATE_TABLE_MSG)
            print("Table 'messages' successfully created")
        except errors.lookup(DUPLICATE_TABLE) as e:
            print(f"Table already exists: {e}")

        cursor.close()
        cnx.close()
    except OperationalError as e:
        print(f"Connection error: {e}")


create_db()
create_table()
