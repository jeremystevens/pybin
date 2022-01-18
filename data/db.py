import sqlite3
import os.path
import rstr
import string

from werkzeug.security import generate_password_hash, check_password_hash


# connection to the database
def get_connection():
    # added to prevent error / http://shorturl.at/hyT02
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "paste.db")
    connection = sqlite3.connect(db_path)
    return connection


# generate a random ID for Url.
def generate_random_id(min_size, max_size):
    letters = string.ascii_uppercase
    lower_letters = string.ascii_lowercase
    numbers = string.digits
    random_string = rstr.rstr(lower_letters + letters + numbers, min_size, max_size)
    return random_string


def insert_paste(paste_text, paste_syntax, paste_exp, paste_exposure, paste_name):
    random_id = generate_random_id(6, 8)
    # TODO Fix the Code below
    # ALL THE CODE BELOW DOES NOT WORK
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO public_post(
   postid,post_syntax,exp_int, post_exp,post_text, post_title) VALUES 
   (''', random_id, paste_syntax, paste_exp, paste_exposure, paste_name, paste_text, '),''')
    conn.commit()
