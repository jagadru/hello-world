from datetime import datetime
from numbers import Real

from app.utils import (
    errors,
    schema_validator
)

DISCOUNT_DB_SCHEMA = {
    "discount_id": {
        "required": True,
        "type": str,
        "minLen": 0
        },
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
}

def new_discount():
    """
    Create a new empty Discount
    Return a dict<key, value> Discount
    """

    return {
        "discount_name": "",
        "discount_value": 0.0,
        "discount_code": "",
        "visibility": "",
        "validFrom": datetime.utcnow(),
        "validTo": datetime.utcnow(),
        "created": datetime.utcnow(),
        "updated": datetime.utcnow(),
        "article_id": '',
    }

def validateSchema(document):
    err = schema_validator.validateSchema(DISCOUNT_DB_SCHEMA, document)

    if(len(err) > 0):
        raise errors.MultipleArgumentException(err)
