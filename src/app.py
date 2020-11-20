from flask import Flask
from flask_jwt_extended import JWTManager

from src.utils.logger.logger import make_logger
from src.api.controllers.home_controller import home_controller
from src.api.controllers.account_controller import account_controller
from src.api.controllers.users_controller import users_controller

app = Flask(__name__)
log = make_logger(__name__)
app.register_blueprint(home_controller)
app.register_blueprint(account_controller)
app.register_blueprint(users_controller)

app.config['JWT_SECRET_KEY'] = 'C1CF4B7DC4C4153KNJ54E4F55OCA4'
jwt = JWTManager(app)

if __name__ == '__main__':
    log.info('Application is running...')
    app.run(debug=1)
