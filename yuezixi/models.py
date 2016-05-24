from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

#import flask.ext.whooshalchemy

#from jieba.analyse import ChineseAnalyzer

class User(db.Model,UserMixin):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30),unique=True)
    password_hash = db.Column(db.String(128))


    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __init__(self,username,password):
        self.username=username
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>'%self.username

class PersonalData(db.Model):
   # __searchable__ = ['Name']
    #__analyzer__ = ChineseAnalyzer()
    #__tablename__='personaldata'
    id=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(20))
    Sex=db.Column(db.String(10))
    Email = db.Column(db.String(30))
    Phone_number=db.Column(db.String(25))
    QQ=db.Column(db.String(20))
    Shells=db.Column(db.Integer,default=0)
    Rank=db.Column(db.String(30),default="0")
    Grade=db.Column(db.String(15) ,default="0")
    Major=db.Column(db.String(30))
    Best_subject=db.Column(db.String(40))
    Worse_subject=db.Column(db.String(40))
    Goal=db.Column(db.String(80))
    Self_introduction=db.Column(db.Text)
    Photo=db.Column(db.String(40))
    PersonalData_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    User= db.relationship('User', backref=db.backref('PersonalData', lazy='dynamic'))

    def __init__(self,Name,Sex,Major,Phone_number,QQ,Email,Best_subject,Worse_subject,Self_introduction,Goal,Photo,User):
        self.Name=Name
        self.Sex=Sex
        self.Major=Major
        self.Phone_number=Phone_number
        self.QQ=QQ
        self.Email=Email
        self.Best_subject=Best_subject
        self.Worse_subject=Worse_subject
        self.Self_introduction=Self_introduction
        self.Goal=Goal
        self.Photo=Photo
        self.User=User

    def __repr__(self):
        return '<User %r>'%self.Name

class Make_match(db.Model):
    #__tablename__ = 'make_match'


    id=db.Column(db.Integer,primary_key=True)
    Subject=db.Column(db.String(20))
    Course=db.Column(db.String(20))
    Location=db.Column(db.String(30))
    Start_time=db.Column(db.DateTime)
    End_time=db.Column(db.DateTime)
    Target1=db.Column(db.String(20))
    Target2=db.Column(db.String(20))
    Number=db.Column(db.Integer)
    Remarks=db.Column(db.Text)
    Number_1=db.Column(db.Integer,default='0')
    Score=db.Column(db.Integer,default=0)
    Make_match_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    User = db.relationship('User', backref=db.backref('Make_match', lazy='dynamic'))

    def __init__(self,Subject,Course,Location,Start_time,End_time,Target_1,Target_2,Number,Remarks,User):
        self.Subject=Subject
        self.Course=Course
        self.Location=Location
        self.Start_time=Start_time
        self.End_time=End_time
        self.Target1=Target_1
        self.Target2=Target_2
        self.Number=Number
        self.Remarks=Remarks
        self.User=User

    def __repr__(self):
        return '<Match %r>' % self.User

class Mked(db.Model):
    id=id=db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(20))
    Sex = db.Column(db.String(10))
    Email = db.Column(db.String(30))
    Phone_number = db.Column(db.String(25))
    QQ = db.Column(db.String(20))
    Grade = db.Column(db.String(15))
    Major = db.Column(db.String(30))
    Self_introduction = db.Column(db.Text)
    Mked_id=db.Column(db.Integer,db.ForeignKey('make_match.id'))
    Make_match = db.relationship('Make_match', backref=db.backref('Mked', lazy='dynamic'))
    Photo=db.Column(db.String(30))

    def __init__(self,Name,Sex,Email,Phone_number,QQ,Grade,Major,Self_introduction,Photo,Make_match):
        self.Name = Name
        self.Sex = Sex
        self.Major = Major
        self.Phone_number = Phone_number
        self.QQ = QQ
        self.Email = Email
        self.Grade=Grade
        self.Self_introduction = Self_introduction
        self.Make_match=Make_match
        self.Photo=Photo

    def __repr__(self):
        return '<Mked %>'% self.Name




db.create_all()



















