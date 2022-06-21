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
""" view_all_views.py -  view all post in archive """
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


bp = Blueprint("view_all_views", __name__, url_prefix="/")

ROWS_PER_PAGE = 6
# view all public posts
@bp.route('/view/')
def view_all():
    # get session
    if 'user_name' in session:
        user_name = session['user_name']
    else:
        user_name = "Anonymous"
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