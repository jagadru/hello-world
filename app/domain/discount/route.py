import flask
from app.domain import (
    MAX_OFFSET,
    PAGE
)
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
    @app.route('/v1/pricing/<discount_id>/discount/', methods=['GET'])
    def get_discount(discount_id):
        try:
            return json.dic_to_json(
                crud.get_discount(discount_id)
            )
        except Exception as err:
            return errors. handleError(err)

    @app.route('/v1/pricing/<article_id>/article-discounts/', methods=['GET'])
    def get_discounts_by_article_id(article_id):
        try:
            offset = int(flask.request.args.get('offset')) if flask.request.args.get('offset') else MAX_OFFSET
            page = int(flask.request.args.get('page')) if flask.request.args.get('page') else PAGE
            return json.dic_to_json(
                crud.get_discounts_by_article_id(article_id, offset, page)
            )
        except Exception as err:
            return errors. handleError(err)

    @app.route('/v1/pricing/discount/', methods=['POST'])
    def add_discount():
        try:
            security.validateAdminRole(flask.request.headers.get("Authorization"))
            token = flask.request.headers.get("Authorization")
            params = json.body_to_dic(flask.request.data)

            validated_discount = restValidator.validateAddDiscountParams(params)

            result = crud.add_discount(validated_discount)

            return json.dic_to_json(result)
        except Exception as err:
            return errors.handleError(err)

    @app.route('/v1/pricing/<discount_id>/discount/', methods=['POST'])
    def update_discount(discount_id):
        try:
            security.validateAdminRole(flask.request.headers.get("Authorization"))

            params = json.body_to_dic(flask.request.data)

            params = restValidator.validateEditDiscountParams(discount_id, params)

            result = crud.update_discount(discount_id, params)

            return json.dic_to_json(result)
        except Exception as err:
            return errors.handleError(err)

    @app.route('/v1/pricing/<discount_id>/discount/', methods=['DELETE'])
    def del_discount(discount_id):
        try:
            security.validateAdminRole(flask.request.headers.get("Authorization"))
            crud.del_discount(discount_id)
            return "Deleted correctly!"
        except Exception as err:
            return errors.handleError(err)
