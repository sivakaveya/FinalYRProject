from cgitb import text
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from unicodedata import name
class cancelEvent:
    def send_mail(sender_address,sender_pass,receiver_address,name,reason):
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Phoenix Alert| Cancellation of Event'
        mail_content='''Dear Customer,\nWe regret that the event you registered for:\n '''+name+''' has been cancelled by the organisation because of the following reason:\n'''+reason
        #The subject line
        # #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        #print('Mail Sent')

# m = mail()
# m.send_mail(sender_address='kaveya.sivaprakasam@vit.edu.in',sender_pass='appleeye123@', receiver_address='sivaaruna10@gmail.com',text='1234')
# m.send_mail('phoenixatsih@gmail.com','ikstao123@', 'sivaaruna10@gmail.com','1234')