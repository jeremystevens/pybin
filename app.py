# /usr/bin/python
# Copyright 2022 Jeremy Stevens <jeremiahstevens@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
__version__ = '2.0.0'  # current version

# ============================================================

""" app.py: - the main pybin flask server """
# ============================================================

"""Import modules required for the app."""
from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_simplemde import SimpleMDE
import datetime
import threading
from datetime import datetime
import os
import json
import string
import time
import math
import schedule
import time
from threading import Thread
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, jsonify, send_file, \
    Response
from flask import Flask, render_template, request, url_for, redirect, flash, session, send_file, Response, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.sql.expression import update
from sqlalchemy import and_, or_, not_
from sqlalchemy.sql import func
from jinja2 import Environment, PackageLoader, select_autoescape, environment
from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter
from flask_sqlalchemy import SQLAlchemy
import flask_login
import requests
from utils import crypto
from models.main import db
from models.posts import Post
from models.users import Users
from models.profile import Profile
from views import (main_views,
                   posting_views,
                   post_views,
                   view_all_views,
                   user_login_views, user_registration_views,
                   user_logout_views,
                   download_file_views,
                   raw_post_views
                   )

''''
  =====================================
            General Setup 
  =====================================
'''

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pybin.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_TYPE'] = 'filesystem'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)

# rows to show for Pagination
ROWS_PER_PAGE = 6

from sqlalchemy.pool import SingletonThreadPool
engine = create_engine('sqlite:///pybin.db',
                poolclass=SingletonThreadPool)


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    db.create_all()
    return app


login_manager = LoginManager(app)
crypto.bcrypt = Bcrypt(app)

# DB ORM
migrate = Migrate()
db.init_app(app)
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
    migrate.init_app(app, db, render_as_batch=True)
else:
    migrate.init_app(app, db)

''' Flask-login Manager '''


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    pass


@login_manager.request_loader
def request_loader(request):
    pass


@login_manager.unauthorized_handler
def unauthorized_handler():
    return '404'


''' SITE BLUEPRINTS '''

# blueprints
app.register_blueprint(main_views.bp)
# posting blueprints
app.register_blueprint(posting_views.bp)
# viewing a post by ID blueprints
app.register_blueprint(post_views.bp)
# view all post in archive blueprints
app.register_blueprint(view_all_views.bp)
# user login blueprints
app.register_blueprint(user_login_views.bp)
# user registration blueprints
app.register_blueprint(user_registration_views.bp)
# user logout blueprints
app.register_blueprint(user_logout_views.bp)
# download post as txt file blueprints
app.register_blueprint(download_file_views.bp)
# view raw post
app.register_blueprint(raw_post_views.bp)


''' ERROR HANDLERS '''


def page_not_found(e):
    return render_template("404.html"), 404


def internal_server_error(e):
    return render_template("500.html"), 500


#  Register Error Handlers
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)

''' Run Main App '''
if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=8080)
