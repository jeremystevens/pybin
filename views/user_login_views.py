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
__author__ = 'Jeremy Stevens'  # author

# ============================================================
""" user_login_views.py -  user Login system """
# ============================================================

''' Import modules '''
import flask
import flask_login
from werkzeug.security import check_password_hash
from flask import Blueprint, url_for, redirect, current_app, session, render_template, request
from utils.prepare import convert_size, generate_random_id, exp_datetime, utf8len
import datetime
from datetime import datetime

# import the models for this view
from models.main import db
from models.users import Users
from models.profile import Profile

bp = Blueprint("user_login_views", __name__, url_prefix="/")


@bp.route('/login', methods=['GET', 'POST'])
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
    return redirect(url_for('main.index'))
