"""Tagony: Slack coding challenge"""

from flask import Flask, render_template, request
from tagony import *

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True 


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fetch')
def fetch():
    input_url = request.args.get('input_url')
    parsed_data = get_parsed_data(input_url)

    augmented_html = parsed_data.get_output()
    freqtionary = parsed_data.TagCounter.most_common()

    return render_template('fetch.html', input_url=input_url,
                           augmented_html=augmented_html,
                           freqtionary=freqtionary)

if __name__ == "__main__":
        app.debug = True
        app.run()
