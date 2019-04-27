import os
import datetime
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../wolfpoker.db'
db = SQLAlchemy(app)


from .apis import blueprint as api
db.create_all()


app.register_blueprint(api, url_prefix='/api')


if __name__ == "__main__":
    app.run()