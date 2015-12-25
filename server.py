"""Tagony: Slack coding challenge"""

from flask import Flask, render_template, request, flash
from tagony import get_parsed_data, FetchDataException
import os

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

if 'SECRET_KEY' in os.environ:
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch')
def fetch():
    input_url = request.args.get('input_url')
    try:
        parsed_data = get_parsed_data(input_url)
        augmented_html = parsed_data.get_output()
        freqtionary = parsed_data.TagCounter.most_common()
    except FetchDataException as e:
        augmented_html = ""  # can also set this to e
        freqtionary = {}
        flash(str(e))

    return render_template('fetch.html', input_url=input_url,
                           augmented_html=augmented_html,
                           freqtionary=freqtionary)

if __name__ == "__main__":
        app.debug = True
        app.config['SECRET_KEY'] = os.urandom(16)
        app.run()

