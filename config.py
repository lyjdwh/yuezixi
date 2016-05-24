# -*-coding:utf-8 -*-
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'



SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:abc201314@localhost/lyjdwh'#mysql的配置
SQLALCHEMY_TRACK_MODIFICATIONS=True

MAIL_SERVER=''#邮箱服务器
MAIL_PORT=465
MAIL_USE_SSL=True
MAIL_USERNAME=''#如果是qq邮箱则为qq号，136邮箱同理
MAIL_PASSWORD=''#客户端密码
MAIL_USE_TLS = False
ADMINS=['1412511544@qq.com']


WHOOSH_BASE='mysql+pymysql://root:abc201314@localhost/lyjdwh'
MAX_SEARCH_RESULTS = 50






#MAIL_DEFAULT_SENDER='系统'
