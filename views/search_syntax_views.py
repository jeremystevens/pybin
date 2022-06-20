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
""" search_snytax_views.py - search for post by syntax """
# ============================================================

from flask import Blueprint, url_for, redirect, current_app, session, render_template, request
from utils.prepare import convert_size, generate_random_id, exp_datetime, utf8len
import datetime
from datetime import datetime
from models.main import db
from models.posts import Post

ROWS_PER_PAGE = 6

bp = Blueprint("search_syntax_views", __name__, url_prefix="/")

# Search archive by syntax
@bp.route('/s/<syntax>')
def search_syntax(syntax):
    post = Post()
    query = syntax
    search = "%{}%".format(query)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.post_syntax.like(search)).paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('search.html', date=datetime.now(), posts=posts, query=query)