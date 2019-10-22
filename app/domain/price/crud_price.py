import datetime

from bson import objectid as bson

from app.utils import errors
from app.utils import mongo as db
from app.domain.price import PRICE_ACTIVE
from app.domain.price import price_schema as price

def get_price(id_article):
    import ipdb; ipdb.set_trace()
    """
    Return a price. \n
    articleId: string ObjectId\n
    return dict<key, value> Price\n
    """
    """
    @api {get} /v1/pricing/:id_article Search Price
    @apiName Search Price
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
            "id_article": "{Article Id}"
        }

    @apiUse Errors
    """
    try:
            # Que el precio no tenga el estado ACTIVO
            # Que no exista
            # Formatear el Price
        result = db.prices.find({"article_id": id_article})
        for i in result:
            import ipdb; ipdb.set_trace()
        import ipdb; ipdb.set_trace()
        if (not result):
            raise error.InvalidArgument("_id", "Document does not exists")
        return ultimoPrecio
    except Exception:
        raise error.InvalidArgument("_id", "Invalid object id")
