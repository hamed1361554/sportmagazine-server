"""
Created on Sep 12, 2016

@author: Hamed Zekri
"""

from deltapy.application.decorators import register
from deltapy.utils.concurrent import run_in_thread

from server.wsdl.security_manager import FlaskWebServicesManager, app
from server.wsdl import SERVER_FLASK_WEB_SERVICES_PROVIDER_MANAGER


@register(SERVER_FLASK_WEB_SERVICES_PROVIDER_MANAGER)
class FlaskWebServicesManagerComponent(FlaskWebServicesManager):
    """
    Flask Web Services Manager Component
    """

    def __init__(self):
        """
        Inits!
        """

        FlaskWebServicesManager.__init__(self)

        #app.run(debug=True, threaded=True, use_reloader=False)
        run_in_thread(app.run, debug=True, threaded=True, use_reloader=False)
