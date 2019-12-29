from flask import Flask, request, jsonify, render_template, flash
from forms.forms  import PredictionForm
#from bokeh.embed import components
#from bokeh.plotting import figure
#import joblib

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.debug = True

#ld_model = load('language_detection.pkl')
#sa_model = load('sentiment_analysis.pkl')

@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html', body='About')


@app.route('/ld', methods=['GET','POST'])
def language_detection():
    form = PredictionForm()
    prediction=""
    if form.user_input.data:
        prediction=form.user_input.data
    return render_template('ld.html', prediction=prediction, form=form)


@app.route('/sa', methods=['GET','POST'])
def sentiment_analysis():
    form = PredictionForm()
    prediction=""
    if form.user_input.data:
        prediction=form.user_input.data
    return render_template('sa.html', prediction=prediction, form=form)

@app.route('/dv', methods=['GET','POST'])
def data_visualization():
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]
#    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
