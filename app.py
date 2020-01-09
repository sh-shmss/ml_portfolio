from bokeh.sampledata.iris import flowers
from bokeh.resources import CDN
from bokeh.plotting import figure
from bokeh.embed import json_item
from jinja2 import Template
from flask import Flask, render_template, request
from bokeh.embed import components
import json
from flask import Flask, request, jsonify, render_template, flash
from forms.forms import PredictionForm, VisualizationForm
from graph.graph import PlotNetwork
from models.predictor import Predict
#from bokeh.embed import components
#from bokeh.plotting import figure

from nltk.data import find
import gensim
word2vec_sample = str(find('models/word2vec_sample/pruned.word2vec.txt'))
model = gensim.models.KeyedVectors.load_word2vec_format(
    word2vec_sample, binary=False)


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.debug = True


@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html', body='About')


@app.route('/ld', methods=['GET', 'POST'])
def language_detection():
    form = PredictionForm()
    prediction = ""
    if form.user_input.data:
        text = form.user_input.data
        prediction = Predict([text]).detect_language()
    return render_template('ld.html', prediction=prediction, form=form)


@app.route('/sa', methods=['GET', 'POST'])
def sentiment_analysis():
    form = PredictionForm()
    prediction = ""
    if form.user_input.data:
        text = form.user_input.data
        prediction = Predict(text).analyze_sentiment()
    return render_template('sa.html', prediction=prediction, form=form)


@app.route('/dv', methods=['GET', 'POST'])
def data_visualization():
    form = VisualizationForm()
    if form.user_input.data and form.user_input_no:
        current_word = form.user_input.data
        current_no = form.user_input_no.data
    else:
        current_word, current_no = 'data', 50
    plot = PlotNetwork(current_word, int(current_no), model).make_plot()
    script, div = components(plot)
    return render_template("dv.html", form=form, script=script, div=div)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
