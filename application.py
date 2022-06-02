# /usr/bin/python

""" application.py: - the main pybin flask server """

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
__version__ = '1.1.3'

# ============================================================

import datetime
import threading
from datetime import datetime
import os
import json
import string
import time
import math

import flask
import schedule
import time
import logging
from threading import Thread
from flask import Flask, render_template, request, url_for, redirect, flash, session, send_file, Response, abort
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import update
from sqlalchemy import and_, or_, not_
from data.db import get_connection, generate_random_id, utf8len, exp_datetime, convert_size
from jinja2 import Environment, PackageLoader, select_autoescape, environment
from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter
import flask_login

# Local imports
from config import users

mod = Blueprint('post', __name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'nots0s3cr3t'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pybin.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
ROWS_PER_PAGE = 6


# db model
class Post(db.Model):
    pid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post_id = db.Column(db.String(80), unique=True, nullable=False)
    post_syntax = db.Column(db.String(80))
    post_title = db.Column(db.String(200))
    post_text = db.Column(db.String(8000))
    expiration = db.Column(db.String(200))
    exposure = db.Column(db.Integer)
    post_date = db.Column(db.String(200))
    post_size = db.Column(db.String(800))
    post_hits = db.Column(db.String(8000))


""" 
 Flask Login Manager
"""


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user


"""  LOGOUT """


@app.route('/logout')
def logout():
    session["user_name"] = None
    flask_login.logout_user()
    flask.flash('Logged out')
    session.clear()
    return redirect(url_for('login'))


#  Admin login Page
@app.route('/admin', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('adminlogin.html')
    username = flask.request.form['username']
    if not username.isupper():
        # capitalize first letter
        username = username.capitalize()
    else:
        username = username
    try:
        if flask.request.form['password'] == users[username]['password']:
            user = User()
            user.id = username
            session['user_name'] = username
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('protected'))
    except KeyError as ke:
        print('KeyError ', ke)
    if 'user_name' in session:
        username = session['user_name']
        return redirect('/protected')
    # flash incorrect username or password
    flash('Incorrect username or password')
    return render_template('adminlogin.html')


"""" ADMIN PANEL PAGE """


@app.route('/apanel')
@flask_login.login_required
def protected():
    flask.flash("")
    return render_template('adminpanel.html')


# Delete expired Post
def prune_expired():
    print("Pruning expired Post")
    post = Post()
    date_now = datetime.now()
    post_date = list(map(lambda x: x.expiration, post.query.all()))
    for p_date in post_date:
        if str(date_now) > str(p_date):
            post_id = post.query.filter_by(expiration=p_date).first().post_id
            # post date + post_id new line after
            date = str(datetime.now())
            del_post = "Deleted on: " + date + " " + post_id + "\n"
            with open('deleted.txt', 'a') as output:
                output.write(del_post)
            post.query.filter_by(expiration=p_date).delete()
            db.session.commit()
        else:
            # do nothing...
            pass


# update the hit counter
def update_hits(post_id):
    post = Post()
    post_hits = post.query.filter_by(post_id=post_id).first().post_hits
    post_hits = int(post_hits) + 1
    rows_changed = post.query.filter_by(post_id=post_id).update(dict(post_hits=post_hits))
    db.session.commit()


# Main index
@app.route('/')
def index():
    return render_template('index.html')


# API for pybin tools.
@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == "POST":
        paste_text = request.form['paste_text']
        paste_syntax = request.form['paste_syntax']
        paste_exp = request.form['paste_exp']
        print(paste_exp)
        # get a datetime when the post will expire
        # if paste_exp == 0 then use never expires
        if paste_exp == "0":
            expired_date = "Never"
            pass
        else:
            expired_date = exp_datetime(paste_exp)
        paste_exposure = request.form['exposure']
        paste_name = request.form['paste_title']
        # if name is blank name it untitled
        if paste_name == "":
            paste_name = "Untitled"
        else:
            paste_name = paste_name
        date = datetime.now()
        # generate random id
        # changed to only generate 7 Character ID
        random_id = generate_random_id(7, 7)
        # uses utf8lens fn to calculate string size in bytes.
        size_bt = utf8len(paste_text)
        hits_count = 0
        make_post = Post(post_id=random_id, post_syntax=paste_syntax, post_title=paste_name, post_text=paste_text,
                         expiration=expired_date, exposure=paste_exposure, post_date=date, post_size=size_bt,
                         post_hits=hits_count)
        db.session.add(make_post)
        db.session.commit()
        return random_id
    else:
        # if not data is posted show 404
        abort(404)


# Search archive by syntax
@app.route('/s/<syntax>')
def search_syntax(syntax):
    post = Post()
    query = syntax
    search = "%{}%".format(query)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.post_syntax.like(search)).paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('search.html', date=datetime.now(), posts=posts, query=query)


