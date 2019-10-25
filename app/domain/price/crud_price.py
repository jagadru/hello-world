import datetime

from app.utils import errors
from app.utils import mongo as db
from app.domain.price import price_schema as price
from app.domain.price import (
    ACTIVE,
    DISABLED,
)

def get_price(id_article):
    """
    Return a price. \n
    articleId: string ObjectId\n
    return dict<key, value> Price\n
    """
    """
    @api {get} /v1/pricing/:id_article Get Price
    @apiName Get Price
    @apiGroup Price

    @apiSuccessExample {json} Response
        HTTP/1.1 200 OK
        [{
            "price_id": "{Price Id}"
            "created": {Creation Date}
            "state": {Price State}
            "max_price": {Max Price}
            "min_price": {Min Price}
            "price": {Current price},
            "price_currency": {Price Currency}
            "formated_price": {Formated Price}
            "id_article": "{Article Id}"
        }]

    @apiUse Errors
    """
    try:
        result = db.prices.find({"article_id": id_article})
        price_to_return = {"prices": []}

        for price in result:
            if price['state'] == ACTIVE:
                price_to_return['prices'].append(price)

        if (not result):
            raise error.InvalidArgument("_id", "Document does not exists")
        return price_to_return
    except Exception:
        raise error.InvalidArgument("_id", "Invalid object id")

def add_price(params):
    """
    Add a price.\n
    params: dict<propiedad, valor> Price\n
    return dict<propiedad, valor> Price
    """
    """
    @api {post} /v1/pricing/ Create Price
    @apiName Create Price
    @apiGroup Price

    @apiUse AuthHeader

    @apiExample {json} Body
        {
            "max_price": {Max Price}
            "min_price": {Min Price}
            "price": {Current price},
            "price_currency": {Price Currency}
            "id_article": "{Article Id}"
        }

    @apiSuccessExample {json} Respuesta
        HTTP/1.1 200 OK
        {
            "price_id": "{Price Id}"
            "max_price": {Max Price}
            "min_price": {Min Price}
            "price": {Current price},
            "price_currency": {Price Currency}
            "formated_price": {Formated Price}
            "id_article": "{Article Id}"
            "updated": {Updated Date}
        }

    @apiUse Errors

    """
    return _addOrUpdatePrice(params)

def _addOrUpdatePrice(params):
    is_new = True
    price = schema.new_price()

    if ("price_id" in params):
        isNew = False
        old_prices = getPrice(params["article_id"])

    prices.update(params)
    schema.validateSchema(prices)
