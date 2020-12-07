from datetime import timedelta
from flask import jsonify, request, make_response
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token

from flask_restplus import Namespace, Resource, fields
from src.api import api_messages
from src.api import api_constants
from src.api.controllers.api_descriptions import ACCOUNT_CONTROLLER, STATUS_CODES
from src.api.managers.account_manager import AccountManager
from src.data.user_repository import UserRepository

account_controller = Namespace('api')
user_repository = UserRepository()

SIGN_IN = account_controller.model('Sign In', {'username': fields.String(required=True),
                                               'password': fields.String(required=True)})


@account_controller.route('/sign-in', methods=['POST'], doc={'description': ACCOUNT_CONTROLLER})
class SignIn(Resource):
    @account_controller.doc(body=SIGN_IN,
                            responses={200: STATUS_CODES[200],
                                       400: STATUS_CODES[400]})
    @cross_origin()
    def post(self):
        if not request.is_json:
            return make_response(jsonify({api_constants.MESSAGE: api_messages.MISSING_JSON}), 400)

        username = request.json.get(api_constants.USERNAME)
        password = request.json.get(api_constants.PASSWORD)

        message = SignIn.validate_user(username, password)
        if message[0] is None:
            access_token = create_access_token(identity=message[1][api_constants.ID], expires_delta=timedelta(days=1))
            return make_response(jsonify(
                {
                    api_constants.SUCCESS: True,
                    api_constants.DATA: access_token
                }), 200)

        return make_response(jsonify(
                {
                    api_constants.SUCCESS: False,
                    api_constants.MESSAGE: message[1]
                }), message[0])

    def validate_user(username, password):
        if not username:
            return (400,api_messages.MISSING_USERNAME)
        if not password:
            return (400,api_messages.MISSING_PASSWORD)

        try:
            user = user_repository.get_by_username(username)
        except KeyError:
            pass
        if user is None:
            try:
                user = user_repository.get_by_email(username)
            except KeyError:
                return make_response(jsonify({
                    api_constants.SUCCESS: False,
                    api_constants.MESSAGE: api_messages.BAD_USERNAME_OR_PASSWORD
                }), 200)
        if user is None:
            return (200, api_messages.BAD_USERNAME_OR_PASSWORD)

        is_password_correct = \
            AccountManager.is_password_correct(
                password=password, hashed_password=user[api_constants.PASSWORD])
        if not is_password_correct:
            return (200, api_messages.BAD_USERNAME_OR_PASSWORD)

        return (None, user)
