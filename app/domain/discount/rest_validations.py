from numbers import Real
from app.utils import (
    errors,
    schema_validator
)

DISCOUNT_VALID_SCHEMA = {
    "discount_name": {
        "required": True,
        "type": str,
        "minLen": 0,
        "maxLen": 150,
        },
    "discount_value": {
        "required": True,
        "type": Real,
        "min": 0,
        "max": 100
        },
    "discount_code": {
        "required": True,
        "type": str,
        "minLen": 0,
        "maxLen": 20,
        },
    "visibility": {
        "required": True,
        "type": str,
        "minLen": 1,
        "maxLen": 50
        },
    "article_id": {
        "required": True,
        "type": str,
        "minLen": 0
        },
    "state": {
        "required": True,
        "type": str,
        "minLen": 1,
        "maxLen": 50
        },
}

def validateAddDiscountParams(params):
    if ("_id" in params):
        raise errors.InvalidArgument("_id", "Inválido")

    return schema_validator.validateAndClean(DISCOUNT_VALID_SCHEMA, params)


def validateEditDiscountParams(discount_id, params):
    if (not discount_id):
        raise errors.InvalidArgument("_id", "Inválido")

    return schema_validator.validateAndClean(DISCOUNT_VALID_SCHEMA, params)
