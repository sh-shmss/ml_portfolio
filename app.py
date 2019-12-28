from flask import Flask, request, jsonify
from flask import render_template
#import joblib
from joblib import load

app = Flask(__name__)
app.debug = True

#ld_model = load('language_detection.pkl')
#sa_model = load('sentiment_analysis.pkl')

@app.route('/')
@app.route('/ld')
def language_detection():
    return render_template('ld.html', body='Language Detection')


@app.route("/predict_language", methods=['POST'])
def predict_language():
    data = request.get_json()
    text = data['text']
    result = loaded_model.predict([text])
    prediction = target_names[result[0]]
    return jsonify({'reponse': prediction})


@app.route('/sa')
def sentiment_analysis():
    return render_template('sa.html', body='Sentiment Analysis')


@app.route("/predict_sentiment", methods=['POST'])
def predict_sentiment():
    data = request.get_json()
    text = data['text']
    result = loaded_model.predict([text])
    prediction = target_names[result[0]]
    return jsonify({'reponse': prediction})


@app.route('/about')
def about():
    return render_template('about.html', body='About')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
