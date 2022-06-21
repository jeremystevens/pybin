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
""" profile_views.py -  views users profile """
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
# load hit updater
from utils.update_hits import update_hits


bp = Blueprint("profile_views", __name__, url_prefix="/")

""" user profile page """

# user profile page
@bp.route('/profile/<username>')
def profile(username):
    p_date = datetime.now()
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
        if user_last_login == "None":
            user_last_login =  "N/A"
        else:
            user_last_login = datetime.strptime(user_last_login, '%Y-%m-%d %H:%M:%f').strftime('%m/%d/%Y')
        # join_date
        user_join_date = profile.query.filter_by(username=username).first().join_date
        user_join_date = str(user_join_date)
        # convert to human readable
        user_join_date = datetime.strptime(user_join_date, '%Y-%m-%d %H:%M:%f').strftime('%m/%d/%Y')
        # format post Dates to human readable
        for i in range(len(post_date)):
            # if no post date, set to N/A
            if post_date[i][0] == 0:
                post_date[i][0] = "N/A"
            else:
                post_date[i] = datetime.strptime(post_date[i][0], '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
                p_date = post_date[i]
        return render_template('profile.html', user_name=user_name, username=username, user_location=user_location,
                               user_post_count=user_post_count, user_total_views=user_total_views,
                               posts=user_post, user_last_login=user_last_login, date=p_date,
                               user_join_date=user_join_date)
    except AttributeError:
        return render_template('404.html', date=datetime.now())
