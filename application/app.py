import flask
from flask_cors import CORS

from utils import config
from pricing import routes as pricing_routes

class MainApp:
    instance = None

    def __init__(self):
        # Init flask_app
        self.app = flask.Flask(__name__)
        CORS(self.app, support_credentials=True, automatic_options=True)
        # Init other apps
        self._init_pricing()

        MainApp.instance = self.app

    def _init_pricing(self):
        pricing_routes.init(self.app)

    def start(self, debug=True):
        self.app.run(port=config.get_server_port(), debug=debug)

    @staticmethod
    def wsgi(*args):
        if not MainApp.instance:
            MainApp()
        return MainApp.instance(*args)
