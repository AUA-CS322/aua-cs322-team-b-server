from flask import jsonify, make_response
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Namespace, Resource
from src.api.controllers.api_descriptions import USER_CONTROLLER, STATUS_CODES, USER_SEARCH_CONTROLLER, \
    USER_GET_BY_ID_CONTROLLER
from src.api.controllers.search import get_required_fields_by_keyword, ACCEPTED_KEYWORDS_FOR_SEARCH
from src.data.user_repository import UserRepository
from src.api.controllers.search import get_required_fields_by_keyword, ACCEPTED_KEYWORDS_FOR_SEARCH
from src.data.organization_chart import OrganizationChart
from src.utils.user_mapper import map_to_response_user
from src.api import api_messages
from src.api import api_constants

authorizations = {'apikey':
                      {'type': 'apiKey',
                       'in': 'header',
                       'name': 'authorization'}
                  }

responses = {
    200: STATUS_CODES[200],
    401: STATUS_CODES[401],
    403: STATUS_CODES[403],
    404: STATUS_CODES[404]
}

users_controller = Namespace('api', default='AUA Organization Users', authorizations=authorizations, security='apikey')
user_repository = UserRepository()


@users_controller.route('/users', methods=['GET'], doc={'description': USER_CONTROLLER})
class Users(Resource):

    @users_controller.doc(security='apikey', responses=responses)
    @jwt_required
    @cross_origin()
    def get(self):
        user = user_repository.get_by_username(get_jwt_identity())
        user_id = user[api_constants.ID]
        user, parent = OrganizationChart().get_user_with_manager(user_id)

        if not user:
            return make_response(jsonify(
                {
                    api_constants.SUCCESS: False,
                    api_constants.MESSAGE: api_messages.USER_NOT_FOUND
                }), 404)

        return make_response(jsonify(
            {
                api_constants.SUCCESS: True,
                api_constants.DATA: map_to_response_user(user, parent)
            }), 200)


@users_controller.route('/users/info/<string:user_id>', methods=['GET'], doc={'description': USER_GET_BY_ID_CONTROLLER})
class Users(Resource):

    @users_controller.doc(params={'user_id': 'The User Id for retrieval.'}, security='apikey', responses=responses)
    @jwt_required
    @cross_origin()
    def get(self, user_id):
        user, parent = OrganizationChart().get_user_with_manager(user_id)

        if not user:
            return make_response(jsonify(
                {
                    api_constants.SUCCESS: False,
                    api_constants.MESSAGE: api_messages.USER_NOT_FOUND
                }), 404)

        return make_response(jsonify(
            {
                api_constants.SUCCESS: True,
                api_constants.DATA: map_to_response_user(user, parent)
            }), 200)


@users_controller.route('/users/search/<string:query>', methods=['GET'], doc={'description': USER_SEARCH_CONTROLLER})
class UsersSearch(Resource):

    @users_controller.doc(params={'query': 'A Query'}, security='apikey', responses=responses)
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
