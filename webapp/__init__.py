import logging, os, logging.handlers
from flask import Flask, g
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

home = os.path.expanduser('~')

app = Flask(__name__)

app.config['webapp_database_uri'] = "dbname=ptdb host=127.0.0.1  user=pt"
app.config['app_base_url'] = "http://192.168.42.141/"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'png', 'gif','JPG','PNG', 'JPEG', 'jpeg','GIF']
app.config['UPLOAD_PATH'] = 'webapp/static/images/uploads/'
app.config['UPLOAD_LOGO_PATH'] = 'webapp/static/images/logos/'
app.config['SCREENSHOTS_UPLOAD_PATH'] = 'webapp/static/images/uploads/screenshots/'
app.config['DEVELOPMENT'] = False
app.config['ADMIN_EMAIL'] = 'admin@pt.local'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

WEBAPP_CONFIG_FILE=os.path.join(home, "webapp_config.json")

app.config.update(dict(
  DEBUG=True,
  CSRF_ENABLED=True,
  SECRET_KEY='SECRET_KEY_HERE',
  WEBAPP_CONFIG_FILE = WEBAPP_CONFIG_FILE,
))

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

import webapp.database
import webapp.routes
import webapp.forms
import webapp.login



