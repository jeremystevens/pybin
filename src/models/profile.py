from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, DateTime, func
import datetime
from datetime import datetime
from models.main import db

# user profile
class Profile(db.Model):
    # location column
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    location = db.Column(db.String(80), unique=True, nullable=True)
    post_count = db.Column(db.String(80), unique=True, nullable=True)
    total_views = db.Column(db.String(80), unique=True, nullable=True)
    languages = db.Column(db.String(80), unique=True, nullable=True)
    # join date column
    join_date = db.Column(DateTime(timezone=True), server_default=func.now())
    # last login column
    last_login = db.Column(DateTime(timezone=True), onupdate=func.now())
