from flask import request, Response
import json


def init(app):

    @app.route("/")
    def route_test():
        return "<h3>Hello!</h3>"
