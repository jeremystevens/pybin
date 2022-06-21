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
import time

import flask
import flask_login

import config

""" admin_panel_views.py - Admin Panel views """
# ============================================================

from flask import Blueprint, url_for, redirect, current_app, session, render_template, request, flash
from utils.prepare import convert_size, generate_random_id, exp_datetime, utf8len
import datetime
from datetime import datetime
from models.main import db
from models.posts import Post
from flask_login import LoginManager , UserMixin , login_user , logout_user , current_user , login_required
import flask_login
import werkzeug
import os, signal

from config import admins

bp = Blueprint('admin_panel_views', __name__, url_prefix="")


@bp.route('/apanel')
# administrator login required to access this page
def protected():
    try:
        username = session['user_name']
    except KeyError as ke:
        flash("Unauthorized Access Attempt, your IP address has been logged", category='warning')
        return redirect(url_for('admin_login_views.login'))
    admin_check = tuple(admins.keys())
    if username in admin_check:
        return redirect(url_for('admin_login_views.login'))
    return render_template('adminpanel.html')


''' deprecated '''
#ef shutdown_server():
    #func = request.environ.get('werkzeug.server.shutdown')
    #if func is None:
        #raise RuntimeError('Not running with the Werkzeug Server')
    #func()

# Kill the server
def shutdown_server():
    os.kill(os.getpid(), signal.SIGINT)

# Shutdown the server after a request has been made
@bp.route('/shutdown', methods=['GET'])
def shutdown():
    try:
        username = session['user_name']
    except KeyError as ke:
        flash("Unauthorized Access Attempt, your IP address has been logged", category='warning')
        return redirect(url_for('admin_login_views.login'))
    admin_check = tuple(admins.keys())
    if username in admin_check:
        return redirect(url_for('admin_login_views.login'))
    for i in range(10, 0, -1):
        # flash message count down until shutdown
        flask.flash(str(i) + ' seconds until shutdown')
        time.sleep(1)
        print('Shutdown in ', i, ' seconds')
    shutdown_server()
    return render_template('adminpanel.html')


# Delete Reported Post.
@bp.route('/del_post', methods=['GET', 'POST'])
def delete_post():
    # first make sure they are authorized to access this page
    try:
        username = session['user_name']
    except KeyError as ke:
        flash("Unauthorized Access Attempt, your IP address has been logged", category='warning')
        return redirect(url_for('admin_login_views.login'))
    admin_check = tuple(admins.keys())
    if username in admin_check:
        return redirect(url_for('admin_login_views.login'))
    # if they are authorized, get the post id
    if request.method == "POST":
        post_id = request.form['post_id']
        # save post id to deleted.txt
        with open('deleted.log', 'a') as f:
            # get session id for user
            user_id = session['user_name']
            f.write(str(post_id) + ' Deleted by ' + 'Administrator' + '\n')
        db.session.query(Post).filter(Post.post_id == post_id).delete()
        db.session.commit()
        # flash message
        flask.flash('deleted: ' + post_id)
        return redirect(url_for('admin_panel_views.protected'))
    return 'Error Please Try Again'