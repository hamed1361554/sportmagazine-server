"""
Created on Dec 2, 2016

@author: Hamed Zekri
"""

from flask import request, abort, jsonify, json
from deltapy.core import DeltaObject
from server.wsdl import flask_app, pyro_server


class FlaskWebServicesInvoiceManager(DeltaObject):
    """
    Flask Web Services Invoice Manager
    """

    @staticmethod
    def check_service_requirements(request_keys):
        '''
        Checks service request minimal requirements.
        '''

        if not request.json:
            abort(400)

        for expected in request_keys:
            if expected not in request.json:
                abort(400)

    @staticmethod
    def get_service_options():
        '''
        Returns service options.
        '''

        options = {}
        if 'options' in request.json:
            options = request.json.get("options")
            if len(options) > 0:
                options = json.loads(options)

        return options

    @staticmethod
    @flask_app.route('/invoice/register', methods=["POST"])
    def register():
        """
        Registers invoice!
        """

        FlaskWebServicesInvoiceManager.check_service_requirements(['ticket', 'user_name', 'invoice_items'])

        invoice = \
            pyro_server.execute_ex(request.json['ticket'], request.json['user_name'], 'server.invoices.register', {},
                                   request.json['invoice_items'])

        invoice = invoice.get('result')
        return jsonify(invoice.get('invoice_id'))