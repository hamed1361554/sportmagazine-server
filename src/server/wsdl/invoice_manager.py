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

    @staticmethod
    @flask_app.route('/invoice/get/<string:id>', methods=["GET"])
    def get_invoice(id):
        """
        Gets product!
        """

        FlaskWebServicesInvoiceManager.check_service_requirements(['ticket', 'user_name'])

        invoice = \
            pyro_server.execute_ex(request.json['ticket'], request.json['user_name'], 'server.invoices.get', {}, id)

        return jsonify(invoice)

    @staticmethod
    @flask_app.route('/invoice/find', methods=["POST"])
    def find_invoices():
        """
        Finds products!
        """

        FlaskWebServicesInvoiceManager.check_service_requirements(['ticket', 'user_name'])
        options = FlaskWebServicesInvoiceManager.get_service_options()

        if 'from_invoice_date' in request.json:
            options['from_invoice_date'] = request.json['from_invoice_date']
        if 'to_invoice_date' in request.json:
            options['to_invoice_date'] = request.json['to_invoice_date']
        if '__offset__' in request.json:
            options['__offset__'] = request.json['__offset__']
        if '__limit__' in request.json:
            options['__limit__'] = request.json['__limit__']

        invoices = \
            pyro_server.execute_ex(request.json['ticket'], request.json['user_name'], 'server.invoices.find', {},
                                   **options)

        invoices = invoices.get('result')

        flat_invoices = []
        for invoice in invoices:
            flat_invoice = {"id": invoice.get("invoice_id"),
                            "date": invoice.get("invoice_date"),
                            "status": invoice.get("invoice_status"),
                            "consumer_user_id": invoice.get("invoice_consumer_user_id"),
                            "comment": invoice.get("invoice_comment"),
                            "total_price": invoice.get("total_invoce_price"),
                            "invoice_items": []}

            invoice_items = []
            for item in invoice.get("invoice_items"):
                invoice_item = {"id": item.get("item_id"),
                                "product_id": item.get("item_product_id"),
                                "price": item.get("item_price"),
                                "quantity": item.get("item_quantity"),
                                "row": item.get("item_row"),
                                "color": item.get("item_color"),
                                "size": item.get("item_size"),
                                "brand": item.get("item_brand")}

                p = item.get("product")
                product = {"id": p.get("product_id"),
                           "name": p.get("product_name"),
                           "category": p.get("product_category"),
                           "image": p.get("product_image"),
                           "age_category": p.get("product_age_category"),
                           "comment": p.get("product_comment"),
                           "creation_date": p.get("product_creation_date"),
                           "gender": p.get("product_gender")}

                invoice_item.update(product=product)
                invoice_items.append(invoice_item)

            flat_invoice.update(invoice_items=invoice_items)
            flat_invoices.append(flat_invoice)

        return jsonify(flat_invoices)
