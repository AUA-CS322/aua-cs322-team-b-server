from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restplus import Api

from src.utils.logger.logger import make_logger
from src.api.controllers.account_controller import account_controller
from src.api.controllers.users_controller import users_controller

app = Flask(__name__)
log = make_logger(__name__)
api = Api(app, default="AUA Organization Chart")

api.add_namespace(account_controller)
api.add_namespace(users_controller)

app.config.from_pyfile('config.py')
jwt = JWTManager(app)

if __name__ == '__main__':
    log.info('Application is running...')
    app.run(debug=1)
