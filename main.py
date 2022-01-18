import json
import string
from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.security import check_password_hash

from data.db import get_connection, insert_paste

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nots0s3cr3t'


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
