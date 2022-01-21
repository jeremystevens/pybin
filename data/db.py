""" db.py: - some tools to handle data before it is inserted into the DB. """

__author__ = "Jeremy Stevens"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jeremy Stevens"
__status__ = "Development"

import sqlite3
import os.path
import rstr
import string
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# connection to the database
def get_connection():
    # added to prevent error / http://shorturl.at/hyT02
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "pybin.db")
    connection = sqlite3.connect(db_path)
    return connection


# generate a random ID for Url.
def generate_random_id(min_size, max_size):
    letters = string.ascii_uppercase
    lower_letters = string.ascii_lowercase
    numbers = string.digits
    random_string = rstr.rstr(lower_letters + letters + numbers, min_size, max_size)
    return random_string


# function to find the date when post will expire.
def exp_datetime(post_exp):
    # 0 = never, 1= 10 min, 2 = 1 hour, 3 = 1 day, 4= 1 month
    if post_exp == "0":
        # this was changed to fix issue #7 it has to be a date.
        exp_date = "0";
        return exp_date
    if post_exp == "1":
        exp_date = datetime.datetime.now() + datetime.timedelta(minutes=10)
        return exp_date
    if post_exp == "2":
        exp_date = datetime.datetime.now() + datetime.timedelta(hours=1)
        return exp_date
    if post_exp == "3":
        exp_date = datetime.datetime.now() + datetime.timedelta(days=1)
        return exp_date
    if post_exp == "4":
        exp_date = datetime.datetime.now() + datetime.timedelta(days=30)
        return exp_date


# gets the string size in bytes.
def utf8len(s):
    return len(s.encode('utf-8'))
