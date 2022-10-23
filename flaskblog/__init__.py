from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# extensions are imported here and initialized, // documentation pending

from flask_login import LoginManager
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a8136b88a8d0f8bef72a7681a0ff1d1a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flaskblog import routes