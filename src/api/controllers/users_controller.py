from flask import Blueprint
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from src.data.user_repository import UserRepository

users_controller = Blueprint('users_controller', __name__, url_prefix='/api')


@users_controller.route('/users', methods=['GET'])
@jwt_required
@cross_origin()
def get_users():
    ur = UserRepository()
    return ur.get_all()
