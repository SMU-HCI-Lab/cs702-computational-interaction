from flask import Flask

application = Flask(__name__)
application.debug = True

from app import views
