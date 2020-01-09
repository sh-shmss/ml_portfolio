from flask_wtf import FlaskForm
from wtforms import TextAreaField, TextField, SubmitField
from wtforms.validators import Required


class PredictionForm(FlaskForm):
    user_input = TextAreaField()
    submit = SubmitField('Predict')


class VisualizationForm(FlaskForm):
    user_input = TextField()
    user_input_no = TextField()
    submit = SubmitField('Visualize')
