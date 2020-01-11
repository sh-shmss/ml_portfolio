from flask_wtf import FlaskForm
from wtforms import TextAreaField, TextField, SubmitField
from wtforms.validators import Required,NumberRange


class PredictionForm(FlaskForm):
    user_input = TextAreaField(validators=[Required()])
    submit = SubmitField('Predict')


class VisualizationForm(FlaskForm):
    user_input = TextField(validators=[Required()])
    user_input_no = TextField(validators=[Required(),NumberRange(min=1)])
    submit = SubmitField('Visualize')
