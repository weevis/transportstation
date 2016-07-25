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

TORRENT = "torrent"
MAGNET = "magnet"
NZB = "nzb"

from models import History, WorkQueue, NZBFile

def allowed_file(filename):
    return '.' in filename and \
        filename.split('.',1)[1] in ALLOWED_EXTENSIONS

def get_extension(filename):
    return filename.split('.',1)[1]

@nzb_page.route('/nzb', methods=['GET', 'POST'])
def nzb():
    filelist = []
    fs = {}
    if request.method == 'POST':
        for k in request.files:
            files = request.files[k]
            if files and allowed_file(files.filename):
                end_file = secure_filename(files.filename)
                f = os.path.join(current_app.config['UPLOAD_FOLDER'], end_file)
                files.save(f)
                extension = get_extension(files.filename)
                if( extension == NZB ):
                    nzb_parser = NZBParse()
                    json_obj = nzb_parser.parseNZB(nzb_parser.readFromFile(f))
                    filelist.append(json_obj)
                    print "NZB Found"
                if( extension == TORRENT or extension == MAGNET):
                    print "Torrent Found"
        fs['files'] = filelist
        fs['success'] = True
        return jsonify(fs)


    else:
        flash('Method not allowed')
        return jsonify({'success': False})


class uploadNZBForm(Form):
    filename = FileField('nzb', validators=[FileAllowed(['nzb', 'torrent', 'magnet'], 'NZB Files Only!')])

class NZBParse:
    nzbfile = None

    def __init__(self):
        self.nzbfile = {}
			
    def readFromURL(self, url, timeout=None):
        try:
            if timeout:
                stream = urlopen(url, timeout)
            else:
                stream = urlopen(url)

            self.nzbfile['url'] = url

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

        self.nzbfile['filename'] = filename

        return output

    def process_nzb(self, filename):
        print "mooo"

    def insert_nzb(self, filename):
        print "moooo"

    def parseNZB(self, output):
        try:
            if output is None:
                raise InputError

            nzb_files = nzb_parser.parse(output)

            subjects = []
            dates = []
            posters = []
            groups = []
            segments = []
            for nzb_file in nzb_files:
#                print 'Subject: {} Date: {} Poster: {} Groups: {}\n'.format(nzb_file.subject, nzb_file.date, nzb_file.poster, nzb_file.groups)
                subjects.append(nzb_file.subject)
                dates.append("{}".format(nzb_file.date))
                posters.append(nzb_file.poster)
                groups.append(nzb_file.groups)
                for segment in nzb_file.segments:
                    tmpsegment = {}
                    tmpsegment['number'] = segment.number
                    tmpsegment['message_id'] = segment.message_id
                    tmpsegment['bytes'] = segment.bytes
                    segments.append(tmpsegment)
#                    print 'Segment: {} Message ID: {} Size: {}\n'.format(segment.number, segment.message_id, segment.bytes)

            self.nzbfile['subjects'] = subjects
            self.nzbfile['dates'] = dates
            self.nzbfile['posters'] = posters
            self.nzbfile['groups'] = groups
            self.nzbfile['segments'] = segments
            return self.nzbfile

        except URLError, TypeError:
            return jsonify({"success":False})
