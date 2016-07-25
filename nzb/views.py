import os
from flask import Blueprint, render_template, url_for, redirect, request, flash, current_app
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['nzb', 'torrent', 'magnet'])

nzb_page = Blueprint('nzb', __name__, url_prefix='/nzb')

ALLOWED_EXTENSIONS = set(['nzb', 'torrent', 'magnet'])

def allowed_file(filename):
	return '.' in filename and \
		filename.split('.',1)[1] in ALLOWED_EXTENSIONS

@nzb_page.route('/nzb', methods=['POST'])
def nzb():
	if request.method == 'POST':
		files = request.files.getlist("filename")
		if files:
			for file in files:
				end_file = secure_filename(file.filename)
				f = os.path.join(current_app.config['UPLOAD_FOLDER'], end_file)
				file.save(f)

			return redirect(url_for('hello'))
		else:
			flash('No selected files')
			return redirect(request.url)
#		if 'filename' not in request.files:
#	            flash('No file part')
#                    return redirect(request.url)
#		file = request.files['filename']
#
#		if file.filename == '':
#		    flash('No selected file')
#		    return redirect(request.url)
#
#		if file and allowed_file(file.filename):
#			end_file = secure_filename(file.filename)
#			f = os.path.join(current_app.config['UPLOAD_FOLDER'], end_file )
#			file.save(f)
#			return redirect(url_for('hello') )
	else:
		return redirect(request.url)
