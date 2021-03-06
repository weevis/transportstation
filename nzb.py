from pynzb import nzb_parser
from urllib2 import urlopen, URLError
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
import os
import time
import json
from flask import Blueprint, render_template, url_for, redirect, request, flash, current_app, jsonify
from werkzeug.utils import secure_filename
from sqlalchemy import func, Integer
from app import app,db

ALLOWED_EXTENSIONS = set(['nzb', 'torrent', 'magnet'])

nzb_page = Blueprint('nzb', __name__, url_prefix='/nzb')

ALLOWED_EXTENSIONS = set(['nzb', 'torrent', 'magnet'])

TORRENT = "torrent"
MAGNET = "magnet"
NZB = "nzb"

from models import History, WorkQueue, NZBFiles

def allowed_file(filename):
    return '.' in filename and \
        filename.split('.',1)[1] in ALLOWED_EXTENSIONS

def get_extension(filename):
    return filename.split('.',1)[1]

@nzb_page.route('/remove/<int:id>', methods=['GET', 'POST'])
def nzb_remove(id):
    to_remove = id

    files_subquery = db.session.query(func.json_array_elements(WorkQueue.field_data['files']).label('files')).subquery()
    query = db.session.query(WorkQueue.id, WorkQueue.field_data, files_subquery.c.files).filter(files_subquery.c.files.op('->>')('file_id').cast(Integer) == id)

    for q in query:
        print q[0]

    return jsonify({"success": True})

@nzb_page.route('/nzb', methods=['GET', 'POST'])
def nzb():
    filelist = []
    fs = {}
    if request.method == 'POST':
        i = 0
        for k in request.files:
	    i = i + 1
            files = request.files[k]
            if files and allowed_file(files.filename):
                end_file = secure_filename(files.filename)
                f = os.path.join(current_app.config['UPLOAD_FOLDER'], end_file)
                files.save(f)
                extension = get_extension(files.filename)
                if( extension == NZB ):
                    nzb_parser = NZBParse()
                    json_obj = nzb_parser.parseNZB(nzb_parser.readFromFile(f, end_file))
                    filelist.append(json_obj)
                if( extension == TORRENT or extension == MAGNET):
                    print "Torrent Found"
            else:
                    print "{} is not an allowed file".format(files.filename)

        fs['files'] = filelist
        fs['success'] = True
    	fs['numfiles'] = i
        jsondump = fs
        nzbfile = NZBFile()
        id = nzbfile.addToWorkQueue(jsondump)
        fs['id'] = id

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

    def readFromFile(self, filename, end_file):
        try:
            contents = open(filename)
            output = contents.read()
        except:
            output = None

        self.nzbfile['filename'] = filename
        self.nzbfile['basefilename'] = end_file
        self.nzbfile['finished'] = False
        self.nzbfile['added'] = time.time()
        nz = NZBFiles(self.nzbfile)
        db.session.add(nz)
        db.session.commit()
        self.nzbfile['file_id'] = nz.id
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

            sub_seg = []
            subjects = []
            segments2 = []
            i = 0
            totalBytes = 0
            for nzb_file in nzb_files:
                subjects.append(nzb_file.subject)
                for segment in nzb_file.segments:
                    i = i + 1
                    tmpsegment = {}
                    tmpsegment['number'] = segment.number
                    tmpsegment['message_id'] = segment.message_id
                    tmpsegment['bytes'] = segment.bytes
                    totalBytes = totalBytes + segment.bytes
                    segments2.append(tmpsegment)

                d = {}
                segs = list(segments2)
                d['subject'] = nzb_file.subject
                d['segments'] = segs
                d['dates'] = '{}'.format(nzb_file.date)
                d['posters'] = '{}'.format(nzb_file.poster)
                d['groups'] = '{}'.format(nzb_file.groups)
                sub_seg.append(d)
                del segments2[:]

            self.nzbfile['sub_seg'] = sub_seg
            self.nzbfile['numsegments'] = i
            self.nzbfile['totalbytes'] = totalBytes
            return self.nzbfile

        except URLError, TypeError:
            return jsonify({"success":False})

class NZBFile:
    nzb_json = None

    def __init__(self):
        self.nzb_json = None

    def addToWorkQueue(self, nzb_json):
        wq = WorkQueue(nzb_json)
        db.session.add(wq)
        db.session.commit()

        return wq.id
