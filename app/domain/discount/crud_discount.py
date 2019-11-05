import bson.objectid as bson

from app.domain import HIDDEN
from app.domain.helpers import validate_offset_page
from app.domain.discount import discount_schema as schema
from app.gateways.rabbit_service import send_new_discount
from app.utils import errors
from app.utils import mongo as db

def get_discount(discount_id):
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
            “discount_id”: “{ID del descuento}”,
            “discount_name”: “{Nombre del descuento}”,
            “discount_value”: “{Porcentaje de descuento}”,
            “discount_code”: “{Codigo de descuento}”,
            “visibility”: “{Si es publico, privado, etc}”,
            “validFrom”: “{Fecha de inicio de validez}”,
            “validTo”: “{Fecha de fin de validez}”,
            created: “{Fecha de creacion}”,
        }

    @apiUse Errors
    """
    try:
        results = db.discounts.find({"_id": bson.ObjectId(discount_id)})

        for result in results:
            response = result

        if (not result):
            raise errors.InvalidArgument("_id", "Document does not exists")
        return response
    except Exception:
        raise errors.InvalidArgument("_id", "Invalid object id")


def get_discounts_by_article_id(article_id, offset, page):
    """
    Return a discount. \n
    articleId: string ObjectId\n
    offset: int
    """
    """
    @api {get} /v1/pricing/:article_id Discount Price
    @apiName Get Discount
    @apiGroup Discount

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
            "discounts": [
            {
                “id_discount”: “{ID del descuento}”,
                “discount_name”: “{Nombre del descuento}”,
                “discount_value”: “{Porcentaje de descuento}”,
                “discount_code”: “{Codigo de descuento}”,
                “visibility”: “{Si es publico, privado, etc}”,
                “validFrom”: “{Fecha de inicio de validez}”,
                “validTo”: “{Fecha de fin de validez}”,
            }, ….
            ]
        }
    @apiUse Errors
    """
    try:
        offset, page = validate_offset_page(offset, page)

        response = {}
        response['pagination'] = {}
        response['pagination']['object_count'] = db.discounts.find({"article_id": article_id}).count()
        response['pagination']['page_count'] = round(response['pagination']['object_count'] / page)
        response['pagination']['has_more_items'] = 'False'

        if response['pagination']['object_count'] > offset:
            response['pagination']['page_size'] = offset
            response['pagination']['has_more_items'] = 'True'

        response['pagination']['page_number'] = page
        response['pagination']['article_id'] = article_id
        response['pagination']['discounts'] = []

        results = db.discounts.find({"article_id": article_id}).skip(offset * (page - 1)).limit(offset)

        if (not results):
            raise errors.InvalidArgument("_id", "Document does not exists")

        for result in results:
            discount = {}
            discount['id_discount'] = str(result['_id'])
            discount['discount_name'] = result['discount_name']
            discount['discount_value'] = result['discount_value']
            discount['discount_code'] = result['discount_code']
            discount['visibility'] = result['visibility']
            discount['discount_value'] = result['discount_value']
            discount['validFrom'] = result['validFrom']
            discount['validTo'] = result['validTo']

            response['pagination']['discounts'].append(discount)

        return response

    except Exception:
        raise errors.InvalidArgument("article_id", "Invalid object id")

def add_discount(params):
    """
    Add a discount.\n
    params: dict<propiedad, valor> Discount\n
    return dict<propiedad, valor> Discount
    """
    """
    @api {post} /v1/pricing/ Create Discount
    @apiName Create Discount
    @apiGroup Discount

    @apiUse AuthHeader

    @apiExample {json} Body
        {
            “discount_name”: “{Nombre del descuento}”,
            “discount_value”: “{Porcentaje de descuento}”,
            “discount_code”: “{Codigo de descuento}”,
            “visibility”: “{Si es publico, privado, etc}”,
            “validFrom”: “{Fecha de inicio de validez}”,
            “validTo”: “{Fecha de fin de validez}”,
            "article_id": “{ID del articulo}”,
            "state": “{Estado del descuento}”
        }

    @apiSuccessExample {json} Respuesta
        HTTP/1.1 200 OK
        {
            “discount_id”: “{ID del descuento}”,
            “discount_name”: “{Nombre del descuento}”,
            “discount_value”: “{Porcentaje de descuento}”,
            “discount_code”: “{Codigo de descuento}”,
            “visibility”: “{Si es publico, privado, etc}”,
            “validFrom”: “{Fecha de inicio de validez}”,
            “validTo”: “{Fecha de fin de validez}”,
            "created": “{Fecha Hora de Creacion}”,
            “updated”: “{Fecha Hora de Actualizacion}”,
            "article_id": "{ID del producto}"
        }

    @apiUse Errors

    """
    response = _addOrUpdateDiscount(params)

    return response

def update_discount(discount_id, params):
    """
    Update a discount. \n
    discount_id: string ObjectId\n
    params: dict<key, value> Discount\n
    return dict<key, value> Discount\n
    """
    """
    @api {post} /v1/pricing/:discount_id/discount Update Price
    @apiName Update Discount
    @apiGroup Discount

    @apiUse AuthHeader

    @apiExample {json} Body
        {
            “discount_name”: “{Nombre del descuento}”,
            “discount_value”: “{Porcentaje de descuento}”,
            “discount_code”: “{Codigo de descuento}”,
            “visibility”: “{Si es publico, privado, etc}”,
            “validFrom”: “{Fecha de inicio de validez}”,
            “validTo”: “{Fecha de fin de validez}”,
            "article_id": “{ID del articulo}”,
            "state": “{Estado del descuento}”
        }

    @apiSuccessExample {json} Respuesta
        HTTP/1.1 200 OK
        {
            “discount_id”: “{ID del descuento}”,
            “discount_name”: “{Nombre del descuento}”,
            “discount_value”: “{Porcentaje de descuento}”,
            “discount_code”: “{Codigo de descuento}”,
            “visibility”: “{Si es publico, privado, etc}”,
            “validFrom”: “{Fecha de inicio de validez}”,
            “validTo”: “{Fecha de fin de validez}”,
            "article_id": “{ID del articulo}”,
            "state": “{Estado del descuento}”
            "created": {Created Date}
        }

    @apiUse Errors

    """
    params['discount_id'] = discount_id
    return _addOrUpdateDiscount(params)

def _addOrUpdateDiscount(params):
    discount = schema.new_discount()

    discount.update(params)
    discount['article_id'] = params['article_id']

    if ("discount_id" in params):
        db.discounts.update_one(
            {"_id": bson.ObjectId(params["discount_id"])},
            {"$set": {'state': HIDDEN} }
        )

    discount["_id"] = db.discounts.insert_one(discount).inserted_id

    message = {}
    message['discount_id'] = discount['article_id']
    message['discount_code'] = discount['discount_code']
    message['created'] = discount['created']

    send_new_discount("discounts", "discounts", "discount_change", message)

    return discount

def del_discount(discount_id):
    """
    Change discount state to HIDDEN.\n
    discount_id: string ObjectId
    """
    """

    @api {delete} /pricing/:discount_id/discount Delete a Discount
    @apiName Delete a Discount
    @apiGroup Discount

    @apiUse AuthHeader

    @apiSuccessExample {json} 200 Respuesta
        HTTP/1.1 200 OK

    @apiUse Errors

    """
    db.discounts.update_one(
        {"_id": bson.ObjectId(discount_id)},
        {"$set": {'state': HIDDEN} }
    )
