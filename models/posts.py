from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from models.main import db

# Post DB Table
class Post(db.Model):
    pid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post_id = db.Column(db.String(80), unique=True, nullable=False)
    poster = db.Column(db.String(100), nullable=True)
    post_syntax = db.Column(db.String(80))
    post_title = db.Column(db.String(200))
    post_text = db.Column(db.String(8000))
    expiration = db.Column(db.String(200))
    exposure = db.Column(db.Integer)
    post_date = db.Column(db.String(200))
    post_size = db.Column(db.String(800))
    post_hits = db.Column(db.String(8000))