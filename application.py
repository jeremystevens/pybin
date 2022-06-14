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
__version__ = '1.1.4'

# ============================================================
""" application.py: - the main pybin flask server """
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
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, Table
from sqlalchemy.sql.expression import update
from sqlalchemy import and_, or_, not_
from sqlalchemy.sql import func
from data.db import get_connection, generate_random_id, utf8len, exp_datetime, convert_size
from jinja2 import Environment, PackageLoader, select_autoescape, environment
from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter
import flask_login

# Local imports
from config import admins

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

""""

# ============================================================
                 MODELS AND DATABASE
# ============================================================
"""


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


"""
# ============================================================
                  Flask Login Manager
# ============================================================
"""


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in admins:
        return
    user = User()
    user.id = email
    return user


"""
# ============================================================ 
         LOGOUT 
# ============================================================
 """


@app.route('/logout')
def logout():
    session.clear()
    flask_login.logout_user()
    # destroy session
    flask.flash('Logged out')
    session.clear()
    return redirect(url_for('index'))


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
        if flask.request.form['password'] == admins[username]['password']:
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


"""
# ============================================================
            ADMIN PANEL PAGE 
# ============================================================
"""


@app.route('/apanel')
@flask_login.login_required
def protected():
    flask.flash("")
    return render_template('adminpanel.html')


"""
# ============================================================
         Admin Shutdown Server
# ============================================================
 """


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['GET'])
@flask_login.login_required
def shutdown():
    # count down to shutdown
    for i in range(10, 0, -1):
        time.sleep(1)
        # flash message count down until shutdown
        flask.flash(str(i) + ' seconds until shutdown')
        print('Shutdown in ', i, ' seconds')
    shutdown_server()
    return render_template('adminpanel.html')


"""
# ============================================================
            Admin Delete Post   
# ============================================================
"""


# Delete Reported Post.
@app.route('/del_post', methods=['GET', 'POST'])
@flask_login.login_required
def delete_post():
    if request.method == "POST":
        post_id = request.form['post_id']
        # save post id to deleted.txt
        with open('deleted.txt', 'a') as f:
            # get session id for user
            user_id = session['user_name']
            f.write(post_id + ' Deleted by ' + user_id + '\n')
        db.session.query(Post).filter(Post.post_id == post_id).delete()
        db.session.commit()
        # flash message
        flask.flash('deleted: ' + post_id)
        return redirect(url_for('protected'))
    return 'Error Please Try Again'


""" 
# ============================================================
            END OF ADMIN PANEL 
# ============================================================
"""

"""
# ============================================================
            USER Registration 
# ============================================================
"""


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form['username']
    password = request.form['password']
    # hash password
    password = generate_password_hash(password)
    email = request.form['email']
    # check if username is already in db
    if Users.query.filter_by(username=username).first():
        flask.flash('Username already exists')
        return render_template('register.html')
    # check if email is already in db
    if Users.query.filter_by(email=email).first():
        flask.flash('Email already exists')
        return render_template('register.html')
    # check if password is less than 8 characters
    if len(password) < 8:
        flash('Password must be at least 8 characters')
        return render_template('register.html')
    # commit to db
    db.session.add(Users(username=username, password=password, email=email))
    db.session.commit()
    db.session.close()
    # create user profile in db
    db.session.add(Profile(username=username))
    db.session.commit()
    db.session.close_all()
    # flash message
    flash('Successfully registered, you can now login')
    return render_template('register.html')


"""
# ============================================================
           User Login Page
# ============================================================
"""


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if flask.request.method == 'GET':
        return render_template('login.html')
    username = flask.request.form['username']
    password = flask.request.form['password']
    # check if username is in user db
    # check username and check_password_hash
    if not Users.query.filter_by(username=username).first():
        flask.flash('incorrect username')
        return render_template('login.html')
    # check if password is correct
    if not check_password_hash(Users.query.filter_by(username=username).first().password, password):
        flask.flash('incorrect password')
        return render_template('login.html')
    # create user object
    users = Users()
    users.id = username
    # set user to authenticated user
    # login user
    flask_login.login_user(users)
    # flash message
    flask.flash('Logged in')
    session['user_name'] = username
    current_user = users.id
    # update the last login column
    db.session.query(Profile).filter(Profile.username == username).update({"last_login": datetime.now()})
    db.session.commit()
    db.session.close_all()
    return redirect(url_for('index'))


"""

# ============================================================
          GENERAL SITE ROUTES 
# ============================================================
"""


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
    # if session is set  get session id
    if 'user_name' in session:
        user_name = session['user_name']
        # display username on page with link to profile
        return render_template('index.html', username=user_name)
    else:
        # display login button
        return render_template('index.html')


