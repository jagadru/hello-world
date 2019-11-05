import flask

from app.domain.price import crud_price as crud
from app.domain.price import rest_validations as restValidator
from app.domain import (
    MAX_OFFSET,
    PAGE,
)
from app.utils import (
    errors,
    security
)
from app.utils import json_serializer as json


def init(app):

    """
    Create all routes for prices.
    app: Flask
    """
    @app.route('/v1/pricing/<article_id>', methods=['GET'])
    def get_price(article_id):
        try:
            return json.dic_to_json(
                crud.get_price(article_id)
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
                result = crud.add_price(validated_price)
                responses.append(result.copy())

            return json.dic_to_json(responses)
        except Exception as err:
            return errors.handleError(err)

    @app.route('/v1/pricing/<article_id>', methods=['POST'])
    def update_price(article_id):
        try:
            security.validateAdminRole(flask.request.headers.get("Authorization"))

            params = json.body_to_dic(flask.request.data)

            params = restValidator.validateEditPriceParams(article_id, params)

            result = crud.update_price(article_id, params)

            return json.dic_to_json(result)
        except Exception as err:
            return errors.handleError(err)

    @app.route('/v1/pricing/<article_id>', methods=['DELETE'])
    def del_price(article_id):
        try:
            security.validateAdminRole(flask.request.headers.get("Authorization"))
            crud.del_price(article_id)
            return "Deleted correctly!"
        except Exception as err:
            return errors.handleError(err)

    @app.route(
        '/v1/pricing/<article_id>/history/',
        methods=['GET']
    )
    def get_price_history(article_id):
        try:
            offset = int(flask.request.args.get('offset')) if flask.request.args.get('offset') else MAX_OFFSET
            page = int(flask.request.args.get('page')) if flask.request.args.get('page') else PAGE
            return json.dic_to_json(
                crud.get_price_history(article_id, offset, page)
            )
        except Exception as err:
            return errors. handleError(err)
