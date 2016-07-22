import os
import requests
from flask import Flask, render_template, url_for, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import History

@app.route('/')
def hello():
    return render_template('main_window/index.html')

if __name__ == '__main__':
    app.run()
