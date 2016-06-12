#-×-coding:utf-8-*-
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


ADMINS=app.config['ADMINS']
MAIL_SERVER=app.config['MAIL_SERVER']
MAIL_PORT=app.config['MAIL_PORT']
MAIL_USERNAME=app.config['MAIL_USERNAME']
MAIL_PASSWORD=app.config['MAIL_PASSWORD']

MAIL=app.config['MAIL']

if not app.debug:
    import logging
    from logging import Formatter



    from logging.handlers import SMTPHandler
    credentials = (MAIL_USERNAME,MAIL_PASSWORD)
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),MAIL,ADMINS, 'your application failed', credentials)
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(Formatter('''
       Message type:       %(levelname)s
       Location:           %(pathname)s:%(lineno)d
       Module:             %(module)s
       Function:           %(funcName)s
       Time:               %(asctime)s

       Message:

       %(message)s
       '''))
    app.logger.addHandler(mail_handler)
    #通过电子邮件发错误
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('tmp/yuezixi.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('app startup')
    #记录错误到文件
from . import views,models