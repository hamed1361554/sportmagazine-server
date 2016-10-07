"""
Created on Sep 9, 2016

@author: Hamed Zekri
"""

from datetime import datetime

from deltapy.security.authentication.authenticator import BaseAuthenticator, UserStatusEnum

import deltapy.unique_id.services as unique_id_services
import deltapy.security.session.services as session_services
import deltapy.transaction.services as transaction_services

from server.model import UserHistoryEntity
from server.utils import verify_sha512


class Authenticator(BaseAuthenticator):
    """
    Authenticator
    """

    def __init__(self):
        """
        Initializes authenticator.
        """

        BaseAuthenticator.__init__(self)

    def _check_password_(self, password, user, **options):
        """
        Checks user password and return True if password is correct.

        @param password: given password
        @param user: user information

        @return: bool
        """

        result = verify_sha512(password, user.user_password)

        if not result:
            self._write_user_log(user,
                                 UserStatusEnum.WRONG_PASSWORD,
                                 message="User [{0}] entered wrong password [{1}]".format(user.user_id, password))

        return result

    def _write_user_log(self, user, status, **options):
        """
        Writes down user activity log.

        @param dict user: user info
        @param int status: user status
        """

        if user is None:
            return

        with transaction_services.begin_root():
            store = transaction_services.get_current_transaction_store()

            history = UserHistoryEntity()
            history.id = unicode(unique_id_services.get_id("uuid"))
            history.user_id = user.id
            current_session = session_services.get_current_session()
            if current_session is not None:
                history.user_history_client_ip = current_session.get_client_request().ip
            history.user_history_date = datetime.now()
            history.user_history_status = status
            history.user_history_message = unicode(options.get("message"))
            store.add(history)