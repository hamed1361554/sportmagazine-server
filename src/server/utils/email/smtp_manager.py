"""
Created on Sep 9, 2016

@author: Hamed Zekri
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email import Charset
from email.generator import Generator

from deltapy.core import DeltaObject


class SmtpEmailManager(DeltaObject):
    '''
    Smtp Email Manager
    '''

    def __init__(self):
        DeltaObject.__init__(self)

    def send_activation_email(self, full_name, email, url):
        '''
        Sends activation email via smtp protocol.

        :param full_name:
        :param email:
        :param url:
        '''

        # Example address data
        from_address = [u'Sport Magazine', 'mail.sportmagazine.ir']
        recipient = [unicode(full_name), email]
        subject = u'User Activation Email (Simaye Salem)'

        # Example body
        html = \
            u'<b>Activation URL (Just Click)</b><br\><h1><a href="{url}">Click Here To Activate ...</a></h1>'.format(url=url)

        # Default encoding mode set to Quoted Printable. Acts globally!
        Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "%s" % Header(subject, 'utf-8')
        # Only descriptive part of recipient and sender shall be encoded, not the email address
        msg['From'] = "\"%s\" <%s>" % (Header(from_address[0], 'utf-8'), from_address[1])
        msg['To'] = "\"%s\" <%s>" % (Header(recipient[0], 'utf-8'), recipient[1])

        # Attach both parts
        htmlpart = MIMEText(html, 'html', 'UTF-8')
        msg.attach(htmlpart)

        smtpServer = smtplib.SMTP()
        smtpServer.connect()
        smtpServer.sendmail(from_address[1], [recipient[1]], msg.as_string())
        smtpServer.quit()

    def send_change_password_email(self, full_name, email, change_code):
        '''
        Sends change password email via smtp protocol.

        :param full_name:
        :param email:
        :param change_code:
        '''
        return

        # Example address data
        from_address = [u'Sport Magazine', 'mail.sportmagazine.ir']
        recipient = [unicode(full_name), email]
        subject = u'User Change Password Email (Simaye Salem)'

        # Example body
        html = \
            u'<b>Change Password Code (Use this code to change password)</b><br\><h1>change_code</h1>'.format(change_code=change_code)

        # Default encoding mode set to Quoted Printable. Acts globally!
        Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "%s" % Header(subject, 'utf-8')
        # Only descriptive part of recipient and sender shall be encoded, not the email address
        msg['From'] = "\"%s\" <%s>" % (Header(from_address[0], 'utf-8'), from_address[1])
        msg['To'] = "\"%s\" <%s>" % (Header(recipient[0], 'utf-8'), recipient[1])

        # Attach both parts
        htmlpart = MIMEText(html, 'html', 'UTF-8')
        msg.attach(htmlpart)

        smtpServer = smtplib.SMTP()
        smtpServer.connect()
        smtpServer.sendmail(from_address[1], [recipient[1]], msg.as_string())
        smtpServer.quit()