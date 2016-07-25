from flask import Blueprint, render_template, abort, url_for
from jinja2 import TemplateNotFound

settings_page = Blueprint('settings', __name__)

@settings_page.route('/settings')
def admin_index():
	try:
		return render_template('settings/index.html')
	except TemplateNotFound:
		abort(404)
