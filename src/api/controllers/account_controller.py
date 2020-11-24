from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from datetime import timedelta

from src.api import api_messages
from src.api import api_constants
from src.data.user_repository import UserRepository

account_controller = Blueprint('account_controller', __name__, url_prefix='/api')
user_repository = UserRepository()


@account_controller.route('/sign-in', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({api_constants.MESSAGE: api_messages.MISSING_JSON}), 400

    username = request.json.get(api_constants.USERNAME)
    password = request.json.get(api_constants.PASSWORD)
    if not username:
        return jsonify(
            {
                api_constants.SUCCESS: False,
                api_constants.MESSAGE: api_messages.MISSING_USERNAME
            }), 400
    if not password:
        return jsonify(
            {
                api_constants.SUCCESS: False,
                api_constants.MESSAGE: api_messages.MISSING_PASSWORD
            }), 400

    try:
        user = user_repository.get_by_username(username)
    except KeyError:
        return jsonify(
            {
                api_constants.SUCCESS: False,
                api_constants.MESSAGE: api_messages.BAD_USERNAME_OR_PASSWORD
            }), 200
    if user[api_constants.PASSWORD] != password:
        return jsonify(
            {
                api_constants.SUCCESS: False,
                api_constants.MESSAGE: api_messages.BAD_USERNAME_OR_PASSWORD
            }), 200

    access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))
    return jsonify(
        {
            api_constants.SUCCESS: True,
            api_constants.DATA: access_token
        }), 200
