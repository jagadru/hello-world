# coding=utf_8
import numbers
from app.utils import (
    errors,
    schema_validator
)

PRICE_ADD_SCHEMA = {
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

PRICE_UPDATE_SCHEMA = {
    "article_id": {
        "required": True,
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
        "required": False,
        "type": str,
        "minLen": 1,
        "maxLen": 50
        },
}


def validateAddPriceParams(params):
    if ("_id" in params):
        raise errors.InvalidArgument("_id", "Inválido")

    return schema_validator.validateAndClean(PRICE_ADD_SCHEMA, params)


def validateEditPriceParams(priceId, params):
    if (not priceId):
        raise errors.InvalidArgument("_id", "Inválido")

    return schema_validator.validateAndClean(PRICE_UPDATE_SCHEMA, params)
