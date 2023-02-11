import os
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'stdv2grirb8hcouistyd'

from app import views