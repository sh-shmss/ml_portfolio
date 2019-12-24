from flask import Flask
from flask import render_template

app = Flask(__name__)
app.debug = True

@app.route('/')
@app.route('/ld')
def language_detector():
    return render_template ('ld.html', body = 'Language Detector')

@app.route('/about')
def about():
    return render_template ('about.html', body = 'About')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)


