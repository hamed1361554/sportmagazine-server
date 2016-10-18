"""
Created on Oct 18, 2016

@author: Hamed Zekri
"""

from flask import request, abort, jsonify, json

from deltapy.core import DeltaObject

from server.wsdl import flask_app, pyro_server


class FlaskWebServicesProductsManager(DeltaObject):
    """
    Flask Web Services Products Manager
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
    @flask_app.route('/products/create', methods=["POST"])
    def create():
        """
        Creates product!
        """

        FlaskWebServicesProductsManager.check_service_requirements(['ticket', 'user_name', 'name', 'price', 'category', 'colors', 'sizes'])
        options = FlaskWebServicesProductsManager.get_service_options()

        if 'status' in request.json:
            options['status'] = request.json['status']

        product = \
            pyro_server.execute_ex(request.json['ticket'], request.json['user_name'], 'server.products.create', {},
                                   request.json['name'], request.json['price'], request.json['category'],
                                   request.json['colors'], request.json['sizes'], **options)

        return jsonify(product)

    @staticmethod
    @flask_app.route('/products/update', methods=["POST"])
    def update():
        """
        Updates product!
        """

        FlaskWebServicesProductsManager.check_service_requirements(['ticket', 'user_name', 'id'])
        options = FlaskWebServicesProductsManager.get_service_options()

        if 'price' in request.json:
            options['price'] = request.json['price']
        if 'image_data' in request.json:
            options['image_data'] = request.json['image_data']
        if 'status' in request.json:
            options['status'] = request.json['status']
        if 'colors' in request.json:
            options['colors'] = request.json['colors']
        if 'sizes' in request.json:
            options['sizes'] = request.json['sizes']

        product = \
            pyro_server.execute_ex(request.json['ticket'], request.json['user_name'], 'server.products.update', {},
                                   request.json['id'], **options)

        return jsonify(product)

    @staticmethod
    @flask_app.route('/products/get/<string:id>', methods=["GET"])
    def get(id):
        """
        Gets product!
        """

        FlaskWebServicesProductsManager.check_service_requirements(['ticket', 'user_name'])

        product = \
            pyro_server.execute_ex(request.json['ticket'], request.json['user_name'], 'server.products.get', {}, id)

        return jsonify(product)

    @staticmethod
    @flask_app.route('/products/get/<string:name>', methods=["GET"])
    def get_by_name(name):
        """
        Gets product!
        """

        FlaskWebServicesProductsManager.check_service_requirements(['ticket', 'user_name'])

        product = \
            pyro_server.execute_ex(request.json['ticket'], request.json['user_name'], 'server.products.get.by_name', {}, name)

        return jsonify(product)

    @staticmethod
    @flask_app.route('/products/find/', methods=["GET"])
    def find():
        """
        Finds products!
        """

        FlaskWebServicesProductsManager.check_service_requirements(['ticket', 'user_name'])
        options = FlaskWebServicesProductsManager.get_service_options()

        if 'from_creation_date' in request.json:
            options['from_creation_date'] = request.json['from_creation_date']
        if 'to_creation_date' in request.json:
            options['to_creation_date'] = request.json['to_creation_date']
        if 'from_price' in request.json:
            options['from_price'] = request.json['from_price']
        if 'to_price' in request.json:
            options['to_price'] = request.json['to_price']
        if 'name' in request.json:
            options['name'] = request.json['name']
        if 'categories' in request.json:
            options['categories'] = request.json['categories']
        if 'include_out_of_stock' in request.json:
            options['include_out_of_stock'] = request.json['include_out_of_stock']

        products = \
            pyro_server.execute_ex(request.json['ticket'], request.json['user_name'], 'server.products.find', {})

        return jsonify(products)

    @staticmethod
    @flask_app.route('/products/history/find/', methods=["GET"])
    def find():
        """
        Finds products histories!
        """

        FlaskWebServicesProductsManager.check_service_requirements(['ticket', 'user_name'])
        options = FlaskWebServicesProductsManager.get_service_options()

        if 'from_edit_date' in request.json:
            options['from_edit_date'] = request.json['from_edit_date']
        if 'to_creation_date' in request.json:
            options['to_edit_date'] = request.json['to_edit_date']
        if 'from_price' in request.json:
            options['from_price'] = request.json['from_price']
        if 'to_price' in request.json:
            options['to_price'] = request.json['to_price']
        if 'name' in request.json:
            options['name'] = request.json['name']
        if 'categories' in request.json:
            options['categories'] = request.json['categories']
        if 'include_out_of_stock' in request.json:
            options['include_out_of_stock'] = request.json['include_out_of_stock']

        products = \
            pyro_server.execute_ex(request.json['ticket'], request.json['user_name'], 'server.products.history.find', {})

        return jsonify(products)