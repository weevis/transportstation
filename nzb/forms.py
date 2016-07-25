from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed

class uploadNZBForm(Form):
	filename = FileField('nzb', validators=[FileAllowed('nzb', 'NZB Files Only!')])
