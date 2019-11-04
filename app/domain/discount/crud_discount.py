from datetime import datetime

from app.domain.discount import (
    OFFSET,
    PAGE,
)
from app.domain.discount import discount_schema as schema
from app.utils import errors
from app.utils import mongo as db

def get_discount(article_id, offset, page):
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
        if not offset or offset == 0 or offset > OFFSET:
            offset = OFFSET

        if not page or page == 0:
            page = PAGE

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
        }

    @apiSuccessExample {json} Respuesta
        HTTP/1.1 200 OK
        {
            “id_discount”: “{ID del descuento}”,
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

def _addOrUpdateDiscount(params):
    is_new = True
    discount = schema.new_discount()

    if ("discount_id" in params):
        is_new = False
        result = get_discount(params["article_id"])
        # Si devuelve con alguna estructura paginada, leer desde "discounts"
        [discount.append(r) for r in result]

    discount.update(params)
    discount['updated'] = datetime.utcnow()
    discount['article_id'] = params['article_id']

    if (not is_new):
        pass
    else:
        discount['discount_id'] = db.discounts.insert_one(discount).inserted_id
    return discount


    ### Falta
    ### - delete discount
    ### - update discount
    ### - mensaje asincrono
