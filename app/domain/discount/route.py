import flask

from app.domain.discount import crud_discount as crud
from app.domain.discount import rest_validations as restValidator
from app.utils import json_serializer as json
from app.utils import (
    errors,
    security
)

def init(app):

    """
    Create all routes for discounts.
    app: Flask
    """
    @app.route('/v1/discount/<article_id>', methods=['GET'])
    def get_discount(article_id):
        try:
            return json.dic_to_json(
                crud.get_discount(article_id, offset=10, page=1)
            )
        except Exception as err:
            return errors. handleError(err)

    @app.route(
        '/v1/discount/<article_id>/?offset=<int:offset>&page=<int:page>',
        methods=['GET']
    )
    def get_discounts_paginated(article_id, offset, page):
        try:
            return json.dic_to_json(
                crud.get_discount(article_id, offset)
            )
        except Exception as err:
            return errors. handleError(err)

    @app.route('/v1/discount', methods=['POST'])
    def add_discount():
        try:
            security.validateAdminRole(flask.request.headers.get("Authorization"))
            token = flask.request.headers.get("Authorization")
            params = json.body_to_dic(flask.request.data)

            validated_price = restValidator.validateAddDiscountParams(params)
            result = crud.add_discount(validated_price)

            return json.dic_to_json(result)
        except Exception as err:
            return errors.handleError(err)

    # @app.route('/v1/discount/<article_id>', methods=['POST'])
    # def update_price(article_id):
    #     try:
    #         security.validateAdminRole(flask.request.headers.get("Authorization"))
    #
    #         params = json.body_to_dic(flask.request.data)
    #
    #         params = restValidator.validateEditPriceParams(price_id, params)
    #
    #         result = crud.update_price(price_id, params)
    #
    #         return json.dic_to_json(result)
    #     except Exception as err:
    #         return errors.handleError(err)
