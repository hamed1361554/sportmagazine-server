"""
Created on Sep 12, 2016

@author: Hamed Zekri
"""

from flask import request, abort, jsonify, json

from deltapy.core import DeltaObject

from server.wsdl import SUCCESS_RESPONSE
from server.wsdl import flask_app, pyro_server
from server.utils.encryption import decrypt_aes, encrypt_aes


class FlaskWebServicesSecurityManager(DeltaObject):
    """
    Flask Web Services Security Manager
    """

    @staticmethod
    def check_user_name():
        '''
        Checks invalid user names.
        '''

        if request.json['user_name'].lower().strip() in ('admin', 'root', 'support'):
            abort(400)

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
    @flask_app.route("/login", methods=["POST"])
    def login():
        """
        Logins!
        """

        FlaskWebServicesSecurityManager.check_service_requirements(['user_name', 'password'])
        FlaskWebServicesSecurityManager.check_user_name()

        options = FlaskWebServicesSecurityManager.get_service_options()
        ticket = pyro_server.login(request.json['user_name'], request.json['password'], **options)
        return jsonify({"ticket": ticket})

    @staticmethod
    @flask_app.route('/signin', methods=["POST"])
    def signin():
        '''
        Sign in!
        '''

        FlaskWebServicesSecurityManager.check_service_requirements(['user_name', 'full_name', 'password'])
        FlaskWebServicesSecurityManager.check_user_name()

        ticket = pyro_server.login('admin', 'sportmagazineserver')
        options = FlaskWebServicesSecurityManager.get_service_options()

        if 'status' in request.json:
            options['status'] = request.json['status']
        if 'type' in request.json:
            options['type'] = request.json['type']
        if 'mobile' in request.json:
            options['mobile'] = request.json['mobile']
        if 'phone' in request.json:
            options['phone'] = request.json['phone']
        if 'email' in request.json:
            options['email'] = request.json['email']
        if 'address' in request.json:
            options['address'] = request.json['address']
        if 'work_address' in request.json:
            options['work_address'] = request.json['work_address']
        if 'national_code' in request.json:
            options['national_code'] = request.json['national_code']
        if 'production_type' in request.json:
            options['production_type'] = request.json['production_type']
        if 'production_package' in request.json:
            options['production_package'] = request.json['production_package']

        user = pyro_server.execute_ex(ticket, 'admin', 'security.user.create', {},
                                      request.json['user_name'], request.json['password'],
                                      request.json['full_name'], **options)
        pyro_server.logoff(ticket, 'admin')

        return jsonify({"user_name": user.get('result').get('user_id'),
                        "password": user.get('result').get('user_password'),
                        "full_name": user.get('result').get('user_full_name'),
                        "mobile": user.get('result').get('user_mobile'),
                        "email": user.get('result').get('user_email'),
                        "address": user.get('result').get('user_address'),
                        "phone": user.get('result').get('user_phone'),
                        "work_address": user.get('result').get('user_work_address'),
                        "national_code": user.get('result').get('user_national_code'),
                        "production_type": user.get('result').get('user_production_type'),
                        "production_package": user.get('result').get('user_production_package')})

    @staticmethod
    @flask_app.route('/user/get', methods=["POST"])
    def get_user():
        '''
        Gets user!
        '''

        FlaskWebServicesSecurityManager.check_service_requirements(['ticket', 'user_name'])

        user = \
            pyro_server.execute_ex(request.json['ticket'], request.json['user_name'], 'security.user.get.by_id',
                                   {}, request.json['user_name'])

        return jsonify({"user_name": user.get('result').get('user_id'),
                        "password": user.get('result').get('user_password'),
                        "full_name": user.get('result').get('user_full_name'),
                        "mobile": user.get('result').get('user_mobile'),
                        "email": user.get('result').get('user_email'),
                        "address": user.get('result').get('user_address'),
                        "phone": user.get('result').get('user_phone'),
                        "work_address": user.get('result').get('user_work_address'),
                        "national_code": user.get('result').get('user_national_code'),
                        "production_type": user.get('result').get('user_production_type'),
                        "production_package": user.get('result').get('user_production_package')})

    @staticmethod
    @flask_app.route('/activate/<path:input_data>', methods=["GET"])
    def activate(input_data):
        '''
        Activates!
        '''

        if input_data is None or input_data.strip() == "":
            abort(400)

        decrypted = decrypt_aes(input_data)
        user_id, activation_data = decrypted.split('$')

        ticket = pyro_server.login('admin', 'sportmagazineserver')
        data = pyro_server.execute_ex(ticket, 'admin', 'security.user.activate', {},
                                      user_id, True, activation_data=input_data)
        pyro_server.logoff(ticket, 'admin')

        if data is not None and data.get('result') is not None:
            return jsonify('activate/{0}'.format(encrypt_aes('{0}${1}'.format(user_id, data.get('result')))))

        return jsonify(SUCCESS_RESPONSE)