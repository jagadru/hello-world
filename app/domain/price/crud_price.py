from datetime import datetime

from app.utils import errors
from app.utils import mongo as db
from app.domain.price import price_schema as schema
from app.domain import (
    ACTIVE,
    HIDDEN,
)
from app.domain.helpers import validate_offset_page
from app.gateways.rabbit_service import (
    send_new_price,
    send_is_article_valid,
)

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
        {
            "price_id": "{Price Id}"
            "created": {Creation Date}
            "state": {Price State}
            "max_price": {Max Price}
            "min_price": {Min Price}
            "price": {Current price},
            "price_currency": {Price Currency}
            "formated_price": {Formated Price}
            "article_id": "{Article Id}"
        }

    @apiUse Errors
    """
    try:
        result = db.prices.find({"article_id": article_id}).sort([('_id', -1)]).limit(1)
        response = {}

        for res in result:
            if res['state'] == ACTIVE:
                response = res

        if (not result):
            raise errors.InvalidArgument("_id", "Document does not exists")
        return response
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
    result = _addOrUpdatePrice(params)

    message = {}
    message['article_id'] = result['article_id']
    message['price'] = result['price']
    message['created'] = result['created']

    send_new_price("prices", "prices", "price-change", message)
    return result

def update_price(article_id, params):
    """
    Update a price. \n
    price_id: string ObjectId\n
    params: dict<key, value> Price\n
    return dict<key, value> Price\n
    """
    """
    @api {post} /v1/pricing/:article_id Update Price
    @apiName Update Price
    @apiGroup Price

    @apiUse AuthHeader

    @apiExample {json} Body
        {
            "max_price": {Max Price}
            "min_price": {Min Price}
            "price": {Current price},
            "price_currency": {Price Currency}
            "price_id": "{Price Id}"
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
    params['article_id'] = article_id
    result = _addOrUpdatePrice(params)

    message = {}
    message['article_id'] = result['article_id']
    message['price'] = result['price']
    message['created'] = result['created']

    send_new_price("prices", "prices", "price-change", message)
    return result

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
    price["state"] = HIDDEN
    db.prices.save(price)

def _addOrUpdatePrice(params):
    price = schema.new_price()
    price.update(params)

    price["formated_price"] = "{} {}".format(params["price_currency"], params["price"])
    price["article_id"] = params["article_id"]

    schema.validateSchema(price)

    if (not params.get("_id")):
        db.prices.update_one(
            {"article_id": params['article_id']},
            {"$set": {'state': HIDDEN} }
        )

    price["_id"] = db.prices.insert_one(price).inserted_id
    send_is_article_valid('catalog', 'catalog', 'article-exist', price)

    return price

def get_price_history(article_id, offset, page):
    """
    Return a all prices of an article. \n
    articleId: string ObjectId\n
    return list(dict<key, value>) Price\n
    """
    """
    @api {get} /v1/pricing/:article_id Get Price History
    @apiName Get Price History
    @apiGroup Price

    @apiSuccessExample {json} Response
        HTTP/1.1 200 OK
        {
        "pagination": {
            "object_count": “{Numero de objetos en todas las paginas}”,
            "page_count": “{Numero de total de paginas}”,
            "page_size": “{Numero maximo de objetos en una response}”,
            "has_more_items": “{Si se puede seguir pidiendo valores a la API}”,
            "page_number": “{Numero de pagina actual}”,
            "article_id": "{ID del producto}"
            "price_schema": [
            {
                "_id": "{Price Id}"
                "created": {Creation Date}
                "state": {Price State}
                "max_price": {Max Price}
                "min_price": {Min Price}
                "price": {Current price},
                "price_currency": {Price Currency}
                "formated_price": {Formated Price}
            }, ….
            ]
        }
    @apiUse Errors
    """
    try:
        offset, page = validate_offset_page(offset, page)

        response = {}
        response['pagination'] = {}
        response['pagination']['object_count'] = db.prices.find({"article_id": article_id}).count()
        response['pagination']['page_count'] = round(response['pagination']['object_count'] / page)
        response['pagination']['has_more_items'] = 'False'

        if response['pagination']['object_count'] > offset:
            response['pagination']['page_size'] = offset
            response['pagination']['has_more_items'] = 'True'

        response['pagination']['page_number'] = page
        response['pagination']['article_id'] = article_id
        response['pagination']['prices'] = []

        results = db.prices.find({"article_id": article_id}).skip(offset * (page - 1)).limit(offset)

        if (not results):
            raise errors.InvalidArgument("_id", "Document does not exists")

        for result in results:
            price = {}
            price['price_id'] = str(result['_id'])
            price['created'] = result['created']
            price['state'] = result['state']
            price['max_price'] = result['max_price']
            price['min_price'] = result['min_price']
            price['price'] = result['price']
            price['price_currency'] = result['price_currency']
            price['formated_price'] = result['formated_price']

            response['pagination']['prices'].append(price)

        return response

    except Exception:
        raise errors.InvalidArgument("article_id", "Invalid object id")
