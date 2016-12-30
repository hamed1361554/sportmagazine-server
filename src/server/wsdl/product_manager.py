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
    @flask_app.route('/product/create', methods=["POST"])
    def create_product():
        """
        Creates product!
        """

        FlaskWebServicesProductsManager.check_service_requirements(['ticket', 'user_name', 'name', 'price',
                                                                    'category', 'colors', 'sizes', 'brands'])
        options = FlaskWebServicesProductsManager.get_service_options()

        if 'status' in request.json:
            options['status'] = request.json['status']
        if 'counter' in request.json:
            options['counter'] = request.json['counter']
        if 'age_category' in request.json:
            options['age_category'] = request.json['age_category']
        if 'gender' in request.json:
            options['gender'] = request.json['gender']
        if 'comment' in request.json:
            options['comment'] = request.json['comment']
        if 'image' in request.json:
            options['image'] = request.json['image']
        if 'wholesale_type' in request.json:
            options['wholesale_type'] = request.json['wholesale_type']

        product = \
            pyro_server.execute_ex(request.json['ticket'], request.json['user_name'], 'server.products.create', {},
                                   request.json['name'], request.json['price'], request.json['category'],
                                   request.json['colors'].split(','), request.json['sizes'].split(','),
                                   request.json['brands'].split(','), **options)

        product = product.get('result')
        product['product_price'] = None
        return jsonify({"name": product.get("product_name"),
                        "comment": product.get("product_comment")})

    @staticmethod
    @flask_app.route('/product/update', methods=["POST"])
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
        if 'brands' in request.json:
            options['brands'] = request.json['brands']
        if 'counter' in request.json:
            options['counter'] = request.json['counter']
        if 'age_category' in request.json:
            options['age_category'] = request.json['age_category']
        if 'gender' in request.json:
            options['gender'] = request.json['gender']
        if 'comment' in request.json:
            options['comment'] = request.json['comment']

        product = \
            pyro_server.execute_ex(request.json['ticket'], request.json['user_name'], 'server.products.update', {},
                                   request.json['id'], **options)

        return jsonify(product)

    @staticmethod
    @flask_app.route('/products/get/<string:id>', methods=["GET"])
    def get_product(id):
        """
        Gets product!
        """

        FlaskWebServicesProductsManager.check_service_requirements(['ticket', 'user_name'])

        product = \
            pyro_server.execute_ex(request.json['ticket'], request.json['user_name'], 'server.products.get', {}, id)

        return jsonify(product)

    @staticmethod
    @flask_app.route('/product/get/<string:name>', methods=["GET"])
    def get_product_by_name(name):
        """
        Gets product!
        """

        FlaskWebServicesProductsManager.check_service_requirements(['ticket', 'user_name'])

        product = \
            pyro_server.execute_ex(request.json['ticket'], request.json['user_name'], 'server.products.get.by_name', {}, name)

        return jsonify(product)

    @staticmethod
    @flask_app.route('/product/find', methods=["POST"])
    def find_products():
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
        if 'size' in request.json:
            options['size'] = request.json['size']
        if 'brand' in request.json:
            options['brand'] = request.json['brand']
        if 'categories' in request.json:
            options['categories'] = request.json['categories']
        if 'age_categories' in request.json:
            options['age_categories'] = request.json['age_categories']
        if 'gender' in request.json:
            options['gender'] = request.json['gender']
        if 'include_out_of_stock' in request.json:
            options['include_out_of_stock'] = request.json['include_out_of_stock']
        if 'wholesale_type' in request.json:
            options['wholesale_type'] = request.json['wholesale_type']
        if 'just_current_user' in request.json:
            options['just_current_user'] = request.json['just_current_user']
        if '__offset__' in request.json:
            options['__offset__'] = request.json['__offset__']
        if '__limit__' in request.json:
            options['__limit__'] = request.json['__limit__']

        products = \
            pyro_server.execute_ex(request.json['ticket'], request.json['user_name'], 'server.products.find', {},
                                   **options)

        products = products.get('result')
        return jsonify([{"id": p.get("product_id"),
                         "name": p.get("product_name"),
                         "category": p.get("product_category"),
                         "image": p.get("product_image"),
                         "age_category": p.get("product_age_category"),
                         "comment": p.get("product_comment"),
                         "creation_date": p.get("product_creation_date"),
                         "price": float(p.get("product_price")),
                         "gender": p.get("product_gender"),
                         "colors": p.get("product_colors"),
                         "sizes": p.get("product_sizes"),
                         "brands": p.get("product_brands")} for p in products])

    @staticmethod
    @flask_app.route('/product/history/find', methods=["POST"])
    def find_history():
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