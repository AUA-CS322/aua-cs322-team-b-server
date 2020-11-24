from flask import jsonify, request
from flask_jwt_extended import create_access_token

from datetime import timedelta
from flask_restplus import Namespace, Resource, fields
from flask import make_response
from src.api import api_messages
from src.api import api_constants
from src.api.controllers.api_descriptions import ACCOUNT_CONTROLLER, STATUS_CODES
from src.data.user_repository import UserRepository

account_controller = Namespace('api')
user_repository = UserRepository()

SIGN_IN = account_controller.model('Sign In', {'username': fields.String(required=True),
                                               'password': fields.String(required=True)})


@account_controller.route('/sign-in', methods=['POST'], doc={'description': ACCOUNT_CONTROLLER})
class SignIn(Resource):
    @account_controller.doc(body=SIGN_IN,
                            responses={200: STATUS_CODES[200],
                                       400: STATUS_CODES[400]},
                            )
    def post(self):
        if not request.is_json:
            return make_response(jsonify({api_constants.MESSAGE: api_messages.MISSING_JSON}), 400)

        username = request.json.get(api_constants.USERNAME)
        password = request.json.get(api_constants.PASSWORD)
        if not username:
            return make_response(jsonify(
                {
                    api_constants.SUCCESS: False,
                    api_constants.MESSAGE: api_messages.MISSING_USERNAME
                }), 400)
        if not password:
            return make_response(jsonify(
                {
                    api_constants.SUCCESS: False,
                    api_constants.MESSAGE: api_messages.MISSING_PASSWORD
                }), 400)

        try:
            user = user_repository.get_by_username(username)
        except KeyError:
            return make_response(jsonify(
                {
                    api_constants.SUCCESS: False,
                    api_constants.MESSAGE: api_messages.BAD_USERNAME_OR_PASSWORD
                }), 200)
        if user[api_constants.PASSWORD] != password:
            return make_response(jsonify(
                {
                    api_constants.SUCCESS: False,
                    api_constants.MESSAGE: api_messages.BAD_USERNAME_OR_PASSWORD
                }), 200)

        access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))
        return make_response(jsonify(
            {
                api_constants.SUCCESS: True,
                api_constants.DATA: access_token
            }), 200)
