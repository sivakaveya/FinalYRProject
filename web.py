from atexit import register
from email import feedparser
from urllib.robotparser import RequestRate
from flask import render_template, Flask,request, session, redirect, url_for, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null
from sqlalchemy import func
import bcrypt
from mail import mail
import random
from werkzeug.utils import secure_filename
from io import BytesIO
from datetime import datetime
import os
import io
import urllib.request,json
import requests
import ast
import validators
import pdfkit
import time
from coursescraper import scrapallcourse
from socialMedia import SocialMedia
import stripe
import json
from dotenv import load_dotenv, find_dotenv
from report import report
from feedbackmail import feedbackmail
from events_scrapper import *
from international_eventscrapper import *
from cancelEvent import cancelEvent


app=Flask(__name__,template_folder='templates',static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Phoenix.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='ikstao'
db = SQLAlchemy(app)
APP_ROOT=os.path.dirname(os.path.abspath(__file__))

# Setup Stripe python client library.
load_dotenv(find_dotenv())

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_version = '2020-08-27'


class Login(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    lid = db.Column(db.String(100))
    name = db.Column(db.String(20))
    email = db.Column(db.String(50))
    password = db.Column(db.String(20))
    role = db.Column(db.String(10))

class Client(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    lid=db.Column(db.String(100), db.ForeignKey("login.lid"), nullable=False)
    name = db.Column(db.String(20))
    occupation = db.Column(db.String(20))
    institute= db.Column(db.String(100))
    email = db.Column(db.String(50))
    cover_photo=db.Column(db.String(100))
    profile_photo=db.Column(db.String(100))
    description=db.Column(db.String(5000))
    phoneNo=db.Column(db.Integer)
    linkedin = db.Column(db.String(100))
    gender=db.Column(db.String(100))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def obj_to_dict(self):  # for build json format
        return {
            "lid": self.lid,
            "name": self.name,
            "occupation": self.occupation,
            "institute": self.institute,
            "email": self.email,
            "cover-photo": self.cover_photo,
            "profile_photo": self.profile_photo,
            "description": self.description,
            "phoneNo": self.phoneNo,
            "linkedin": self.linkedin
        }

class Registeration(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    rid=db.Column(db.String(200))
    lid=db.Column(db.String(100), db.ForeignKey("login.lid"), nullable=False)
    eid=db.Column(db.String(200), db.ForeignKey("event.eid"), nullable=False)
###########TEMPORARY COMMENTED DONT DELETE###########
# class Certificate(db.Model):
#     id=db.Column(db.Integer, primary_key=True)
#     lid=db.Column(db.String(100), db.ForeignKey("login.lid"), nullable=False)
#     certificate_link=db.Column(db.String(200))
#     eid=db.Column(db.String(100), db.ForeignKey("event.eid"), nullable=False)
######################################################

class Notification(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    lid=db.Column(db.String(100))
    eid=db.Column(db.String(200))
    message=db.Column(db.String(200))

class Feedback(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    lid = db.Column(db.String(100))
    eid = db.Column(db.String(100))
    q1 = db.Column(db.Integer)
    q2 = db.Column(db.Integer)
    q3 = db.Column(db.Integer)
    q4 = db.Column(db.Integer)
    q5 = db.Column(db.Integer)
    q6 = db.Column(db.String(500))

class Event(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    eid=db.Column(db.String(200))
    orgImg=db.Column(db.String(200))
    lid=db.Column(db.String(100), db.ForeignKey("login.lid"), nullable=False)
    name = db.Column(db.String(20))
    domain = db.Column(db.String(50))
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    endTime = db.Column(db.String(50))
    eventImg = db.Column(db.String(300))
    regLastDate = db.Column(db.String(50))
    fees = db.Column(db.String(100))
    eventMode = db.Column(db.String(10))
    location = db.Column(db.String(1000))
    description = db.Column(db.String(1000))
    ptOfContact_name= db.Column(db.String(200))
    ptOfContact_phone= db.Column(db.String(200))
    ptOfContact_email= db.Column(db.String(200))
    noOfSpeakers=db.Column(db.Integer)
    speaker1Name=db.Column(db.String(200))
    speaker1LinkedIn=db.Column(db.String(500))
    speaker1Img=db.Column(db.String(300))
    speaker1Description=db.Column(db.String(1000))
    speaker2Name=db.Column(db.String(200))
    speaker2LinkedIn=db.Column(db.String(500))
    speaker2Img=db.Column(db.String(300))
    speaker2Description=db.Column(db.String(1000))
    speaker3Name=db.Column(db.String(200))
    speaker3LinkedIn=db.Column(db.String(500))
    speaker3Img=db.Column(db.String(300))
    speaker3Description=db.Column(db.String(1000))
    
    

class ClientInterest(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    lid=db.Column(db.String(100), db.ForeignKey("login.lid"), nullable=False)
    interest=db.Column(db.String(50))

class Orgdata(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    lid=db.Column(db.String(100), db.ForeignKey("login.lid"), nullable=False)
    name = db.Column(db.String(20))
    institute= db.Column(db.String(100))
    email = db.Column(db.String(50))
    cover_photo=db.Column(db.String(100))
    profile_photo=db.Column(db.String(100))
    description=db.Column(db.String(5000))
    phoneNo=db.Column(db.Integer)
    linkedin = db.Column(db.String(100))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def create_path(filename):
    target = os.path.join(APP_ROOT,'static//images/')
    location = "events/".join([target, filename])
    return location


@app.route('/',methods=['POST','GET'])
def home():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        user = Login.query.filter_by(email=email).first()
        if user==None:
            return render_template('login.html', user_exists=0)
        try:
            if email == user.email:
                if bcrypt.checkpw(password.encode('utf-8'), user.password):
                    session['email']=email
                    session['role']=user.role
                    session['name']=user.name
                    session['lid']=user.lid
                    if user.role == 'user':
                        return redirect(url_for('clientDashboard'))
                    else:
                        return redirect(url_for('organisationDashboard'))
                else:
                    return render_template('login.html',password=1)
        except:
            return "There is an error in logging in"
    else:
        return render_template('login.html')

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        session['name']=name
        role=request.form.get('role')
        if role!='organisation':
            role='user'
        session['role']=role
        email = request.form.get('email')
        session['email']=email
        global genotp 
        exists = db.session.query(Login.id).filter_by(email=email).first() is not None
        if exists:
            return render_template('signUp.html', user_exists=1)
        else:
            genotp= random.randint(1000,9999)
            mail.send_mail('phoenixatsih@gmail.com','uhyhrxcaadzjhomi', email,str(genotp))
            return redirect(url_for('otp'))

    return render_template('signUp.html')


@app.route("/otp", methods = ["GET", "POST"])
def otp():
    if request.method == 'POST':       
        otp = request.form.get('otp')
        if str(otp) == str(genotp):
            return redirect(url_for('createPassword'))
        else:
            return render_template("verifyOtp.html", verified=2)
    else:
        return render_template("verifyOtp.html",verified=0)

@app.route("/createPassword", methods = ["GET", "POST"])
def createPassword():
    if request.method == 'POST':
        name = session['name']
        email = session['email']
        role = session['role']
        password = request.form.get('password')
        cnfpassword = request.form.get('cnfpassword')
        if password==cnfpassword:
            exists = db.session.query(Login.id).filter_by(email=email).first() is not None
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            if exists:
                db.session.query(Login).filter(Login.email == email).update({'password': hashed})
                db.session.commit()
            else:
                lid = createIdLogin(role,email)
                session['lid']=lid
                time.sleep(2)
                new_entry=Login(lid=lid, name=name, email=email, password=hashed, role=role)
                db.session.add(new_entry)
                db.session.commit()
                if role=='user':
                    new_entry=Client(lid=lid, name=name,gender=None, occupation=None, institute= None, email = email, cover_photo= 'default.jpg', profile_photo='default.jpg', description=None, phoneNo=None, linkedin = None)
                    db.session.add(new_entry)
                    db.session.commit()
                else:
                    new_entry=Orgdata(lid=lid, name=name, institute= None, email = email, cover_photo= 'default.jpg', profile_photo='default.jpg', description=None, phoneNo=None, linkedin = None)
                    db.session.add(new_entry)
                    db.session.commit()
            if session['role']=='user':
                return redirect(url_for('clientDashboard'))
            else:
                return redirect(url_for('organisationDashboard'))
        else:
            render_template("createPassword.html",different_password=1)
    else:
        return render_template("createPassword.html")

@app.route("/forgotPassword", methods = ["GET", "POST"])
def forgotPassword():
    if request.method == 'POST':
        email = request.form.get('email')
        session['email']=email
        user = Login.query.filter_by(email=email).first()
        if user==None:
            return render_template('login.html', user_exists=0)
        else:
            session['name']=user.name
            session['role']=user.role
            global genotp 
            genotp= random.randint(1000,9999)
            mail.send_mail('phoenixatsih@gmail.com','uhyhrxcaadzjhomi', email,str(genotp))
            return redirect(url_for('otpForgotPassword'))
    else:
        return render_template('forgotPassword.html')

@app.route("/otpForgotPassword", methods = ["GET", "POST"])
def otpForgotPassword():
    if request.method == 'POST':
        otp = request.form.get('otp')
        if str(otp) == str(genotp):
            return render_template("createPassword.html")
        else:
            return render_template("otpForgotPassword.html", wrong_otp=1)
    else:
        return render_template("otpForgotPassword.html",verified=0)

@app.route('/clientDashboard',methods=['POST','GET'])
def clientDashboard():
    if session['role']=='user':
        if request.method == 'POST':
            eid=request.form.get('delete_not')
            print(eid)
            Notification.query.filter_by(eid=eid).delete()
            db.session.commit()
        e=upcomingEvents()
        l=registeredupcomingEvents(lid=session['lid'])
        n=showNotifications(lid=session['lid'])
        exevents=knowafest()
        user=db.session.query(ClientInterest).filter_by(lid=session['lid']).all()
        global international_events
        international_events=[]
        if len(international_events)==0:
            
            for u in user:
                temp=int_event(u.interest)
                international_events.extend(temp)
        global courses
        courses=[]
        if len(courses)==0:
            
            courses.extend(getCourses(session['lid']))
        return render_template('clientDashboard.html',events=e,international_events=international_events[:12], registered=l[1], ongoing=l[0], notifications=n, exevents=exevents[:12], courses=courses[:-1])
    else:
        return redirect(url_for('home'))

@app.route('/organisationDashboard',methods=['POST','GET'])
def organisationDashboard():
    if session['role']=='organisation':
        if request.method=='POST':
            if request.form.get('close_reg'):
                close_eid=request.form.get('close_reg')
                db.session.query(Event).filter(Event.eid == close_eid).update({'regLastDate': datetime.utcnow()})
                db.session.commit()
            if request.form.get('report'):
                eid=request.form.get('report')
                global summary
                summary=''
                summary=request.form.get('summary')
                print(summary)
                return redirect(url_for('report', eid=eid))
            if request.form.get('send_cert'):
                eid=request.form.get('send_cert')
                ############# Code to send Certificates ##########
                ##################################################
                push_notification(eid)
            else:
                eid=request.form.get('delete_not')
                Notification.query.filter_by(eid=eid).delete()
                db.session.commit()
                send_feedback_link(eid)
        events=eventsOrg(lid=session['lid'])
        push_notification_org(session['lid'])
        notifications=showNotifications(session['lid'])

        ######## This part of code is for testing the feedback form #########
        ######## This code is supposed to work when organizer clicks on send feedback for a particular event########
        ######## Do not delete #######

        send_feedback_link('o_sivakaveyaSample1660464326.58539')

        ######## END OF TEST CODE #########
        return render_template('orgDashboard.html', ongoing=events['ongoing'], reg_open=events['reg_open'], reg_close=events['reg_close'], completed=events['completed'], completed_sentcert=events['completed_sentcert'], notifications=notifications)
    else:
        return redirect(url_for('home'))

# @app.route('/addEvent',methods=['POST','GET'])
# def addEvent():
#     if request.method == 'POST' and request.form.get('submit')=='submit':
#         name = request.form.get('name')
#         eid=createIdEvent(name)
#         domain=request.form.get('domain')
#         eventImg = request.files['eventImg']
#         #print(eventImg)
#         if eventImg:
#             filename = secure_filename(eventImg.filename)
#             destination= create_path(filename,eid)
#             eventImg.save(destination)
#             fname=destination[destination.index('o_'):]
#         else:
#             fname=None
#         date = request.form.get('date')
#         time = request.form.get('time')
#         endTime = request.form.get('endTime')
#         regLastDate = request.form.get('regLastDate')
#         fees = request.form.get('fees')
#         eventMode = request.form.get('mode')
#         city=request.form.get('city')
#         link=request.form.get('link')
#         fees=str(int(fees)*100)
#         stripe.Product.create(
#             name=eid,
#             default_price_data={
#                 "unit_amount": fees,
#                 "currency": "INR",
#             },
#             expand=["default_price"],
#         )
#         # print(3)
#         if city:
#             eventMode='offline'
#             location=city
#         elif link:
#             eventMode='online'
#             location=link
#         else:
#             eventMode='platform'
#             location='platform link'
#         description = request.form.get('description')
#         ptOfContact_name= request.form.get('ptOfContact_name')
#         ptOfContact_phone= request.form.get('ptOfContact_phone')
#         ptOfContact_email= request.form.get('ptOfContact_email')
#         speaker1Name=request.form.get('speaker1Name')
#         noOfSpeakers=0
#         if speaker1Name:
#             noOfSpeakers+=1
#             speaker1LinkedIn=request.form.get('speaker1LinkedIn')
#             speaker1Img=request.files['speaker1Img']
#             filename = secure_filename(speaker1Img.filename)
#             destination= create_path_speaker(filename, eid, 1)
#             speaker1Img.save(destination)
#             fname1=destination[destination.index('o_'):]
#             speaker1Description=request.form.get('speaker1Description') 
#         else:
#             speaker1Name=None
#             speaker1LinkedIn=None
#             speaker1Description=None
#             fname1=None
#         speaker2Name=request.form.get('speaker2Name')
#         if speaker2Name:
#             noOfSpeakers+=1
#             speaker2LinkedIn=request.form.get('speaker2LinkedIn')
#             speaker2Img=request.files['speaker2Img']
#             filename = secure_filename(speaker2Img.filename)
#             destination= create_path_speaker(filename, eid, 2)
#             speaker2Img.save(destination)
#             fname2=destination[destination.index('o_'):]
#             speaker2Description=request.form.get('speaker2Description')
#         else:
#             speaker2Name=None
#             speaker2LinkedIn=None
#             fname2=None
#             speaker2Description=None
#         speaker3Name=request.form.get('speaker3Name')
#         if speaker3Name:
#             noOfSpeakers+=1
#             speaker3LinkedIn=request.form.get('speaker3LinkedIn')
#             speaker3Img=request.files['speaker3Img']
#             filename = secure_filename(speaker3Img.filename)
#             destination= create_path_speaker(filename, eid, 3)
#             speaker3Img.save(destination)
#             fname3=destination[destination.index('o_'):]
#             speaker3Description=request.form.get('speaker3Description')
#         else:
#             speaker3Name=None
#             speaker3LinkedIn=None
#             fname3=None
#             speaker3Description=None
#         orgImg=db.session.query(Orgdata.profile_photo).filter_by(lid=session['lid']).first()
#         new_entry=Event(eid=eid, lid=session['lid'], name=name,orgImg=orgImg[0], domain = domain, date = date, time = time, endTime = endTime,
#                     eventImg = fname, regLastDate = regLastDate, fees = fees, eventMode = eventMode, location = location, 
#                     description = description, ptOfContact_name= ptOfContact_name, ptOfContact_phone= ptOfContact_phone,
#                     ptOfContact_email= ptOfContact_email, noOfSpeakers=noOfSpeakers, speaker1Name=speaker1Name,
#                     speaker1LinkedIn=speaker1LinkedIn, speaker1Img=fname1, speaker1Description=speaker1Description,
#                     speaker2Name=speaker2Name, speaker2LinkedIn=speaker2LinkedIn, speaker2Img=fname2,speaker2Description=speaker2Description,
#                     speaker3Name=speaker3Name, speaker3LinkedIn=speaker3LinkedIn, speaker3Img=fname3, speaker3Description=speaker3Description)
#         db.session.add(new_entry)
#         db.session.commit()
#         return redirect(url_for('organisationDashboard'))
#     else:
#         notifications=showNotifications(session['lid'])
#         domains=['Artificial Intelligence','Web Developement', 'Machine Learning','Deep Learning','Block Chain','IOE / IOT','Embedded System','Raspberry Pi','Mechanical Robotics','Power Electronics','Antenna','Android','Cloud Computing','Big Data','VLSI','Image Processing','RPA','Cyber Security','Data mining','Industry 4.0','Information Security','Computer Networking','Data Science','Neural Network','Software Engineering']
#         return render_template('Add_Event.html', domains=domains, notifications=notifications)


@app.route('/feedback/<lid>/<eid>',methods=['POST','GET'])
def feedback(lid,eid):
    user=db.session.query(Client).filter_by(lid=lid).first()
    event=db.session.query(Event).filter_by(eid=eid).first()
    
    if request.method=='POST':
        q1=request.form.get('Q1')
        q2=request.form.get('Q2')
        q3=request.form.get('Q3')
        q4=request.form.get('Q4')
        q5=request.form.get('Q5')
        q6=request.form.get('Q6')
        new_entery=Feedback(lid=lid,eid=eid,q1=q1,q2=q2,q3=q3,q4=q4,q5=q5,q6=q6)
        db.session.add(new_entery)
        db.session.commit()
        session['email']=user.email
        session['role']='user'
        session['name']=user.name
        session['lid']=user.lid
        return redirect(url_for('clientDashboard'))
    else:
        exists = db.session.query(Feedback.id).filter_by(lid=lid, eid=eid).first() is not None
        if exists:
            session['email']=user.email
            session['role']='user'
            session['name']=user.name
            session['lid']=user.lid
            return redirect(url_for('clientDashboard'))
        else:
            
            return render_template('feedback.html',user=user,event=event)

@app.route('/eventPage/<eid>',methods=['POST','GET'])
def eventPage(eid):
    event = Event.query.filter_by(eid=eid).first()
    global eventid
    eventid=eid
    global fees 
    fees=event.fees
    if request.method=='POST':
        if request.form.get('cancel'):
            Registeration.query.filter_by(lid=session['lid']).delete()
            db.session.commit()
            return redirect(url_for('clientDashboard'))
        rid=createIdRegisteration(session['lid'],eid)
        new_entry=Registeration(rid=rid,lid=session['lid'],eid=eid)
        db.session.add(new_entry)
        db.session.commit()
    lst=[]
    lst=stripe.Product.list()
    #print(lst['data'])
    global price
    for js in lst:
        if(js['name']==eid):
            #print(js['default_price'])
            price= js['default_price']
            #print(price)
        if fees=='0':
            price='0'
    org = Orgdata.query.filter_by(lid=event.lid).first()
    sm = SocialMedia()
    socialmediasites = sm.GetSocialMediaSites_WithShareLinks_OrderedByPopularity()
    socialmediaurls = sm.GetSocialMediaSiteLinks_WithShareLinks({
        'url':url_for(request.endpoint, **request.view_args),
        'title':event.name,
        'desc':'%0d%0aCheck this event out%0d%0a'+event.name+'%0d%0a'+event.description+'%0d%0aon Phoenix! %0d%0a',
        'image':url_for('static', filename='/images/events'+event.eventImg)
    })

    socialmediaurls['copy']=url_for(request.endpoint, **request.view_args, _external=True)
    notifications=showNotifications(session['lid'])
    exists = db.session.query(Registeration.id).filter_by(lid=session['lid'], eid=eid).first() is not None
    if exists:
        return render_template('Event_Page.html',price=price, event=event, org=org, socialmediaurls=socialmediaurls, registered=1, notifications=notifications)
    
    return render_template('Event_Page.html', event=event, org=org, socialmediaurls=socialmediaurls, notifications=notifications)


@app.route('/event_page_org/<eid>',methods=['POST','GET'])
def event_page_org(eid):
    event = Event.query.filter_by(eid=eid).first()
    global eventid
    eventid=eid
    session['eid']=eid
    if request.method=='POST':
        if request.form.get('cancel')=='cancel':
            reason=request.form.get('reason')
            send_cancel_email(eid,event.name,reason)
            Event.query.filter_by(eid=eid).delete()
            db.session.commit()
            return redirect(url_for('organisationDashboard'))
        if request.form.get('modify')=='modify':
            return redirect(url_for('addEvent'))
    
    org = Orgdata.query.filter_by(lid=event.lid).first()
    sm = SocialMedia()
    socialmediasites = sm.GetSocialMediaSites_WithShareLinks_OrderedByPopularity()
    socialmediaurls = sm.GetSocialMediaSiteLinks_WithShareLinks({
        'url':url_for(request.endpoint, **request.view_args),
        'title':event.name,
        'desc':'%0d%0aCheck this event out%0d%0a'+event.name+'%0d%0a'+event.description+'%0d%0aon Phoenix! %0d%0a',
        'image':url_for('static', filename='/images/events'+event.eventImg)
    })
    socialmediaurls['copy']=url_for(request.endpoint, **request.view_args)
    notifications=showNotifications(session['lid'])
    exists = db.session.query(Registeration.id).filter_by(lid=session['lid'], eid=eid).first() is not None
    if exists:
        return render_template('org_event_page.html',price=price, event=event, org=org, socialmediaurls=socialmediaurls, registered=1, notifications=notifications)
    
    return render_template('org_event_page.html', event=event, org=org, socialmediaurls=socialmediaurls, notifications=notifications)


@app.route('/addEvent',methods=['POST','GET'])
def addEvent():
    if session.get("eid") != None:
        event=db.session.query(Event).filter_by(eid=session['eid']).first()
        session.pop('eid', None)  
    if request.method=='POST' and request.form.get('bg')=='bg':
        eventImg = request.files['eventImg']
        if eventImg:
            filename = secure_filename(eventImg.filename)
            print(filename)
            destination= create_path(filename,eid)
            eventImg.save(destination)
            fname=destination[destination.index('o_'):]
    if request.method == 'POST' and request.form.get('submit')=='submit':
        name = request.form.get('name')
        eid=createIdEvent(name)
        domain=request.form.get('domain')
        eventImg = request.files['eventImg']
        if eventImg:
            filename = secure_filename(eventImg.filename)
            print(filename)
            destination= create_path(filename,eid)
            eventImg.save(destination)
            fname=destination[destination.index('o_'):]
        else:
            fname=None
        date = request.form.get('date')
        time = request.form.get('time')
        endTime = request.form.get('endTime')
        regLastDate = request.form.get('regLastDate')
        fees = request.form.get('fees')
        eventMode = request.form.get('mode')
        city=request.form.get('city')
        link=request.form.get('link')
        fees=str(int(fees)*100)
        stripe.Product.create(
            name=eid,
            default_price_data={
                "unit_amount": fees,
                "currency": "INR",
            },
            expand=["default_price"],
        )
        # print(3)
        if city:
            eventMode='offline'
            location=city
        elif link:
            eventMode='online'
            location=link
        else:
            eventMode='platform'
            location='platform link'
        description = request.form.get('description')
        ptOfContact_name= request.form.get('ptOfContact_name')
        ptOfContact_phone= request.form.get('ptOfContact_phone')
        ptOfContact_email= request.form.get('ptOfContact_email')
        speaker1Name=request.form.get('speaker1Name')
        noOfSpeakers=0
        if speaker1Name:
            noOfSpeakers+=1
            speaker1LinkedIn=request.form.get('speaker1LinkedIn')
            speaker1Img=request.files['speaker1Img']
            if speaker1Img:
                filename = secure_filename(speaker1Img.filename)
                destination= create_path_speaker(filename, eid, 1)
                speaker1Img.save(destination)
                fname1=destination[destination.index('o_'):]
                speaker1Description=request.form.get('speaker1Description') 
        else:
            speaker1Name=None
            speaker1LinkedIn=None
            speaker1Description=None
            fname1=None
        speaker2Name=request.form.get('speaker2Name')
        if speaker2Name:
            noOfSpeakers+=1
            speaker2LinkedIn=request.form.get('speaker2LinkedIn')
            
            speaker2Img=request.files['speaker2Img']
            if speaker2Img:
                filename = secure_filename(speaker2Img.filename)
                destination= create_path_speaker(filename, eid, 2)
                speaker2Img.save(destination)
                fname2=destination[destination.index('o_'):]
                speaker2Description=request.form.get('speaker2Description')
        else:
            speaker2Name=None
            speaker2LinkedIn=None
            fname2=None
            speaker2Description=None
        speaker3Name=request.form.get('speaker3Name')
        if speaker3Name:
            noOfSpeakers+=1
            speaker3LinkedIn=request.form.get('speaker3LinkedIn')
            speaker3Img=request.files['speaker3Img']
            if speaker3Img:
                filename = secure_filename(speaker3Img.filename)
                destination= create_path_speaker(filename, eid, 3)
                speaker3Img.save(destination)
                fname3=destination[destination.index('o_'):]
                speaker3Description=request.form.get('speaker3Description')
        else:
            speaker3Name=None
            speaker3LinkedIn=None
            fname3=None
            speaker3Description=None
        if session.get("eid") != None:
            db.session.query(Event).filter(Event.eid == session['eid']).update({'name': name, 'domain':domain, 'date':date, 'time':time, 'endTime':endTime,
            'regLastDate':regLastDate, 'fees':fees, 'ptOfContact_name':ptOfContact_name, 'ptOfContact_phone':ptOfContact_phone, 'ptOfContact_email':ptOfContact_email,
            'noOfSpeakers':noOfSpeakers, 'speaker1Name':speaker1Name, 'speaker1LinkedIn':speaker1LinkedIn, 'speaker2Name':speaker2Name, 'speaker2LinkedIn':speaker2LinkedIn,
            'speaker3Name':speaker3Name, 'speaker3LinkedIn':speaker3LinkedIn})
            db.session.commit()
            return redirect(url_for('organisationDashboard'))
        
        orgImg=db.session.query(Orgdata.profile_photo).filter_by(lid=session['lid']).first()
        new_entry=Event(eid=eid, lid=session['lid'], name=name,orgImg=orgImg[0], domain = domain, date = date, time = time, endTime = endTime,
                    eventImg = fname, regLastDate = regLastDate, fees = fees, eventMode = eventMode, location = location, 
                    description = description, ptOfContact_name= ptOfContact_name, ptOfContact_phone= ptOfContact_phone,
                    ptOfContact_email= ptOfContact_email, noOfSpeakers=noOfSpeakers, speaker1Name=speaker1Name,
                    speaker1LinkedIn=speaker1LinkedIn, speaker1Img=fname1, speaker1Description=speaker1Description,
                    speaker2Name=speaker2Name, speaker2LinkedIn=speaker2LinkedIn, speaker2Img=fname2,speaker2Description=speaker2Description,
                    speaker3Name=speaker3Name, speaker3LinkedIn=speaker3LinkedIn, speaker3Img=fname3, speaker3Description=speaker3Description)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('organisationDashboard'))
    else:
        notifications=showNotifications(session['lid'])
        eventid=''
        domains=['Artificial Intelligence','Web Developement', 'Machine Learning','Deep Learning','Block Chain','IOE / IOT','Embedded System','Raspberry Pi','Mechanical Robotics','Power Electronics','Antenna','Android','Cloud Computing','Big Data','VLSI','Image Processing','RPA','Cyber Security','Data mining','Industry 4.0','Information Security','Computer Networking','Data Science','Neural Network','Software Engineering']
        if session.get("eid") == None:
            event={}
        return render_template('Add_Event.html', domains=domains, notifications=notifications, event=event)
            



@app.route('/orgProfile/<lid>',methods=['POST','GET'])
def orgprofile(lid):
    if request.method == "POST":
        if request.form.get('changeImg')=='changeImg':
            profileImage = request.files['profileImage']
            filename = secure_filename(profileImage.filename)
            destination= create_path_profile(filename, session['lid'])
            profileImage.save(destination)
            db.session.query(Orgdata).filter(Orgdata.lid == lid).update({'profile_photo': destination[destination.index('o_'):]})
            db.session.commit()
            db.session.query(Event).filter(Event.lid == lid).update({'orgImg': destination[destination.index('o_'):]})
            db.session.commit()
        if request.form.get('changeBanner')=='changeBanner':
            profileImage = request.files['profileBanner']
            filename = secure_filename(profileImage.filename)
            destination= create_path_banner(filename, session['lid'])
            profileImage.save(destination)
            db.session.query(Orgdata).filter(Orgdata.lid == lid).update({'cover_photo': destination[destination.index('o_'):]})
            db.session.commit()
        if request.form.get('update')=='update':
            name=request.form.get('name')
            institute=request.form.get('institute')
            phoneNo=request.form.get('phoneNo')
            linkedin=request.form.get('linkedin')
            description=request.form.get('description')
            db.session.query(Orgdata).filter(Orgdata.lid == lid).update({'name': name, 'institute':institute, 'phoneNo': phoneNo, 'linkedin':linkedin, 'description':description})
            db.session.commit()
    org = Orgdata.query.filter_by(lid=session['lid']).first()
    notifications=showNotifications(session['lid'])
    return render_template('orgprofilePage.html',org=org, notifications=notifications)

@app.route('/viewOrgProfile/<lid>',methods=['POST','GET'])
def viewOrgProfile(lid):
    if request.form.get('report')=='report':
        description=request.form.get('description')
        report.send_mail('phoenixatsih@gmail.com','uhyhrxcaadzjhomi', 'phoenixatsih@gmail.com',session['lid'], lid, description)
        return redirect(url_for('clientDashboard'))
    org=Orgdata.query.filter_by(lid=lid).first()
    events=upcomingEventsOrg(lid)
    notifications=showNotifications(session['lid'])
    return render_template('viewOrgProfile.html',org=org,events=events, notifications=notifications)

# Fetch the Checkout Session to display the JSON result on the success page
@app.route('/checkout-session', methods=['GET'])
def get_checkout_session():
    id = request.args.get('sessionId')
    checkout_session = stripe.checkout.Session.retrieve(id)
    return jsonify(checkout_session)


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    domain_url = os.getenv('DOMAIN')
    #print(domain_url)
    # price=request.form.get('price')
    if fees=='0':
        rid=createIdRegisteration(session['lid'],eventid)
        new_entry=Registeration(rid=rid,lid=session['lid'],eid=eventid)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('clientDashboard'))
        
    try:
        #print(price)
        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain_url + '/canceled.html',
            mode='payment',
            # automatic_tax={'enabled': True},
            line_items=[{
                'price': price,
                'quantity': 1,
            }]
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/success', methods=['GET'])
def success():
    rid=createIdRegisteration(session['lid'],eventid)
    new_entry=Registeration(rid=rid,lid=session['lid'],eid=eventid)
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for('clientDashboard'))

@app.route('/webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    print('event ' + event_type)

    if event_type == 'checkout.session.completed':
        print('🔔 Payment succeeded!')
        
    return jsonify({'status': 'success'})


@app.route('/profile/<lid>',methods=['POST','GET'])
def profile(lid):
    if request.method == "POST":
        if request.form.get('changeImg')=='changeImg':
            profileImage = request.files['profileImage']
            filename = secure_filename(profileImage.filename)
            destination= create_path_profile(filename, session['lid'])
            profileImage.save(destination)
            db.session.query(Client).filter(Client.lid == lid).update({'profile_photo': destination[destination.index('u_'):]})
            db.session.commit()
        elif request.form.get('changeBanner')=='changeBanner':
            profileImage = request.files['profileBanner']
            filename = secure_filename(profileImage.filename)
            destination= create_path_banner(filename, session['lid'])
            profileImage.save(destination)
            db.session.query(Client).filter(Client.lid == lid).update({'cover_photo': destination[destination.index('u_'):]})
            db.session.commit()
        elif request.form.get('update')=='update':
            name=request.form.get('name')
            occupation=request.form.get('occupation')
            institute=request.form.get('institute')
            phoneNo=request.form.get('phoneNo')
            linkedin=request.form.get('linkedin')
            gender=request.form.get('gender')
            description=request.form.get('description')
            db.session.query(Client).filter(Client.lid == lid).update({'name': name,'gender': gender, 'occupation':occupation, 'institute':institute, 'phoneNo': phoneNo, 'linkedin':linkedin, 'description':description})
            db.session.commit()
        else:
            skill=request.form.get('skill')
            new_entry=ClientInterest(lid=lid, interest=skill)
            db.session.add(new_entry)
            db.session.commit()
    skills= ClientInterest.query.filter_by(lid=lid).all()
    client = Client.query.filter_by(lid=session['lid']).first()
    domains=['Artificial Intelligence','Web Developement','Computer Science', 'Machine Learning','Deep Learning','Block Chain','IOE / IOT','Embedded System','Raspberry Pi','Mechanical Robotics','Power Electronics','Antenna','Android','Cloud Computing','Big Data','VLSI','Image Processing','RPA','Cyber Security','Data mining','Industry 4.0','Information Security','Computer Networking','Data Science','Neural Network','Software Engineering']
    notifications=showNotifications(session['lid'])
    return render_template('profilePage.html',client=client, domains=domains, skills=skills, notifications=notifications)


@app.route('/take_image', methods=['POST','GET'])
def take_image():
    print('hi')
    profileImage = request.files['profileImage']
    filename = secure_filename(profileImage.filename)
    destination= create_path_profile(filename, session['lid'])
    profileImage.save(destination)
    db.session.query(Client).filter(Client.lid == session['lid']).update({'profile_photo': destination[destination.index('u_'):]})
    db.session.commit()
    return 

@app.route('/report/<eid>',methods=['POST','GET'])
def report(eid):
    event=db.session.query(Event).filter(Event.eid==eid).first()
    org=db.session.query(Orgdata).filter(Orgdata.lid==event.lid).first()
    registered = Registeration.query.filter_by(eid=event.eid).count()
    regs=db.session.query(Registeration.lid).filter(Registeration.eid==event.eid).all()
    gender=[]
    institute=[]
    gender=db.session.query(Client.gender, func.count(Client.gender)).filter(db.session.query(Registeration.id).filter(Registeration.eid==eid and Registeration.lid==Client.lid).first() is not None).group_by(Client.gender).all()
    institute=db.session.query(Client.institute, func.count(Client.institute)).filter(db.session.query(Registeration.id).filter(Registeration.eid==eid and Registeration.lid==Client.lid).first() is not None).group_by(Client.institute).all()
    q1=db.session.query(Feedback.q1, func.count(Feedback.q1)).filter(Feedback.eid==event.eid).group_by(Feedback.q1).all()
    q2=db.session.query(Feedback.q2, func.count(Feedback.q2)).filter(Feedback.eid==event.eid).group_by(Feedback.q2).all()
    q3=db.session.query(Feedback.q3, func.count(Feedback.q3)).filter(Feedback.eid==event.eid).group_by(Feedback.q3).all()
    q4=db.session.query(Feedback.q4, func.count(Feedback.q4)).filter(Feedback.eid==event.eid).group_by(Feedback.q4).all()
    q5=db.session.query(Feedback.q5, func.count(Feedback.q5)).filter(Feedback.eid==event.eid).group_by(Feedback.q5).all()
    Q1=[0,0,0,0,0]
    Q2=[0,0,0,0,0]
    Q3=[0,0,0,0,0]
    Q4=[0,0,0,0,0]
    Q5=[0,0,0,0,0]
    for i in q1:
        Q1[i[0]-1]=i[-1]
    for i in q2:
        Q2[i[0]-1]=i[-1]
    for i in q3:
        Q3[i[0]-1]=i[-1]
    for i in q4:
        Q4[i[0]-1]=i[-1]
    for i in q5:
        Q5[i[0]-1]=i[-1]

    print(gender)
    glabels = [row[0] for row in gender]
    gvalues = [row[1] for row in gender]

    ilabels = [row[0] for row in institute]
    ivalues = [row[1] for row in institute]
    print(glabels, gvalues)
    print(ilabels, ivalues)
    if len(gvalues)==1:
        gvalues.append(0)
    return render_template('report.html',event=event,org=org,summary=summary, registered=registered,Q1=Q1, Q2=Q2, Q3=Q3, Q4=Q4, Q5=Q5, glabels= glabels, gvalues=gvalues, ilabels=ilabels, ivalues=ivalues)

    # rendered= render_template('report.html',event=event,org=org, registered=registered,Q1=Q1, Q2=Q2, Q3=Q3, Q4=Q4, Q5=Q5)
    # config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    # pdf=pdfkit.from_string(rendered,False, configuration=config, options={"enable-local-file-access": ""})
    # response = make_response(pdf)
    # response.headers['content-Type']='application/pdf'
    # response.headers['content-Disposition']='inline; filename='+eid+'.pdf'
    # return response
    return render_template('report.html',event=event,org=org, registered=registered,Q1=Q1, Q2=Q2, Q3=Q3, Q4=Q4, Q5=Q5)

@app.route('/search',methods=['POST','GET'])
def search():
    exevents=knowafest()
    #print(type(exevents))
    natVenue=""
    if request.method=="POST":
        domain=request.form.get('domain')
        location=request.form.get('location')
        date=request.form.get('date')
        venue=request.form.getlist('venue')
        #print(venue)
        etype=request.form.get('etype')
        money=request.form.get('money')
        free=request.form.get('free')
        if free=='free':
            money=0
        lst=[]
        if 'national' in venue:
            natVenue="India"
        elif 'international' in venue:
            natVenue=""
        if 'online' in venue:
            natVenue=""
        for events in exevents:
            if events.name.__contains__(etype) and events.detail.__contains__(domain) and events.loc.__contains__(location) and events.loc.__contains__(natVenue) :
                lst=lst+[events]
        # for l in lst:
        #     print(l.detail)
        return render_template('searchPage.html',notifications=showNotifications(session['lid']),exevents=lst)
    return render_template('searchPage.html',notifications=showNotifications(session['lid']),exevents=exevents)

@app.route('/modify_search',methods=['POST','GET'])
def modify_search():
    exevents=knowafest()
    natVenue=""
    if request.method=="POST":
        domain=request.form.get('domain')
        location=request.form.get('location')
        date=request.form.get('date')
        venue=request.form.getlist('venue')
        #print(venue)
        etype=request.form.get('type')
        money=request.form.get('money')
        free=request.form.get('free')
        if free=='free':
            money=0
        lst=[]
        if 'national' in venue:
            natVenue="India"
        elif 'international' in venue:
            natVenue=""
        if 'online' in venue:
            natVenue=""
        for events in exevents:
            if events.detail.__contanis__(etype) and events.detail.__contains__(domain) and events.loc.__contains__(location) and events.loc.__contains__(natVenue) :
                lst=lst+[events]
        # for l in lst:
        #     print(l.detail)
        return redirect('/search')
    return redirect('/search')



@app.route('/logout')
def logout():
    session.pop('name',None)
    session.pop('email',None)
    session.pop('role',None)
    session.pop('lid',None)
    return redirect('/')
#####Extra Functions######

#Function to generate login id
def createIdLogin(role,email):
    if role == 'user':
        id = 'u_'+email[:email.index('@')]
    else:
        id = 'o_'+email[:email.index('@')]
    while Login.query.filter_by(id=id).first():
        id=id+'0'
    return id

#Function to generate event id
def createIdEvent(name):
    ts = time.time()
    id=session['lid']+name+str(ts)
    return id

#Function to generate file to save backgroud images of event
def create_path(filename, eid):
    new_filename=eid+'bg'+filename[filename.index("."):]
    target = os.path.join(APP_ROOT,'static/images/')
    location = "events/".join([target, new_filename])
    return location

#Function to generate file to save backgroud images of event
def create_path_profile(filename, lid):
    new_filename=lid+'profile'+filename[filename.index("."):]
    target = os.path.join(APP_ROOT,'static/images/')
    location = "profile/".join([target, new_filename])
    return location

#Function to generate file to save backgroud images of event
def create_path_banner(filename, lid):
    new_filename=lid+'banner'+filename[filename.index("."):]
    target = os.path.join(APP_ROOT,'static/images/')
    location = "profile/".join([target, new_filename])
    return location

#Function to generate path for report img
def create_path_report(filename):
    new_filename='img1'+filename[filename.index("."):]
    target = os.path.join(APP_ROOT,'static/images/')
    location = "report/".join([target, new_filename])
    return location

#Function to generate file to save backgroud images of event
def create_path_speaker(filename, eid, speakerno):
    new_filename=eid+'speaker'+str(speakerno)+filename[filename.index("."):]
    target = os.path.join(APP_ROOT,'static/images/')
    location = "events/".join([target, new_filename])
    return location

#Function to filter upcoming events and discard completed events
def upcomingEvents():
    events = Event.query.all()
    e = []
    for event in events:
        # print(event.date[0:10])
        if event.date=='':
            continue
        date_format = "%Y-%m-%d"
        a = datetime.strptime(event.regLastDate[0:10], date_format)
        b = datetime.utcnow()
        delta = b - a
        if delta.days<=0:

            if db.session.query(ClientInterest.id).filter_by(interest=event.domain).first() is not None:
                e.insert(0,event)
            else:
                e.append(event)
    return e

def upcomingEventsOrg(lid):
    events = Event.query.filter_by(lid=lid).all()
    e = []
    for event in events:
        # print(event.date[0:10])
        try:
            date_format = "%Y-%m-%d"
            a = datetime.strptime(event.date[0:10], date_format)
            b = datetime.utcnow()
            delta = b - a
            if delta.days<=0:
                e.append(event)
        except:
            pass
    return e 

#Function to return registered upcoming events
def registeredupcomingEvents(lid):
    registered = Registeration.query.filter_by(lid=lid).all()
    r={}
    o={}
    l=[]
    for i in registered:
        temp=Event.query.filter_by(eid=i.eid).first()
        if temp==None:
            continue
        date_format = "%Y-%m-%d"
        a = datetime.strptime(temp.date[0:10], date_format)
        b = datetime.utcnow()
        delta = b - a
        if delta.days<0:
            r[i]=temp
            exists = db.session.query(Notification.id).filter_by(eid=temp.eid).first() is not None
            if exists:
                db.session.query(Notification).filter(Notification.eid == temp.eid).update({'message': str(abs(delta.days))+' Days to go for '+temp.name})
                db.session.commit()
            else:
                new_entry=Notification(lid=i.lid, eid=temp.eid, message=str(abs(delta.days))+' Days to go for '+temp.name)
                db.session.add(new_entry)
                db.session.commit()
        if delta.days==0:
            o[i]=temp
            exists = db.session.query(Notification.id).filter_by(eid=temp.eid).first() is not None
            if exists:
                Notification.query.filter_by(eid=temp.eid).delete()
                db.session.commit()
    l.append(o)
    l.append(r)
    return l

#Function to return events for organisation side
def eventsOrg(lid):
    ongoing={}
    reg_open={}
    reg_close={}
    completed={}
    completed_sentcert={}
    events=Event.query.filter_by(lid=lid).all()
    for event in events:
        registered = Registeration.query.filter_by(eid=event.eid).count()
        print(event.date)
        if event.date=='':
            continue
        date_format = "%Y-%m-%d"
        a = datetime.strptime(event.date[0:10], date_format)
        b = datetime.utcnow()
        delta = b - a
        if delta.days<0:
            c = datetime.strptime(event.regLastDate[0:10], date_format)
            delta2=b-c
            if delta2.days>=0:
                reg_close[event]=registered
            else:
                reg_open[event]=registered
        elif delta.days==0:
            ongoing[event]=registered
        else:
            completed[event]={}
            completed_sentcert[event]={}
            completed[event]['count']=registered
            completed_sentcert[event]['count']=registered
            reg=Registeration.query.filter_by(eid=event.eid).all()
            individual=[]
            for r in reg:
                temp=Client.query.filter_by(lid=r.lid).first().as_dict()
                individual.append(temp)
        #  print(individual)
            completed[event]['individual']=individual
            completed_sentcert[event]['individual']=individual
            #####you hv to write if statement to check if certificates are sent or not#####
            
    final={}
    final['ongoing']=ongoing
    final['reg_open']=reg_open
    final['reg_close']=reg_close
    final['completed']=completed
    final['completed_sentcert']=completed_sentcert
    return(final)


#Function to generate registeration id
def createIdRegisteration(lid,eid):
    ts = time.time()
    id=lid+eid+str(ts)
    return id


#Function to send feedback links to all clients
def send_feedback_link(eid):
    reg=db.session.query(Registeration).filter_by(eid=eid).all()
    for r in reg:
        user=db.session.query(Client).filter_by(lid=r.lid).first()
        event=db.session.query(Event.name).filter_by(eid=eid).first()
        print("mail sent to "+user.name+user.email)
        link=url_for('feedback',lid=user.lid,eid=eid, _external=True)
        feedbackmail.send_mail('phoenixatsih@gmail.com','uhyhrxcaadzjhomi', user.email, user.name, event[0], link)

#Function to push notification when org sends certificates
def push_notification(eid):
    reg=db.session.query(Registeration).filter_by(eid=eid).all()
    for r in reg:
        name=db.session.query(Event.name).filter_by(eid=eid).first()
        new_entry=Notification(lid=r.lid, eid=eid, message=name[0]+' Certicate Received')
        db.session.add(new_entry)
        db.session.commit()

def push_notification_org(lid):
    events=Event.query.filter_by(lid=lid).all()
    for event in events:
        if event.date=='':
            continue
        date_format = "%Y-%m-%d"
        a = datetime.strptime(event.date[0:10], date_format)
        b = datetime.utcnow()
        delta = b - a
        exists = db.session.query(Notification.id).filter_by(eid=event.eid).first() is not None
        if delta.days>=1 and not exists:
            exists = db.session.query(Feedback.id).filter_by(eid=event.eid).first() is not None
            if exists:
                pass
            else:
                new_entry=Notification(lid=lid, eid=event.eid, message='Successfully completed the event '+ event.name +'! Send feedback form.')
                db.session.add(new_entry)
                db.session.commit()
    

#Function to show notifications in client side
def showNotifications(lid):
    notifications=db.session.query(Notification).filter_by(lid=lid).all()
    n={}
    for noti in notifications:
        org=db.session.query(Orgdata).filter_by(lid=db.session.query(Event.lid).filter_by(eid=noti.eid).first()[0]).first()
        n[noti]=org
    return n

#Function to get courses 
def getCourses(lid):
    interests=db.session.query(ClientInterest).filter_by(lid=lid).all()
    courses=[]
    for interest in interests:
        courses.extend(scrapallcourse(interest.interest))
    if len(courses)==0:
        courses.extend(scrapallcourse('Computer Science'))
        courses.extend(scrapallcourse('Machine Learning'))
    return courses



#Function to send cancel event mails
def send_cancel_email(eid,name,reason):
    reg=db.session.query(Registeration).filter_by(eid=eid).all()
    registered = Registeration.query.filter_by(eid).count()
    if registered!=0:
        for r in reg:
            client=db.session.query(Client).filter_by(lid=r.lid).first()
            cancelEvent.send_mail('phoenixatsih@gmail.com','uhyhrxcaadzjhomi', client.email, name, reason)
        Registeration.query.filter_by(eid=r.eid).delete()
        db.session.commit()
        Notification.query.filter_by(eid=r.eid).delete()
        db.session.commit()


db.create_all()
