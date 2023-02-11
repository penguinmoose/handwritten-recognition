from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    file = FileField('Select an image file', validators=[DataRequired()])
    # white_background = BooleanField('Check if the background is white', default=False)
    submit = SubmitField('Upload!')


class ResultForm(FlaskForm):
    submit = SubmitField('Go back')