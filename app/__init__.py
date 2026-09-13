from flask import Flask
from flask_login import LoginManager
import config
import logging, logging.handlers


#log formatting
log_formatter = '%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s'
formatter = logging.Formatter(log_formatter)
log_handler = logging.handlers.RotatingFileHandler("app.log",maxBytes=1000000)
log_handler.setFormatter(formatter)

app = Flask(__name__)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)

app.secret_key = config.SECRET_KEY
login: LoginManager = LoginManager(app)
login.login_view = 'login'

from app import routes