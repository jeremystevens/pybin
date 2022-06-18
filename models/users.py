from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from models.main import db


# user login db
class Users(db.Model):
    # username db
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)  # is active
    is_active = db.Column(db.Boolean, default=False)
