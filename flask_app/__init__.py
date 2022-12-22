from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__) #creating a flask instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanban.sqlite3'
#flask-login needs a secret key to work
app.config['SECRET_KEY'] = 'a_very_secret_key'
app.config['UPLOAD_FOLDER'] = "./flask_app/user_data/" # folder where the user uploaded files will be saved

db = SQLAlchemy(app) #creating a SQLAlchemy instance
login_manager = LoginManager()
login_manager.init_app(app) #creating a login_manager instance
bcrypt = Bcrypt(app) #creating a bcrypt instance

from flask_app import views