from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required

class PredictionForm(FlaskForm):
    user_input = TextAreaField()
    submit = SubmitField('Predict')
