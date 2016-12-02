"""
Created on Sep 12, 2016

@author: Hamed Zekri
"""

from deltapy.application.decorators import register
from deltapy.core import DeltaObject
from deltapy.utils.concurrent import run_in_thread

from server.wsdl import flask_app
from server.wsdl import SERVER_FLASK_WEB_SERVICES_PROVIDER_MANAGER, \
    SERVER_FLASK_WEB_SERVICES_PRODUCTS_MANAGER, \
    SERVER_FLASK_WEB_SERVICES_SECURITY_MANAGER, \
    SERVER_FLASK_WEB_SERVICES_INVOICE_MANAGER
from server.wsdl.product_manager import FlaskWebServicesProductsManager
from server.wsdl.security_manager import FlaskWebServicesSecurityManager
from server.wsdl.invoice_manager import FlaskWebServicesInvoiceManager


@register(SERVER_FLASK_WEB_SERVICES_PROVIDER_MANAGER)
class FlaskWebServicesManagerComponent(DeltaObject):
    """
    Flask Web Services Manager Component
    """

    def __init__(self):
        """
        Inits!
        """

        DeltaObject.__init__(self)

        #app.run(debug=True, threaded=True, use_reloader=False)
        run_in_thread(flask_app.run, debug=False, threaded=True, use_reloader=False, host='0.0.0.0', port=5001)


@register(SERVER_FLASK_WEB_SERVICES_SECURITY_MANAGER)
class FlaskWebServicesSecurityManagerComponent(FlaskWebServicesSecurityManager):
    """
    Flask Web Services Security Manager Component
    """


@register(SERVER_FLASK_WEB_SERVICES_PRODUCTS_MANAGER)
class FlaskWebServicesProductsManagerComponent(FlaskWebServicesProductsManager):
    """
    Flask Web Services Products Manager Component
    """

@register(SERVER_FLASK_WEB_SERVICES_INVOICE_MANAGER)
class FlaskWebServicesInvoiceManagerComponent(FlaskWebServicesInvoiceManager):
    """
    Flask Web Services Invoice Manager Component
    """
