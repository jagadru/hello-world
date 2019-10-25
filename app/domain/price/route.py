import flask

from app.domain.price import crud_price as crud
from app.utils import (
    errors,
    security
)
from app.utils import json_serializer as json


def init(app):

    """
    Create all routes for prices and discounts.
    app: Flask
    """
    @app.route('/v1/pricing/<id_article>', methods=['GET'])
    def get_price(id_article):
        try:
            return json.dic_to_json(
                crud.get_price(id_article)
            )
        except Exception as err:
            return errors. handleError(err)

    @app.route('/v1/pricing', methods=['POST'])
    def add_price():
        try:
            security.validateAdminRole(flask.request.headers.get("Authorization"))
            token = flask.request.headers.get("Authorization")
            params = json.body_to_dic(flask.request.data)
            responses = []

            for price in params:
                validated_price = restValidator.validateAddPriceParams(price)
                result = crud.addPrice(validated_price)
                responses.append(result.copy())

            return json.dic_to_json(responses)
        except Exception as err:
            return errors.handleError(err)

    @app.route('/', methods=['GET'])
    def hello_world():
        return "Hello world"
