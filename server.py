"""Tagony: Slack coding challenge"""

from flask import Flask, render_template, request, flash, get_flashed_messages
from tagony import get_parsed_data, FetchDataException


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = "8675309"


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
        flash(str(e))


    return render_template('fetch.html', input_url=input_url,
                           augmented_html=augmented_html,
                           freqtionary=freqtionary)

if __name__ == "__main__":
        app.debug = True
        app.run()
