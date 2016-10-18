"""
Created on 11/25/15

@author: Ehsan F.J
"""

import signal

from deltapy.core import DeltaObject
from deltapy.request_processor.manager import TimeoutException
from deltapy.security.session.services import get_current_session


class RequestProcessorHelper(DeltaObject):
    """

    """

    def set_request_timeout(self, timeout):
        """
        Sets request timeout in current thread.
        """

        # Considering timeout if it is required
        if timeout is not None and timeout > 0:
            def handler(signum, frame):
                # Getting client request
                client_request = get_current_session().get_client_request()
                message = _('Request timeout [{0} second(s)] reached for request [{1}].')
                raise TimeoutException(message.format(timeout, client_request))
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(timeout)