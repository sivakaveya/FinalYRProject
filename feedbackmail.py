from cgitb import text
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from unicodedata import name
class feedbackmail:
    def send_mail(sender_address,sender_pass,receiver_address,name, event, link):
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Phoenix Alert| Feedback Link'
        mail_content='''Dear '''+name+''',\nYour presence in the event'''+event+''' was duly noted and your satisfaction means the most to us. Kindly feel free to fill the feedback form by clicking on the link given below.\n\n'''+link+'''\n\n Thank you\nRegards\nPhoenix Team'''
        message.attach(MIMEText(mail_content, 'plain'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()