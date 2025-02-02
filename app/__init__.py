# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from instance import config

app = Flask(__name__)
app.config.from_object(config.Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) or None

from .routes import *
from .models import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    