from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('flaskommerce.cfg')

db = SQLAlchemy()
db.init_app(app)

from app import routes
