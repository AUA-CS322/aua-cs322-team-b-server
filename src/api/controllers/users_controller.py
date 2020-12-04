from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, Resource
from flask import jsonify
from src.api.controllers.api_descriptions import USER_CONTROLLER, STATUS_CODES, USER_SEARCH_CONTROLLER
from src.data.user_repository import UserRepository
from src.api.controllers.search import get_required_fields_by_keyword, ACCEPTED_KEYWORDS_FOR_SEARCH

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
        user_repository = UserRepository()

        return user_repository.get_all()

@users_controller.route('/users/search/<string:query>', methods=['GET'], doc={'description': USER_SEARCH_CONTROLLER})
class UsersSearch(Resource):
    @users_controller.doc(params={'query': 'A Query'},
                          security='apikey',
                          responses={200: STATUS_CODES[200],
                                     401: STATUS_CODES[401],
                                     403: STATUS_CODES[403]})
    @jwt_required
    @cross_origin()
    def get(self, query):
        values = []
        for keyword in ACCEPTED_KEYWORDS_FOR_SEARCH:
            matched_users_list = get_required_fields_by_keyword(keyword, query)
            for user in matched_users_list:
                if user not in values:
                    values.append(user)
        return jsonify(success=True, data=values)
