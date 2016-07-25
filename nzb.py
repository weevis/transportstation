from pynzb import nzb_parser
from urllib2 import urlopen, URLError
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
import os
from flask import Blueprint, render_template, url_for, redirect, request, flash, current_app, jsonify
from werkzeug.utils import secure_filename

from app import app,db

ALLOWED_EXTENSIONS = set(['nzb', 'torrent', 'magnet'])

nzb_page = Blueprint('nzb', __name__, url_prefix='/nzb')

ALLOWED_EXTENSIONS = set(['nzb', 'torrent', 'magnet'])

def allowed_file(filename):
    return '.' in filename and \
        filename.split('.',1)[1] in ALLOWED_EXTENSIONS

@nzb_page.route('/nzb', methods=['GET', 'POST'])
def nzb():
    if request.method == 'POST':
        for k in request.files:
            files = request.files[k]
            if files and allowed_file(files.filename):
                end_file = secure_filename(files.filename)
                f = os.path.join(current_app.config['UPLOAD_FOLDER'], end_file)
                files.save(f)
                return jsonify({'success': True})


    else:
        flash('No selected files')
        return jsonify({'success': False})


class uploadNZBForm(Form):
    filename = FileField('nzb', validators=[FileAllowed(['nzb', 'torrent', 'magnet'], 'NZB Files Only!')])

class NZBParse:
	nzbfile = None

	def __init__(self):
		self.nzbfile = None
			

	def readFromURL(self, url, timeout=None):
		try:
			if timeout:
				stream = urlopen(url, timeout)
			else:
				stream = urlopen(url)

			output = stream.read()
		except:
			output = None

		print 'Output from URL: {}'.format(output)
		return output

	def readFromFile(self, filename):
		try:
			contents = open(filename)
			output = contents.read()
		except:
			output = None

		return output

	def parseNZB(self, output):
		try:
			if output is None:
				raise InputError

			nzb_files = nzb_parser.parse(output)

			for nzb_file in nzb_files:
				print 'Subject: {} Date: {} Poster: {} Groups: {}\n'.format(nzb_file.subject, nzb_file.date, nzb_file.poster, nzb_file.groups)
				for segment in nzb_file.segments:
					print 'Segment: {} Message ID: {} Size: {}\n'.format(segment.number, segment.message_id, segment.bytes)

			return nzb_files

		except URLError, TypeError:
			print "Error!"
