"""
Created on Sep 12, 2016

@author: Hamed Zekri
"""

from flask import Flask

from deltapy.packaging.package import Package
import deltapy.application.services as services
from server.utils.json_encoder import CustomJsonEncoder

from server.wsdl.service_manager import PyroServer


SERVER_FLASK_WEB_SERVICES_PROVIDER_MANAGER = 'server.flask.web_services.provider.manager'
SERVER_FLASK_WEB_SERVICES_SECURITY_MANAGER = 'server.flask.web_services.security.manager'
SERVER_FLASK_WEB_SERVICES_PRODUCTS_MANAGER = 'server.flask.web_services.products.manager'
SERVER_FLASK_WEB_SERVICES_INVOICE_MANAGER = 'server.flask.web_services.invoice.manager'
SUCCESS_RESPONSE = "SUCCESSFUL"
FAILED_RESPONSE = "FAILED"

pyro_server = PyroServer("127.0.0.1", "6082")
flask_app = Flask("flask-{0}".format(services.get_name()))
flask_app.json_encoder = CustomJsonEncoder


class FlaskWebServicesPackage(Package):
    """
    Flask Web Services Package
    """