# Search Archive by name
@app.route("/search", methods=['GET', 'POST'])
def search_archive():
    if request.method == "POST":
        query = request.form['search']
        page = request.args.get('page', 1, type=int)
        search = "%{}%".format(query)
        post = Post()
        posts = Post.query.filter(Post.post_title.like(search)).paginate(page=page, per_page=ROWS_PER_PAGE)
        if posts == "":
            posts = "Nothing Found"
        # posts = post.query.filter(Post.post_title.like(search)).paginate(page=page,per_page=ROWS_PER_PAGE)
        return render_template('search.html', date=datetime.now(), posts=posts, query=query)


# Posting Route
# add methods to route or it will not work
@app.route('/submit', methods=['GET', 'POST'])
def submit_paste():
    if request.method == 'POST':
        paste_text = request.form['paste_text']
        paste_syntax = request.form['paste_syntax']
        paste_exp = request.form['paste_exp']
        print(paste_exp)
        # get a datetime when the post will expire
        # if paste_exp == 0 then use never expires
        if paste_exp == "0":
            expired_date = "Never"
            pass
        else:
            expired_date = exp_datetime(paste_exp)
        paste_exposure = request.form['exposure']
        paste_name = request.form['paste_title']
        # if name is blank name it untitled
        if paste_name == "":
            paste_name = "Untitled"
        else:
            paste_name = paste_name
        date = datetime.now()
        # generate random id
        # changed to only generate 7 Character ID
        random_id = generate_random_id(7, 7)
        # uses utf8lens fn to calculate string size in bytes.
        size_bt = utf8len(paste_text)
        hits_count = 0
        make_post = Post(post_id=random_id, post_syntax=paste_syntax, post_title=paste_name, post_text=paste_text,
                         expiration=expired_date, exposure=paste_exposure, post_date=date, post_size=size_bt,
                         post_hits=hits_count)
        db.session.add(make_post)
        db.session.commit()
        # needs the Function name not the app.route to work.
        # this fixed issue in #3
        return redirect(url_for('get_post', random_id=random_id))


# View Raw Code Route
@app.route('/raw/<random_id>')
def get_raw(random_id):
    post = Post()
    post_text = post.query.filter_by(post_id=random_id).first().post_text
    return render_template('raw.html', post_text=post_text)


# Download to file Route
@app.route('/download/<random_id>')
def download_file(random_id):
    post = Post()
    pwd = os.path.dirname(__file__)
    post_text = post_text = post.query.filter_by(post_id=random_id).first().post_text
    with open(random_id + '.txt', 'w') as output:
        output.write(post_text)
    path = pwd + "/" + random_id + ".txt"
    return send_file(path, as_attachment=True)


ROWS_PER_PAGE = 6


# view all public posts
@app.route('/view/')
def view_all():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get('page', 1, type=int)
    # remove expired post
    prune_expired()
    user = "none"
    post = Post()
    dates = post.query.with_entities(Post.post_date).all()
    # filer out unlisted post
    total_post = post.query.filter_by(exposure="public").paginate(page=page, per_page=ROWS_PER_PAGE)
    public_post = post.query.filter_by(exposure="public").all()

    return render_template('posts.html', date=datetime.now(), posts=total_post)
    # old code used below.
    # return render_template('posts.html', posts=post.query.all(), date=datetime.now())


# View post by ID Route
@app.route('/p/<random_id>')
def get_post(random_id):
    # remove expired post
    prune_expired()
    post = Post()
    post_id = post.query.filter_by(post_id=random_id).first().post_id
    post_title = post.query.filter_by(post_id=random_id).first().post_title
    post_syntax = post.query.filter_by(post_id=random_id).first().post_syntax
    post_date = post.query.filter_by(post_id=random_id).first().post_date
    # convert date to human Readable(works)
    p_date = datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
    post_size = post.query.filter_by(post_id=random_id).first().post_size
    # convert 1024 byes to KB
    post_size = convert_size(int(post_size))
    post_hits = post.query.filter_by(post_id=random_id).first().post_hits
    # this updates the view count.
    update_hits(random_id)
    post_expire = post.query.filter_by(post_id=random_id).first().expiration
    if post_expire == "Never":
        exp_date = "Never"
    else:
        exp_date = datetime.strptime(post_expire, '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
    post_text = post.query.filter_by(post_id=random_id).first().post_text
    return render_template('view.html', post_id=post_id, post_title=post_title, post_syntax=post_syntax,
                           post_date=p_date, post_size=post_size, post_hits=post_hits, post_expire=exp_date,
                           post_text=post_text)


# report abusive post.
@app.route('/report/<random_id>')
def report_post(random_id):
    pass


# route to handle 404
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_server_error():
    return render_template('500.html')
    pass


schedule.every(10).minutes.do(lambda: prune_expired())


def run_cronjob():
    # Infinity loop to run scheduler and prune expired post every 10 minutes
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    app.run(debug=True)
