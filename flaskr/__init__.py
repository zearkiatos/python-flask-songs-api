from flask import Flask
from config import Config

def create_app(config_name):
    config = Config()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = config.SECRET_KEY
    app.config['PROPAGATE_EXCEPTIONS']=True
    return app

from . import *