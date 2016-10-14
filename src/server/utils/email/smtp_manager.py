"""
Created on Sep 9, 2016

@author: Hamed Zekri
"""

import smtplib

from deltapy.core import DeltaObject


class SmtpEmailManager(DeltaObject):
    '''
    Smtp Email Manager
    '''

    def __init__(self):
        DeltaObject.__init__(self)

        self._messages = {'activation_email':
                            """
                            From: Sport Magazine <info@faportmagazine.com>
                            To: {full_name} <{email}>
                            MIME-Version: 1.0
                            Content-type: text/html
                            Subject: User Activation Email (Sports Magazine)

                            <b>Activation URL (Just Click)</b>
                            <h1>{url}</h1>
                            """
                          }

    def send_activation_email(self, full_name, email, url):
        '''
        Sends activation email via smtp protocol.

        :param full_name:
        :param email:
        :param url:
        '''

        sender = 'info@faportmagazine.com'
        receivers = [email]

        smtpServer = smtplib.SMTP()
        smtpServer.connect()
        smtpServer.sendmail(sender, receivers, self._messages['activation_email'].format(full_name=full_name,
                                                                                         email=email,
                                                                                         url=url))
