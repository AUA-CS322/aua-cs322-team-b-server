from flask import jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, Resource
from src.api.controllers.api_descriptions import USER_CHART_ORGANIZATION, STATUS_CODES
from src.data.organization_chart import OrganizationChart

authorizations = {'apikey':
                      {'type': 'apiKey',
                       'in': 'header',
                       'name': 'authorization'}
                  }

responses = {
    200: STATUS_CODES[200],
    401: STATUS_CODES[401],
    403: STATUS_CODES[403]
}

users_chart_controller = Namespace('api',
                                   default='AUA Organization Chart',
                                   authorizations=authorizations,
                                   security='apikey')


@users_chart_controller.route('/users/chart', methods=['GET'], doc={'description': USER_CHART_ORGANIZATION})
class OrganizationChartTree(Resource):

    @users_chart_controller.doc(security='apikey', responses=responses)
    @jwt_required
    @cross_origin()
    def get(self):
        organization_chart = OrganizationChart()
        return jsonify(sucess=True, data=organization_chart.get_chart())