# API for pybin tools.
@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == "POST":
        paste_text = request.form['paste_text']
        # set poster to anonymous
        poster = "anonymous"
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
        make_post = Post(post_id=random_id, poster=poster, post_syntax=paste_syntax, post_title=paste_name,
                         post_text=paste_text,
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
    # get session
    if 'user_name' in session:
        user_name = session['user_name']
    if request.method == "POST":
        if 'user_name' in session:
            user_name = session['user_name']
        query = request.form['search']
        page = request.args.get('page', 1, type=int)
        search = "%{}%".format(query)
        post = Post()
        posts = Post.query.filter(Post.post_title.like(search)).paginate(page=page, per_page=ROWS_PER_PAGE)
        if posts == "":
            posts = "Nothing Found"
        # posts = post.query.filter(Post.post_title.like(search)).paginate(page=page,per_page=ROWS_PER_PAGE)
        return render_template('search.html', date=datetime.now(), posts=posts, query=query, username=user_name)


# Posting Route
# add methods to route or it will not work
@app.route('/submit', methods=['GET', 'POST'])
def submit_paste():
    if request.method == 'POST':
        paste_text = request.form['paste_text']
        # if session is set then use the session user name
        if 'user_name' in session:
            poster = session['user_name']
        else:
            poster = "Anonymous"
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
        make_post = Post(post_id=random_id, poster=poster, post_syntax=paste_syntax, post_title=paste_name,
                         post_text=paste_text,
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
    # get session
    if 'user_name' in session:
        user_name = session['user_name']
    else:
        user_name = None
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
    return render_template('posts.html', date=datetime.now(), posts=total_post, username=user_name)
    # old code used below.
    # return render_template('posts.html', posts=post.query.all(), date=datetime.now())


# View post by ID Route
@app.route('/p/<random_id>')
def get_post(random_id):
    # if session is set then use the session user name
    if 'user_name' in session:
        user_name = session['user_name']
    else:
        # clear the session
        session.clear()
        user_name = "Anonymous"
    # remove expired post
    prune_expired()
    post = Post()
    # added this to fix issue #45 - post not found
    # if post is not found then redirect to post not found page
    try:
        post_id = post.query.filter_by(post_id=random_id).first().post_id
    except AttributeError:
        return render_template('404.html', date=datetime.now())
    # if post id is not found then redirect to post not found page
    if post_id == None:
        return render_template('404.html', date=datetime.now())
    # if post id is found then get the post
    poster = post.query.filter_by(post_id=random_id).first().poster
    # if no session then poster name = anonymous
    if poster == "":
        poster = "Anonymous"
    else:
        poster = poster
    # if poster is not anonymous then update profile view count etc.
    if poster != "Anonymous":
        profile = Profile()
        total_views = profile.query.filter_by(username=poster).first().total_views
        if total_views == "":
            total_views = 0
        total_views = int(total_views) + 1
        profile.query.filter_by(username=poster).update(dict(total_views=total_views))
        db.session.commit()
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
    return render_template('view.html', post_id=post_id, poster=poster, post_title=post_title, post_syntax=post_syntax,
                           post_date=p_date, post_size=post_size, post_hits=post_hits, post_expire=exp_date,
                           post_text=post_text, username=user_name)


""" user profile page """

# user profile page
@app.route('/profile/<username>')
def profile(username):
    # get session
    if 'user_name' in session:
        user_name = session['user_name']
    else:
        user_name = "Anonymous"
    # get user profile
    users = Users()
    # get user post
    post = Post()
    profile = Profile()
    # added this to fix issue #47 - profile not found (prevent attribute error) added in V.1.1.6-bug-fix
    try:
        user_post = post.query.filter_by(poster=username).all()
        # get post dates
        post_date = post.query.with_entities(Post.post_date).all()
        # users location
        user_location = profile.query.filter_by(username=username).first().location
        if user_location == None:
            user_location = "N/A"
        else:
            user_location = user_location
        # users post count
        user_post_count = post.query.filter_by(poster=username).count()
        # total views of user
        user_total_views = profile.query.filter_by(username=username).first().total_views
        if user_total_views == None:
            user_total_views = 0
        else:
            user_total_views = user_total_views
        # post count by user
        user_post_count = post.query.filter_by(poster=username).count()
        if user_post_count == None:
            user_post_count = 0
        else:
            user_post_count = user_post_count
        # last login time
        user_last_login = profile.query.filter_by(username=username).first().last_login
        # convert to string format
        user_last_login = str(user_last_login)
        # convert to human readable
        user_last_login = datetime.strptime(user_last_login, '%Y-%m-%d %H:%M:%f').strftime('%m/%d/%Y')
        # join_date
        user_join_date = profile.query.filter_by(username=username).first().join_date
        user_join_date = str(user_join_date)
        # convert to human readable
        # convert to %m/%d/%Y
        user_join_date = datetime.strptime(user_join_date, '%Y-%m-%d %H:%M:%f').strftime('%m/%d/%Y')
        # format post Dates to human readable
        for i in range(len(post_date)):
            post_date[i] = datetime.strptime(post_date[i][0], '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
            # post_date[i] = datetime.strptime(post_date[i][0], '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
            p_date = post_date[i]
            # p_date = datetime.strptime(post_date[i], '%Y-%m-%d').strftime('%m/%d/%Y')
        # return user profile
        return render_template('profile.html', user_name=user_name, username=username, user_location=user_location,
                               user_post_count=user_post_count, user_total_views=user_total_views,
                               posts=user_post, user_last_login=user_last_login, date=p_date,
                               user_join_date=user_join_date)
    except AttributeError:
        return render_template('404.html', date=datetime.now())





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
