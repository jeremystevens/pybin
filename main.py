import json
import string
from datetime import datetime

from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from data.db import get_connection, generate_random_id

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nots0s3cr3t'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pybin.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# db model
class Post(db.Model):
    pid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post_id = db.Column(db.String(80), unique=True, nullable=False)
    post_syntax = db.Column(db.String(80), nullable=False)
    post_title = db.Column(db.String(200), nullable=False)
    post_text = db.Column(db.String(8000), nullable=False)
    expiration = db.Column(db.String(200), nullable=False)
    exposure = db.Column(db.Integer, nullable=False)
    post_date = db.Column(db.String(200), nullable=False)
    post_size = db.Column(db.String(800))
    post_hits = db.Column(db.String(8000))


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
        paste_exposure = request.form['exposure']
        paste_name = request.form['paste_title']
        print(paste_text)
        # generate random id 
        random_id = generate_random_id(6, 8)
        pid = Post(post_id=random_id)
        db.session.add(pid)
        post_syn = Post(post_syntax=paste_syntax)
        db.session.add(post_syn)
        post_title = Post(post_title=paste_name)
        db.session.add(post_title)
        post_txt = Post(post_text=paste_text)
        db.session.add(post_txt)
        expr = Post(expiration=paste_exp)
        db.session.add(expr)
        expo = Post(exposure=paste_exposure)
        db.session.add(expo)
        date = datetime.now()
        p_date = Post(post_date=date)
        db.session.add(p_date)
        # update to get size later
        size_bt = 0
        size = Post(post_size=size_bt)
        db.session.add(size)
        # set hits to zero
        hits_count = 0
        p_hits = Post(post_hits=hits_count)
        db.session.add(p_hits)
        db.session.commit()
        # Redirect after post is complete Needs Work
        # TODO fix this to redirect to view post page
        # return render_template("view.html",
        #       post_id=random_id)
        return redirect(url_for('/'))
    else:
        return redirect(url_for('index'))


@app.route('/view/<post_id>')
def get_post(post_id):
    post = Post()
    results = post.query.filter_by(post_id=post_id).first().post_title
    print(results)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
