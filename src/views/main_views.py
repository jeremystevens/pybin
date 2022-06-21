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
""" main_views.py - Main Page views """
# ============================================================

from flask import Blueprint, url_for, redirect, current_app, session, render_template


bp = Blueprint("main", __name__, url_prefix="/")


@bp.route("/")
def index():
    # if session is set  get session id
    if 'user_name' in session:
        user_name = session['user_name']
    else:
        user_name = "Anonymous"
        # display username on page with link to profile
        return render_template('index.html', username=user_name)

    # display login button
    return render_template('index.html')
