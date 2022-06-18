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
""" user_registration_views.py -  user registration system """
# ============================================================

''' Import modules '''

import flask
import flask_login
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, url_for, redirect, current_app, session, render_template, request, flash
from utils.prepare import convert_size, generate_random_id, exp_datetime, utf8len
import datetime
from datetime import datetime

# import the models for this view
from models.main import db
from models.users import Users
from models.profile import Profile

bp = Blueprint("user_registration_views", __name__, url_prefix="/")


@bp.route('/register', methods=['GET', 'POST'])
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