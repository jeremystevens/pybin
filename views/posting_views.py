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
""" Posting.py - submitting post. views """
# ============================================================

from flask import Blueprint, url_for, redirect, current_app, session, render_template, request
from utils.prepare import convert_size, generate_random_id, exp_datetime, utf8len
import datetime
from datetime import datetime
from models.main import db
from models.posts import Post

bp = Blueprint("posting", __name__, url_prefix="/")

# Posting Route
# add methods to route or it will not work
@bp.route('/submit', methods=['GET', 'POST'])
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
        return redirect(url_for('posts.get_post', random_id=random_id))