from flask import Blueprint

home_controller = Blueprint('home_controller', __name__)


@home_controller.route('/')
def get_default():
    return 'Welcome to AUA org-chart'
