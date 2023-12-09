# import pywhatkit
 
 
# pywhatkit.sendwhatmsg("+919949590838", 
#                       "python automated message generated ", 
#                       11,2)


from email.message import EmailMessage 
import ssl 
import smtplib
sender="lingareddydanda098@gmail.com" 
password="ixzh ujjb eydh uzgz" 


def send_mail(receiver,subject,body):
    em=EmailMessage()
    em['From']=sender
    em['To']=receiver
    em['subject']=subject
    em.set_content(body) 

    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(sender,password)
        smtp.sendmail(sender,receiver,em.as_string())

