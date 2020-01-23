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
import os
from time import localtime, strftime
import psycopg2
from nltk.data import find
import gensim

secret_key = os.environ.get('SECRET_KEY')
db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
host = os.environ.get('HOST')
port = os.environ.get('PORT')
db = os.environ.get('DB')
table = os.environ.get('TABLE')


word2vec_sample = str(find('models/word2vec_sample/pruned.word2vec.txt'))
model = gensim.models.KeyedVectors.load_word2vec_format(
    word2vec_sample, binary=False)


def insert_db(component, user_input, user_input_no, prediction):
    ip = request.remote_addr
    timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime()) 
    connection = psycopg2.connect(user = db_username,
                                  password = db_password,
                                  host = host,
                                  port = port,
                                  database = db)

    cursor = connection.cursor()

    postgres_insert_query = f""" INSERT INTO {table}(component, user_input, user_input_no, prediction, timestamp, ip) VALUES (%s,%s,%s,%s,%s,%s)"""
    record_to_insert = (component, user_input, user_input_no, prediction, timestamp, ip)
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount

    cursor.close()
    connection.close()


app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.debug = True


@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html', body='About')


@app.route('/aa')
def academic_achievements():
    return render_template('aa.html', body='Academic Achievements')


@app.route('/ld', methods=['GET', 'POST'])
def language_detection():
    form = PredictionForm()
    prediction = ""
    if form.user_input.data:
        text = form.user_input.data
        prediction = Predict([text]).detect_language()
        insert_db("ld", text, str(0), str(prediction))
    return render_template('ld.html', prediction=prediction, form=form)


@app.route('/sa', methods=['GET', 'POST'])
def sentiment_analysis():
    form = PredictionForm()
    prediction = ""
    if form.user_input.data:
        text = form.user_input.data
        prediction = Predict(text).analyze_sentiment()
        insert_db("sa", text, str(0), str(prediction))
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
    insert_db("dv", str(current_word), str(current_no), "none")
    return render_template("dv.html", form=form, script=script, div=div)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)


