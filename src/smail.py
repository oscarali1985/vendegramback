# import necessary packages

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


'''
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'vendegram@gmail.com',
	)
mail = Mail(app)

'''
def sendEmail(titulocorreo,nombre,correo,men):
    # create message object instance
    msg = MIMEMultipart()
    
    
    
    message = nombre+men+"n Thank you"
    
    # setup the parameters of the message
    password = os.environ.get('PASSWORD_EMAIL')
    msg['From'] = "vendegram@gmail.com"
    msg['To'] = correo
    msg['Subject'] = titulocorreo+" "+nombre
    
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    #msg.attach(MIMEText(message, 'html'))

    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    
    #depuracion
    server.set_debuglevel(1)


    # send the message via the server.
    logr = server.sendmail(msg['From'], msg['To'], msg.as_string())
    print(" Imprimiendo log")
    print (logr)

    server.quit()
    respuesta ="successfully sent email to %s:" % (msg['To'])
    return respuesta