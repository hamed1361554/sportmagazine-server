"""
Created on Sep 9, 2016

@author: Hamed Zekri
"""

from deltapy.security.authentication.authenticator import BaseAuthenticator


class Authenticator(BaseAuthenticator):
    """

    """

    def __init__(self):
        BaseAuthenticator.__init__(self)

    def _check_password_(self, password, user, **options):
        '''
        Checks user password and return True if password is correct.

        @param password: given password
        @param user: user information
        @param **options:

        @return: bool
        '''

        return True