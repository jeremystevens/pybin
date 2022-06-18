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
""" Post.py -  view post by ID """
# ============================================================

from flask import Blueprint, url_for, redirect, current_app, session, render_template, request
from utils.prepare import convert_size, generate_random_id, exp_datetime, utf8len
import datetime
from datetime import datetime
from models.main import db
from models.posts import Post
from models.users import Users
from models.profile import Profile
from views.prune_post_views import prune_expired


bp = Blueprint("posts", __name__, url_prefix="/")

# View post by ID Route
@bp.route('/p/<random_id>')
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
    #update_hits(random_id)
    post_expire = post.query.filter_by(post_id=random_id).first().expiration
    if post_expire == "Never":
        exp_date = "Never"
    else:
        exp_date = datetime.strptime(post_expire, '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
    post_text = post.query.filter_by(post_id=random_id).first().post_text
    return render_template('view.html', post_id=post_id, poster=poster, post_title=post_title, post_syntax=post_syntax,
                           post_date=p_date, post_size=post_size, post_hits=post_hits, post_expire=exp_date,
                           post_text=post_text, username=user_name)