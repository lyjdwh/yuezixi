# -*-coding:utf-8 -*-
from flask import render_template,flash,redirect,url_for,g,session,request,current_app
from flask.ext.login import current_user,login_required,login_user,logout_user
from datetime  import datetime
from fuzzywuzzy import fuzz
from flask_mail import Message
from threading import Thread

from . import app
from . import lm,db,mail
from .models import User,PersonalData,Make_match,Mked
# from .forms import


def match_user(match_user):
    choice=[]


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.template_filter('time')
def time_filter(s):

    return s.strftime('%b %d %H:%M')



@app.before_request
def before_request():
    pass


@app.route('/index')
@login_required
def index():
    return  render_template('index.html')

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        user1=User(request.form['Name_0'],request.form['Password_0'])
        db.session.add(user1)
        db.session.commit()
        login_user(user1)
        return redirect(url_for('modify'))

    return render_template('register.html')

@app.route('/log_in',methods=['POST','GET'])
def log_in():
    error=None
    if request.method=="POST":
        user = User.query.filter_by(username=request.form['Name_0']).first()
        if user is None:
            error = 'Invalid username'
        elif user.verify_password(request.form['Password_0']) is not True:
            error = 'Invalid password'

        else:
            login_user(user)
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('log_in.html', error=error)


@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/modify',methods=['POST','GET'])
@login_required
def modify():
    if request.method=="POST":
        personal_data1 = current_user.PersonalData.first()

        if personal_data1 is not None:
            db.session.delete(personal_data1)
            db.commit()
        Name=request.form['Name_1']
        Sex=request.form['Sex_1']
        Major=request.form['Major_1']
        Phone_number=request.form['Phone_number_1']
        QQ=request.form['QQ_1']
        Email=request.form['Email_1']
        Best_subject=request.form['Best_subject_1']
        Worse_subject=request.form['Worse_subject_1']
        Self_introduction=request.form['Self_introduction_1']
        Goal=request.form['Goal']
        personal_data2=PersonalData(Name,Sex,Major,Phone_number,QQ,Email,Best_subject,Worse_subject,Self_introduction,Goal,current_user)
        db.session.add(personal_data2)
        db.session.commit()
        return redirect(url_for('index'))
    personal_data1 = current_user.PersonalData.first()
    return  render_template('modify.html',pd=personal_data1)
@app.route('/person')
@login_required
def person():
    personal_data1 = current_user.PersonalData.first()
    return render_template('person.html',pd=personal_data1)

@app.route('/make_meet',methods=['POST','GET'])
@login_required
def make_meet():
    if request.method=='POST':
        Subject=request.form['Subject']
        Course=request.form['Course']
        Location=request.form['Location']
        Start_time=request.form['Start_time']
        End_time=request.form['End_time']
        Target_1=request.form['Target1']
        Target_2=request.form['Target2']
        Number=request.form['Number']
        Remarks=request.form['Remarks']

        make_match1=Make_match(Subject,Course,Location,Start_time,End_time,Target_1,Target_2,Number,Remarks,current_user)
        db.session.add(make_match1)
        current_user.PersonalData.first().Shells = current_user.PersonalData.first().Shells + 1
        db.session.commit()


        return redirect(url_for('notice'))
    return render_template('make_meet.html')

@app.route('/notice',methods=['POST','GET'])
@app.route('/notice/<int:page>', methods = ['GET', 'POST'])
@login_required
def notice(page = 1):
    mks=Make_match.query.filter(Make_match.Number_1 < Make_match.Number ).order_by(Make_match.id.desc()).paginate(page, 2, False)

    return render_template('notice.html',mks=mks)

