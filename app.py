import os
import requests
from flask import Flask, render_template, url_for, request
from flask.ext.sqlalchemy import SQLAlchemy
from settings import settings_page
from nzb import NZBParse

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(settings_page)
db = SQLAlchemy(app)

from models import History

@app.route('/')
def hello():
    print settings_page.root_path
    nzb_parse = NZBParse()
    print 'Parse NZB From File\n'
    nzb_parse.parseNZB(nzb_parse.readFromFile('static/theprojecthate.nzb'))
    print 'End Parse NZB From File\n'

#    print 'Parse NZB From URL\n'
#    try:
#	    nzb_parse.parseNZB(nzb_parse.readFromURL('http://localhost:5000/static/theprojecthate.nzb'))
#    except InputError:
#    	print 'Crap.'

    return render_template('main_window/index.html')

if __name__ == '__main__':
    app.run()
