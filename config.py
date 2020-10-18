# ----- [///// IMPORTS /////] -----
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# ----- [///// CONFIGURATIONS /////] -----
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SHH'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app, session_options={"autoflush": False})
