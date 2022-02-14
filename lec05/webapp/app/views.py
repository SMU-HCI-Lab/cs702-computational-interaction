import json
from flask import render_template, request
from app import app
from usecase.cp.style_cp import StyleCP

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)



@app.route('/')
def home():
    return render_template('home.html')
