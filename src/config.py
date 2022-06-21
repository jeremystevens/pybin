# /usr/bin/python

""" config.py: - Configuration for Admin Panel """

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
# ======================================================================

import os

''' General configuration'''

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///pybin.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SESSION_PERMANENT = False
SESSION_TYPE = 'filesystem'


# ============================================================
# Configuration for Admin Panel
# ============================================================
"""
 Site Administrators 
"""


# admins email address
admin_email = 'admin@youremail.com'

''' get a rapid api key for  sendgrid.com  add it below '''
rapid_apikey = 'fiosjef939t03gkr0gk4yh59940wowsfg00340435543'

''' Site Administrator Accounts 
 
    Add the site administrator accounts here.
    The format is:
    { Username : Password }
'''
admins = {'Admin1': {'password': '123'}, 'Admin2': {'password': '123'}}

