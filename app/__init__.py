from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import StringField, IntegerField
from flask_wtf.html5 import EmailField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
