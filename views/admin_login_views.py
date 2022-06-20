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
import flask
import flask_login

import config

""" admin_login_views.py - Admin Login Panel """
# ============================================================

from flask import Blueprint, url_for, redirect, current_app, session, render_template, request, flash
from utils.prepare import convert_size, generate_random_id, exp_datetime, utf8len
import datetime
from datetime import datetime
from models.main import db
from models.posts import Post
from config import admins

bp = Blueprint('admin_login_views', __name__, url_prefix='/')


#  Admin login Page
@bp.route('/admin', methods=['GET', 'POST'])
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
            user = config.admins[username]
            #user.is_active = True
            #user.id = username
            session['user_name'] = user
            # set is_active to True
            #user.is_active = True
            #flask_login.login_user(user)
            return flask.redirect(flask.url_for('admin_panel_views.protected'))
    except KeyError as ke:
        print('KeyError ', ke)
        flash('Incorrect username or password')
        return render_template('adminlogin.html')
    if 'user_name' in session:
        username = session['user_name']
        return redirect('/protected')
    # flash incorrect username or password
    flash('Incorrect username or password')
    return render_template('adminlogin.html')


