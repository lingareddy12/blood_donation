

from email.message import EmailMessage 
import ssl 
import smtplib
sender="lingareddydanda098@gmail.com" 
password="zhdegessvjtvsjho" 

receiver="20131A0444@gvpce.ac.in"
subject="Test mail"
body=""" idey best mowa pani chestundi ga """
em=EmailMessage()
em['From']=sender
em['To']=receiver
em['subject']=subject
em.set_content(body) 

context=ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
    smtp.login(sender,password)
    smtp.sendmail(sender,receiver,em.as_string())
    