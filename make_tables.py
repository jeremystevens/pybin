from flask import Flask, render_template, request, url_for, redirect, flash, session, send_file, Response, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, Table
from sqlalchemy.sql.expression import update
from sqlalchemy import and_, or_, not_
from sqlalchemy.sql import func
import os


""" 
# ============================================================
                 MODELS AND DATABASE
# ============================================================
"""
db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pybin.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)


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


# user login db
class Users(db.Model):
    # username db
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)  # is active
    is_active = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)


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
