from flask import Blueprint

home_page_blue_print = Blueprint('home_page_blue_print', __name__)

@home_page_blue_print.route('/')
def home_page():
    return 'Hello guys'
