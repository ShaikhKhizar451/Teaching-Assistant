from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TA.db'
db.init_app(app)

from .models import TA, User

with app.app_context():
    db.create_all()

from .route import app

def str_to_bool(s):
    if s.lower() in ['true']:
        return True
    elif s.lower() in ['false']:
        return False
    else:
        raise ValueError("Invalid boolean value: " + s)
