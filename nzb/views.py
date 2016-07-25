import os
from flask import Blueprint, render_template, url_for, redirect, request, flash, current_app, jsonify
from werkzeug.utils import secure_filename

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
