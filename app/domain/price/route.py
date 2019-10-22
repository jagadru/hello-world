import flask

from app.domain.price import crud_price as crud
from app.utils import errors
from app.utils import json_serializer as json


def init(app):

    """
    Create all routes for prices and discounts.
    app: Flask
    """
    @app.route('/v1/pricing/<id_article>', methods=['GET'])
    def get_price(id_article):
        try:
            import ipdb; ipdb.set_trace()
            return json.dic_to_json(
                crud.get_price(id_article)
            )
        except Exception as err:
            return errors. handleError(err)
    
    @app.route('/', methods=['GET'])
    def hello_world():
        return "Hello world"
