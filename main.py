import json
import string
from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from data.db import get_connection, insert_paste

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
        # run the db function to enter data
        insert_paste(paste_text, paste_syntax, paste_exp, paste_exposure, paste_name)
        return redirect(url_for('index'))
    else:
        # TODO change this to redirect to post
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
