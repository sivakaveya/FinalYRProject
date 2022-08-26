from cgitb import text
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from unicodedata import name
class report:
    def send_mail(sender_address,sender_pass,receiver_address,user_id, org_id, desc):
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Phoenix Alert'
        mail_content='''Dear Admin,\nThe user with user id: '''+user_id+''' has reported organisation '''+org_id+''' for:\n'''+desc
        message.attach(MIMEText(mail_content, 'plain'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()