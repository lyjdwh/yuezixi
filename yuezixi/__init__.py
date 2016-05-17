from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import pymysql
from flask.ext.mail import Mail

app=Flask(__name__)
app.config.from_object('config')
db=SQLAlchemy(app)

lm=LoginManager()
lm.init_app(app)
lm.login_view='log_in'

mail=Mail(app)

from . import views,models