@app.route('/match_meet',methods=["POST","GET"])
def match_meet():
    if request.method == 'POST':
        Subject = request.form['Subject_1']
        Course = request.form['Course_1']
        Location = request.form['Location_1']
        Start_time = request.form['Start_time_1']
        End_time = request.form['Start_time']
        Target_1 = request.form['Target_1']
        Target_2 = request.form['Target_1']
        Number = request.form['Number_1']


        choices=[Subject,Course,Location,Start_time,End_time,Target_1,Target_2,Number]
        if (Make_match.query.filter(Start_time<=Make_match.Start_time,Make_match.Start_time<=End_time).all()) :
            mks=Make_match.query.filter(Start_time<=Make_match.Start_time,Make_match.Start_time<=End_time).all()
        elif (Make_match.query.filter(Start_time<=Make_match.End_time,Make_match.End_time<=End_time).all()):
            mks=Make_match.query.filter(Start_time<=Make_match.End_time,Make_match.End_time<=End_time).all()
        else:
            mks=Make_match.query.all()

        for mk in mks:
            mk.Score=fuzz.partial_ratio(Location,mk.Location)

        mks1=Make_match.query.filter(Make_match.Score>=80).order_by(Make_match.Score.desc()).all()

        for mk in mks1:
            a1=fuzz.partial_ratio(Subject,mk.Subject)
            a2=fuzz.partial_ratio(Course,mk.Course)
            a3=fuzz.partial_ratio(Target_1,mk.Target1)
            a4=fuzz.partial_ratio(Target_2,mk.Target2)
            mk.Score=mk.Score+a2+a2+a3+a4
        mks2=Make_match.query.order_by(Make_match.Score.desc()).limit(20).paginate(1, 21, False)
        return render_template('notice.html',mks=mks2)


    return render_template('match_meet.html')

@app.route('/current',methods=["POST","GET"])
def current():

    mkeds=current_user.Make_match.order_by(Make_match.id.desc()).first()
    if mkeds is None:
        return "你还没有发起自习，或者没人应约你的自习"
    else:
        return render_template('current.html',mkeds=mkeds.Mked.all())





@app.route('/invate/<int:id>', methods=["POST","GET"])
def invate(id):
    if request.method=='POST':
        mk = Make_match.query.filter_by(id=id).first()
        mk.Number_1=mk.Number_1+1
        db.session.commit()
        Sex = current_user.PersonalData.first().Sex
        Name = current_user.PersonalData.first().Name
        Major=current_user.PersonalData.first().Major
        Phone_number=current_user.PersonalData.first().Phone_number
        QQ=current_user.PersonalData.first().QQ
        Email=current_user.PersonalData.first().Email
        Grade=current_user.PersonalData.first().Grade
        Self_introduction=current_user.PersonalData.first().Self_introduction
        mked=Mked(Name,Sex,Email,Phone_number,QQ,Grade,Major,Self_introduction,mk)
        db.session.add(mked)
        current_user.PersonalData.first().Shells = current_user.PersonalData.first().Shells + 1
        db.session.commit()
        session['QQ']=mk.User.PersonalData.first().QQ
        return redirect(url_for('mail1'))

    if "match_meet" in request.referrer:
        g.last_page=request.referrer
    else:
        g.last_page=url_for('index')
    g.mk=Make_match.query.filter_by(id=id).first()
    return render_template('invate.html')

@app.route("/mail1")
def mail1():
    #send_email('约自习', ('me', '1412511544@qq.com'), ['15207183373@163.com'],'hello')
    #return 'good'
    invite_data=PersonalData.query.filter_by(QQ=session['QQ']).first()
    invited_data=current_user.PersonalData.first()

    str2="你已经应约了"+invite_data.Name.encode('utf-8')+"的自习啦， 她/他的qq:"+invite_data.QQ.encode('utf-8')+", Email:"+invite_data.Email.encode('utf-8')+", 你们可以在线下联系呦， 祝你们学习愉快"
    str1="有人应约你的自习啦， 他/她的名字："+invited_data.Name.encode('utf-8')+", 年级："+invited_data.Grade.encode('utf-8')+", 专业："+invited_data.Major.encode('utf-8')+", qq:"+invited_data.QQ.encode('utf-8')+", Email:"+invited_data.Email.encode('utf-8')+", 你们可以在线下联系呦，祝你们学习愉快"
    send_email('约自习',('me','1412511544@qq.com'),[invited_data.Email],str2)
    send_email('约自习',('me','1412511544@qq.com'),[invite_data.Email],str1)
    return 'good'


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()


















