import os
import requests
from flask import Flask, render_template, url_for, request
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_wtf import Form

from app import app,db
from settings import settings_page
from nzb import NZBParse, nzb_page, uploadNZBForm

app.register_blueprint(settings_page)
app.register_blueprint(nzb_page)
db = SQLAlchemy(app)

from models import History, WorkQueue

@app.route('/')
def hello():
#    nzb_parse = NZBParse()
#    print 'Parse NZB From File\n'
#    nzb_parse.parseNZB(nzb_parse.readFromFile('static/theprojecthate.nzb'))
#    print 'End Parse NZB From File\n'

#    print 'Parse NZB From URL\n'
#    try:
#	    nzb_parse.parseNZB(nzb_parse.readFromURL('http://localhost:5000/static/theprojecthate.nzb'))
#    except InputError:
#    	print 'Crap.'
    form = uploadNZBForm()
    return render_template('main_window/index.html', uploadNZBForm=form)

if __name__ == '__main__':
    app.run()
