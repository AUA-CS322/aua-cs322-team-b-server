from flask import Blueprint
from flask_jwt_extended import jwt_required

from src.data.user_repository import UserRepository

users_controller = Blueprint('users_controller', __name__)


@users_controller.route('/users', methods=['GET'])
@jwt_required
def login():
    ur = UserRepository()
    return ur.get_all()
