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
import requests

""" Posting_views.py - submitting post to the database """
# ============================================================

from flask import Blueprint, url_for, redirect, current_app, session, render_template, request, flash
import datetime
from datetime import datetime
import sys, os
# import config from outside directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import admin_email, rapid_apikey

bp = Blueprint('report_post_views', __name__, url_prefix="")


# admin_email = "jeremiahstevens@gmail.com"
# rapid_apikey = 'c3be1c06c1msh4372be4e855de86p1e0430jsn8efd69e42245'
# report to site admin via email
@bp.route('/report/<random_id>')
def report_post(random_id):
    if request.method == 'GET':
        if random_id == None:
            flash("Error: No post ID was provided.")
            return redirect(url_for('index'))
        else:
            post_id = random_id
    # get
    # send grid email
    url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"

    payload = {
        "personalizations": [
            {
                "to": [{"email": admin_email}],
                "subject": "Reported Post"
            }
        ],
        "from": {"email": "pybinbot@gmail.com"},
        "content": [
            {
                "type": "text/plain",
                "value": random_id
            }
        ]
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": rapid_apikey,
        "X-RapidAPI-Host": "rapidprod-sendgrid-v1.p.rapidapi.com"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    # flash success message
    flash("Thank you for reporting this post. We will review it and take appropriate action.")
    # return to get_post page
    return redirect(url_for('posts.get_post', random_id=random_id))
