# -*- coding: utf-8 -*-
#! /usr/bin/python
import os
import logging

logger = logging.getLogger(__name__)


#send to NetEase via twisted mail component
#Env  endpoint
#Dev  atom.corp.ebay.com
#Feature/Staging  mailhost.qa.ebay.com
#Prd  mx.vip.ebay.com
def sendeBay(message,subject,sender = 'ScriptAutoRun@atom.corp.ebay.com',recipients = ['kwang6@ebay.com','andy_wang_ke@163.com']):
    logger.log(logging.INFO,'start sending email reminder from eBay.')
    host='atom.corp.ebay.com'
    sendHtmlViasmtplib(message, subject, sender, recipients, host)



#twisted mail
def send(message, subject, sender, recipients, host):
    from email.mime.text import MIMEText
    from twisted.mail.smtp import sendmail
    #from twisted.internet import reactor
    """
    Send email to one or more addresses.
    """
    logger.info('mail send in progress...')
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    dfr = sendmail(host, sender, recipients, msg.as_string().encode('utf-8'))
    def success(r):
        logger.info('mail send successful...')
        #reactor.stop()
    def error(e):
        logger.info('email error:%s'% e)
        #reactor.stop()
    dfr.addCallback(success)
    dfr.addErrback(error)

    #reactor.run()


#smtplib mail
def sendViasmtplib(message,subject,sender,recipients,host):
    import smtplib

    # SERVER = "atom.corp.ebay.com"

    # FROM = "ScriptAutoRun@atom.corp.ebay.com"
    # TO = ["kwang6@ebay.com"] # must be a list

    # SUBJECT = "Hello!"

    # TEXT = "This message was sent with Python's smtplib."

    # Prepare actual message

    msg = """\
    From: %s\r\nTo: %s\r\nCC: %s\r\nSubject: %s\r\n\r\n%s""" % (sender, ", ".join(recipients),'andy_wang_ke@163.com', subject, message)

    # Send the mail

    server = smtplib.SMTP(host,25)
    server.sendmail(sender, recipients, msg)
    server.quit()
    logging.info('Send email via Python smtplib successfully');

#smptlib html mail
def sendHtmlViasmtplib(message,subject,sender,recipients,host):
    import smtplib

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['CC'] = 'andy_wang_ke@163.com'

    html="""\
    <html>
    <head></head>
    <body>
        <p>Hi!<br>
           How are you?<br>
           A brand new Day coming!<br>
           <b>%s</b>
        </p>
    </body>
    </html>
    """ % (message)

    part1=MIMEText(html,'html')
    msg.attach(part1)

    # Send the mail

    server = smtplib.SMTP(host,25)
    server.sendmail(sender, recipients, msg.as_string().encode('utf-8'))
    server.quit()
    logging.info('Send html email via Python smtplib successfully');

'''
if __name__ == '__main__':
    msg = 'This is the message body'
    subject = 'This is the message subjet'

    host = 'smtp3.xxx.com'
    sender = 'sender@xxx.com'
    recipients = ['recipient@xxx.com']

    log.startLogging(sys.stdout)
    send(msg, subject, sender, recipients, host)
'''
# if __name__=='__main__':
#     import smtplib

#     SERVER = "atom.corp.ebay.com"

#     FROM = "ScriptAutoRun@atom.corp.ebay.com"
#     TO = ["kwang6@ebay.com"] # must be a list

#     SUBJECT = "Hello!"

#     TEXT = "This message was sent with Python's smtplib."

#     # Prepare actual message

#     message = """\
#     From: %s
#     To: %s
#     Subject: %s

#     %s
#     """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

#     # Send the mail

#     server = smtplib.SMTP(SERVER)
#     server.sendmail(FROM, TO, message)
#     server.quit()
#     logging.info('send email succesful via Python smtplib');