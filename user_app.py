import argparse
from psycopg2 import connect, OperationalError, errors
from psycopg2.errorcodes import UNIQUE_VIOLATION
from clcrypto import check_password
from models import User

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")

args = parser.parse_args()


def create_user(cursor, username, password):
    if len(password) < 8:
        print("Password is too short! It requires at least 8 characters!")
    else:
        try:
            user = User(username, password)
            user.save_to_db(cursor)
            print("User successfully created")
        except errors.lookup(UNIQUE_VIOLATION) as e:
            print(f"Username already exists in database: {e}")


def edit_user(cursor, username, password, new_pass):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print(f"There is no user: {username} in database")
    elif check_password(password, user.hashed_password):
        if len(new_pass) < 8:
            print("Password is too short! It requires at least 8 characters!")
        else:
            user.hashed_password = new_pass
            user.save_to_db(cursor)
            print("Password changed")
    else:
        print("Wrong password!")


def delete_user(cursor, username, password):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print(f"There is no user: {username} in database")
    elif check_password(password, user.hashed_password):
        user.delete(cursor)
        print(f"User {username} successfully deleted from database")
    else:
        print("Wrong password!")


def list_of_users(cursor):
    users = User.load_all_users(cursor)
    for user in users:
        print(user.username)


if __name__ == '__main__':
    try:
        cnx = connect(user="postgres", password="coderslab", host="localhost", database="workshop")
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password and args.edit and args.new_pass:
            edit_user(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        elif args.list:
            list_of_users(cursor)
        else:
            parser.print_help()
        cnx.close()
    except OperationalError as e:
        print(f"Connection Error: {e}")