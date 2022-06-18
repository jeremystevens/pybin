""" prepare.py:  calculate data functions. """

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
__version__ = '2.0.0'

# ============================================================

import sqlite3
import os.path
import rstr
import string
import datetime
import math
from werkzeug.security import generate_password_hash, check_password_hash


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


# generate a random ID for Url.
def generate_random_id(min_size, max_size):
    letters = string.ascii_uppercase
    lower_letters = string.ascii_lowercase
    numbers = string.digits
    random_string = rstr.rstr(lower_letters + letters + numbers, min_size, max_size)
    return random_string


# function to find the date when post will expire.
def exp_datetime(post_exp):
    # 0 = never, 1= 10 min, 2 = 1 hour, 3 = 1 day, 4= 1 month
    if post_exp == "0":
        # this was changed to fix issue #7 it has to be a date.
        exp_date = "0";
        return exp_date
    if post_exp == "1":
        exp_date = datetime.datetime.now() + datetime.timedelta(minutes=10)
        return exp_date
    if post_exp == "2":
        exp_date = datetime.datetime.now() + datetime.timedelta(hours=1)
        return exp_date
    if post_exp == "3":
        exp_date = datetime.datetime.now() + datetime.timedelta(days=1)
        return exp_date
    if post_exp == "4":
        exp_date = datetime.datetime.now() + datetime.timedelta(days=30)
        return exp_date


# gets the string size in bytes.
def utf8len(s):
    return len(s.encode('utf-8'))
