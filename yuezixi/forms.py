#-×-coding:utf-8-*-
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,PasswordField,TextAreaField
from wtforms.validators import DataRequired,EqualTo,Email
from flask_wtf.file import FileField,FileAllowed,FileRequired


class LoginForm(Form):
    Name_0=StringField("Name_0",validators=[DataRequired(message=u'姓名忘填啦')])
    Password_0=PasswordField('Password_0',validators=[DataRequired()])
    Submit=SubmitField('submit')

class RegisterForm(Form):
    Name_0=StringField(u'姓名:',validators=[DataRequired(message=u'姓名忘填啦')])
    Password_0=PasswordField(u'密码:',validators=[DataRequired(u'密码忘填啦')])
    Password_01=PasswordField(u'确认密码:',validators=[DataRequired(u'密码忘填啦'),EqualTo('Password_0',message=u'两次密码不一致')])
    Summit=SubmitField('summit')
class DataForm(Form):
    Email_1= StringField(u'邮箱',[Email(message=u'邮箱格式不对'),DataRequired(message=u'最重要的邮箱没填(⊙o⊙)哦')])
    Photo=FileField(u'头像', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    Self_introduction_1=TextAreaField(u'自我介绍：')
    Summit=SubmitField('Summit')
