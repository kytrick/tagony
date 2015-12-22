"""Tagony: Slack coding challenge"""

import requests
from flask import Flask, render_template
from tagony import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("base.html")