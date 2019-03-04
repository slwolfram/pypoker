import os
import datetime
from flask import Flask, jsonify
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pypoker.db'
db = SQLAlchemy(app)

from .apis.create_game import create_game
app.register_blueprint(create_game)
app.run()
            
            
            