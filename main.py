import json

from flask import Flask, render_template, request, url_for, redirect, flash, session
from werkzeug.security import check_password_hash

from data.db import get_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nots0s3cr3t'


@app.route('/')
def index():
    return render_template('index.html')
    pass


if __name__ == '__main__':
    app.run(debug=True)
