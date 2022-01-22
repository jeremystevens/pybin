""" main.py: the main python fIle"""

__author__ = "Jeremy Stevens"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jeremy Stevens"
__status__ = "Development"

import datetime
from datetime import datetime
import os
import json
import string
import time
from flask import Flask, render_template, request, url_for, redirect, flash, session, send_file
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import update
from data.db import get_connection, generate_random_id, utf8len, exp_datetime
from jinja2 import Environment, PackageLoader, select_autoescape, environment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nots0s3cr3t'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pybin.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# db model
class Post(db.Model):
    pid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post_id = db.Column(db.String(80), unique=True, nullable=False)
    post_syntax = db.Column(db.String(80))
    post_title = db.Column(db.String(200))
    post_text = db.Column(db.String(8000))
    expiration = db.Column(db.String(200))
    exposure = db.Column(db.Integer)
    post_date = db.Column(db.String(200))
    post_size = db.Column(db.String(800))
    post_hits = db.Column(db.String(8000))

    def __init__(self):
        self.pid = None
        self.post_id = None
        self.post_syntax = None
        self.post_title = None
        self.post_text = None
        self.expiration = None
        self.exposure = None
        self.post_date = None
        self.post_size = None


# update the hit counter
def update_hits(post_id):
    post = Post()
    post_hits = post.query.filter_by(post_id=post_id).first().post_hits
    post_hits = int(post_hits) + 1
    rows_changed = post.query.filter_by(post_id=post_id).update(dict(post_hits=post_hits))
    db.session.commit()


# Main index
@app.route('/')
def index():
    return render_template('index.html')


# Posting Route
# add methods to route or it will not work
@app.route('/submit', methods=['GET', 'POST'])
def submit_paste():
    if request.method == 'POST':
        paste_text = request.form['paste_text']
        paste_syntax = request.form['paste_syntax']
        paste_exp = request.form['paste_exp']
        print(paste_exp)
        # get a datetime when the post will expire
        expired_date = exp_datetime(paste_exp)
        paste_exposure = request.form['exposure']
        paste_name = request.form['paste_title']
        date = datetime.now()
        # generate random id
        random_id = generate_random_id(6, 8)
        # uses utf8lens fn to calculate string size in bytes.
        size_bt = utf8len(paste_text)
        hits_count = 0
        make_post = Post(post_id=random_id, post_syntax=paste_syntax, post_title=paste_name, post_text=paste_text,
                         expiration=expired_date, exposure=paste_exposure, post_date=date, post_size=size_bt,
                         post_hits=hits_count)
        db.session.add(make_post)
        db.session.commit()
        # needs the Function name not the app.route to work.
        # this fixed issue in #3
        return redirect(url_for('get_post', random_id=random_id))


# View Raw Code Route
@app.route('/raw/<random_id>')
def get_raw(random_id):
    post = Post()
    post_text = post.query.filter_by(post_id=random_id).first().post_text
    return render_template('raw.html', post_text=post_text)


# Download to file Route
@app.route('/download/<random_id>')
def download_file(random_id):
    post = Post()
    pwd = os.path.dirname(__file__)
    post_text = post_text = post.query.filter_by(post_id=random_id).first().post_text
    with open(random_id + '.txt', 'w') as output:
        output.write(post_text)
    path = pwd + "/" + random_id + ".txt"
    return send_file(path, as_attachment=True)


@app.route('/view/')
def view_all():
    post = Post()
    dates = post.query.with_entities(Post.post_date).all()
    return render_template('posts.html', posts=post.query.all(), date=datetime.now())


# View post by ID Route
@app.route('/p/<random_id>')
def get_post(random_id):
    post = Post()
    post_id = post.query.filter_by(post_id=random_id).first().post_id
    post_title = post.query.filter_by(post_id=random_id).first().post_title
    post_syntax = post.query.filter_by(post_id=random_id).first().post_syntax
    post_date = post.query.filter_by(post_id=random_id).first().post_date
    # convert date to human Readable(works)
    p_date = datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
    post_size = post.query.filter_by(post_id=random_id).first().post_size
    post_hits = post.query.filter_by(post_id=random_id).first().post_hits
    # this updates the view count.
    update_hits(random_id)
    post_expire = post.query.filter_by(post_id=random_id).first().expiration
    if post_expire == "0":
        exp_date = "Never"
    else:
        exp_date = datetime.strptime(post_expire, '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
    post_text = post.query.filter_by(post_id=random_id).first().post_text
    return render_template('view.html', post_id=post_id, post_title=post_title, post_syntax=post_syntax,
                           post_date=p_date, post_size=post_size, post_hits=post_hits, post_expire=exp_date,
                           post_text=post_text)


if __name__ == '__main__':
    app.run(debug=True)
