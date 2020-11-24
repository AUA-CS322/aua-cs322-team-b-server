from flask_restplus import Namespace, Resource
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required

from src.api.controllers.api_descriptions import USER_CONTROLLER, STATUS_CODES
from src.data.user_repository import UserRepository

users_controller = Namespace('api', default="AUA Organization Chart",
                             authorizations={'apikey': {'type': 'apiKey',
                                                        'in': 'header',
                                                        'name': 'authorization'
                                                        }
                                             },
                             security='apikey')


@users_controller.route('/users', methods=['GET'], doc={'description': USER_CONTROLLER})
class Users(Resource):
    @users_controller.doc(security='apikey',
                          responses={200: STATUS_CODES[200],
                                     401: STATUS_CODES[401],
                                     403: STATUS_CODES[403]})
    @jwt_required
    @cross_origin()
    def get(self):
        ur = UserRepository()

        return ur.get_all()

