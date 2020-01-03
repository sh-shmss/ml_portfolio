from flask import Flask, request, jsonify, render_template, flash
from forms.forms  import PredictionForm
#from bokeh.embed import components
#from bokeh.plotting import figure
#import joblib



import json
from bokeh.embed import components

from flask import Flask, render_template, request
from jinja2 import Template

from bokeh.embed import json_item
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.sampledata.iris import flowers



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

def make_plot(x, y):
    p = figure(title = "Iris Morphology", sizing_mode="fixed", plot_width=400, plot_height=400)
    p.xaxis.axis_label = x
    p.yaxis.axis_label = y
    p.circle(flowers[x], flowers[y], color=colors, fill_alpha=0.2, size=10)
    return p

colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
colors = [colormap[x] for x in flowers['species']]
features=[("sepal_length", "sepal_width"), ("petal_length", "petal_width")]
options=[0,1]
@app.route('/dv', methods=['GET','POST'])
def data_visualization():
    form = PredictionForm()
    if form.user_input.data:
        current_option = form.user_input.data
    else:
        current_option = options[0]
    plot = make_plot(features[int(current_option)][0],features[int(current_option)][1])
    script, div = components(plot)
    return render_template("dv.html", form=form, script=script, div=div,
                options=options,  current_option=current_option)






if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
