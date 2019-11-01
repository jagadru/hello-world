from datetime import datetime
import bson.objectid as bson

from app.utils import errors
from app.utils import mongo as db
from app.domain.price import price_schema as schema
from app.domain.price import (
    ACTIVE,
    HIDDEN,
)
from app.gateways.rabbit_service import send_new_price

def get_price(article_id):
    """
    Return a price. \n
    articleId: string ObjectId\n
    return dict<key, value> Price\n
    """
    """
    @api {get} /v1/pricing/:article_id Get Price
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
            "article_id": "{Article Id}"
        }]

    @apiUse Errors
    """
    try:
        result = db.prices.find({"article_id": article_id})
        price_to_return = {"prices": []}

        for price in result:
            if price['state'] == ACTIVE:
                price_to_return['prices'].append(price)

        if (not result):
            raise errors.InvalidArgument("_id", "Document does not exists")
        return price_to_return
    except Exception:
        raise errors.InvalidArgument("_id", "Invalid object id")

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
            "article_id": "{Article Id}"
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
            "article_id": "{Article Id}"
            "created": {Created Date}
            "updated": {Updated Date}
        }

    @apiUse Errors

    """
    response = _addOrUpdatePrice(params)

    message = {}
    message['article_id'] = response['article_id']
    message['price'] = response['price']
    message['created'] = response['created']
    send_new_price("prices", "prices", "price_change", message)

    return response

def update_price(price_id, params):
    """
    Update a priceActualiza un articulo. \n
    price_id: string ObjectId\n
    params: dict<key, value> Price\n
    return dict<key, value> Price\n
    """
    """
    @api {post} /v1/pricing/:price_id Update Price
    @apiName Update Price
    @apiGroup Price

    @apiUse AuthHeader

    @apiExample {json} Body
        {
            "max_price": {Max Price}
            "min_price": {Min Price}
            "price": {Current price},
            "price_currency": {Price Currency}
            "article_id": "{Article Id}"
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
            "article_id": "{Article Id}"
            "created": {Created Date}
            "updated": {Updated Date}
        }

    @apiUse Errors

    """
    params["price_id"] = price_id
    return _addOrUpdatePrice(params)

def del_price(article_id):
    """
    Change price state to HIDDEN.\n
    article_id: string ObjectId
    """
    """

    @api {delete} /pricing/:article_id Delete a Price
    @apiName Delete a Price
    @apiGroup Price

    @apiUse AuthHeader

    @apiSuccessExample {json} 200 Respuesta
        HTTP/1.1 200 OK

    @apiUse Errors

    """
    price = get_price(article_id)
    price["updated"] = datetime.utcnow()
    price["state"] = HIDDEN
    db.prices.save(price)

def _addOrUpdatePrice(params):
    is_new = True
    price = schema.new_price()
    if ("price_id" in params):
        is_new = False
        result = get_price(params["article_id"])
        [price.append(r) for r in result]

    price.update(params)
    price["updated"] = datetime.utcnow()
    price["formated_price"] = "{} {}".format(params["price_currency"], params["price"])
    schema.validateSchema(price)

    if (not is_new):
        del price["price_id"]
        r = db.prices.replace_one({"price_id": bson.ObjectId(params["price_id"])}, price)
        price["price_id"] = params["price_id"]
    else:
        price["price_id"] = db.prices.insert_one(price).inserted_id

    return price
