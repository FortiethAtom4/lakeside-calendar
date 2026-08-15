from flask import Flask
from flask_login import LoginManager
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
login: LoginManager = LoginManager(app)
login.login_view = 'login'

from app import routes