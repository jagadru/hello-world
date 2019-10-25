# coding=utf_8
import numbers
from utils import (
    error,
    schema_validator
)
import prices.crud_service as crud

PRICE_UPDATE_SCHEMA = {
    "article_id": {
        "type": str,
        "minLen": 1,
        "maxLen": 60
        },
    "price": {
        "required": True,
        "type": numbers.Real,
        "min": 0
        },
    "min_price": {
        "required": False,
        "type": numbers.Real,
        "min": 0
        },
    "max_price": {
        "required": False,
        "type": numbers.Real,
        "min": 0
        },
    "price_currency": {
        "required": True,
        "type": str,
        "minLen": 1,
        "maxLen": 5
        },
    "state": {
        "required": True,
        "type": str,
        "minLen": 1,
        "maxLen": 50
        },
}


def validateAddPriceParams(params):
    if ("_id" in params):
        raise error.InvalidArgument("_id", "Inválido")

    return schemaValidator.validateAndClean(PRICE_UPDATE_SCHEMA, params)


def validateEditPriceParams(priceId, params):
    if (not priceId):
        raise error.InvalidArgument("_id", "Inválido")

    return schemaValidator.validateAndClean(PRICE_UPDATE_SCHEMA, params)


def validatePriceExist(priceId):
    article = crud.getPrice(priceId)
    if("enabled" not in article or not article["enabled"]):
        raise error.InvalidArgument("_id", "Inválido")
