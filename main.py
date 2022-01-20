import datetime
import json
import string
from datetime import datetime
import jsonify
from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import update
from data.db import get_connection, generate_random_id, utf8len, exp_datetime

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


# update the hit counter
def update_hits(post_id):
    post_id
    post = Post()
    post_hits = post.query.filter_by(post_id=post_id).first().post_hits
    post_hits = int(post_hits) + 1
    rows_changed = post.query.filter_by(post_id=post_id).update(dict(post_hits=post_hits))
    db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')


# add methods to route or it will not work
@app.route('/submit', methods=['GET', 'POST'])
def submit_paste():
    if request.method == 'POST':
        paste_text = request.form['paste_text']
        paste_syntax = request.form['paste_syntax']
        paste_exp = request.form['paste_exp']
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
    exp_date = datetime.strptime(post_expire, '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
    post_text = post.query.filter_by(post_id=random_id).first().post_text
    return render_template('view.html', post_id=post_id, post_title=post_title, post_syntax=post_syntax,
                           post_date=p_date, post_size=post_size, post_hits=post_hits, post_expire=post_expire,
                           post_text=post_text)


if __name__ == '__main__':
    app.run(debug=True)
