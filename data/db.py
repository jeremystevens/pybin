import sqlite3
import os.path
from werkzeug.security import generate_password_hash, check_password_hash


def get_connection():
    # added to prevent error / http://shorturl.at/hyT02
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "paste.db")
    connection = sqlite3.connect(db_path)
    return connection
