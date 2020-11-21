from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from datetime import timedelta

from src.api import api_messages
from src.api import api_constants
from src.data.user_repository import UserRepository

account_controller = Blueprint('account_controller', __name__)
user_repository = UserRepository()


@account_controller.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({api_constants.message: api_messages.missing_json}), 400

    username = request.json.get(api_constants.username, None)
    password = request.json.get(api_constants.password, None)
    if not username:
        return jsonify({api_constants.message: api_messages.missing_username_parameter}), 400
    if not password:
        return jsonify({api_constants.message: api_messages.missing_password_parameter}), 400

    try:
        user = user_repository.get_by_username(username)
    except KeyError:
        return jsonify({api_constants.message: api_messages.bad_username_or_password}), 401
    if user[api_constants.password] != password:
        return jsonify({api_constants.message: api_messages.bad_username_or_password}), 401

    access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))
    return jsonify(access_token=access_token), 200
