from flask import Flask
from utils.logger.logger import make_logger
from home_page import home_page_blue_print

app = Flask(__name__)
log = make_logger(__name__)
app.register_blueprint(home_page_blue_print)

if __name__ == '__main__':
    log.info('Application is running...')
    app.run(debug=1)
