"""
Created on Sep 12, 2016

@author: Hamed Zekri
"""

from flask import Flask, request, abort, jsonify, json

from deltapy.core import DeltaObject
import deltapy.application.services as services

from server.wsdl.service_manager import PyroServer

pyro_server = PyroServer("127.0.0.1", "6082")
app = Flask("flask-{0}".format(services.get_name()))


class FlaskWebServicesManager(DeltaObject):
    """
    Flask Web Services Manager
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
    @app.route("/login", methods=["POST"])
    def login():
        """
        Logins!
        """

        FlaskWebServicesManager.check_service_requirements(['user_name', 'password'])
        FlaskWebServicesManager.check_user_name()

        options = FlaskWebServicesManager.get_service_options()
        ticket = pyro_server.login(request.json['user_name'], request.json['password'], **options)
        return jsonify({"ticket": ticket})

    @staticmethod
    @app.route('/signin', methods=["POST"])
    def Signin():
        '''
        Sign in!
        '''

        FlaskWebServicesManager.check_service_requirements(['user_name', 'full_name', 'password'])
        FlaskWebServicesManager.check_user_name()

        ticket = pyro_server.login('admin', 'sportmagazineserver')
        options = FlaskWebServicesManager.get_service_options()
        user = pyro_server.execute_ex(ticket, 'admin', 'security.user.create', {},
                                      request.json['user_name'], request.json['password'],
                                      request.json['full_name'], **options)
        pyro_server.logoff(ticket, 'admin')

        return jsonify({"user_name": user.get('user_name')})