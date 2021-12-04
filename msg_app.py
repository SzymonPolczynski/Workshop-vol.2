import argparse
from psycopg2 import connect, OperationalError
from clcrypto import check_password
from models import Messages, User

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters")
parser.add_argument("-t", "--to", help="recipient username")
parser.add_argument("-s", "--send", help="message text")
parser.add_argument("-l", "--list", help="list all messages", action="store_true")

args = parser.parse_args()


def list_of_messages(cursor, user):
    messages = Messages.load_all_messages(cursor, user.id)
    for message in messages:
        from_ = User.load_user_by_id(cursor, message.from_id)
        print(20 * "-")
        print(f"from: {from_.username}")
        print(f"data: {message.creation_date}")
        print(message.text)
        print(20 * "-")


def send_message(cursor, from_id, recipient_name, text):
    if len(text) > 255:
        print("Message too long! Max 255 char")
        return
    to_ = User.load_user_by_username(cursor, recipient_name)
    if to_:
        message = Messages(from_id, to_.id, text=text)
        message.save_to_db(cursor)
        print(f"Message send to {recipient_name}")
    else:
        print(f"There is no {recipient_name} in database")


if __name__ == '__main__':
    try:
        cnx = connect(user="postgres", password="coderslab", host="localhost", database="workshop")
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password:
            user = User.load_user_by_username(cursor, args.username)
            if check_password(args.password, user.hashed_password):
                if args.list:
                    list_of_messages(cursor, user)
                elif args.to and args.send:
                    send_message(cursor, user.id, args.to, args.send)
                else:
                    parser.print_help()
            else:
                print("Incorrect password or User does not exists!")
        else:
            print("username and password are required")
            parser.print_help()
        cnx.close()
    except OperationalError as e:
        print(f"Connection Error: {e}")
