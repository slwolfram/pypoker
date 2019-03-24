import os
import datetime
from flask import Flask, jsonify
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../pypoker.db'
db = SQLAlchemy(app)

from .apis.game_api import game_bp
from .apis.auth_api import auth_bp
from .apis.player_api import player_bp

app.register_blueprint(game_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(player_bp)

if __name__ == "__main__":
    app.run()
            
            
            