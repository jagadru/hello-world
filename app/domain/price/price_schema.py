import datetime
import numbers

import app.utils.errors as errors
import app.utils.schema_validator as validator

PRICE_DB_SCHEMA = {
    "id_price": {
        "required": True,
        "type": numbers.Integral,
        "min": 0
    },
    "created": {
        "required": False,
        "type": datetime.datetime,
    },
    "state": {
        "required": True,
        "type": str
    },
    "max_price": {
        "required": False,
        "type": numbers.Real,
        "min": 0
    },
    "min_price": {
        "required": False,
        "type": numbers.Real,
        "min": 0
    },
    "price": {
        "required": True,
        "type": numbers.Real,
    },
    "price_currency": {
        "required": True,
        "type": str,
        "maxLen": 5
    },
    "formated_price": {
        "required": True,
        "type": str,
    },
    "id_article": {
        "required": True,
        "type": numbers.Integral,
        "min": 0
    },
}

def new_price():
    """
    Create a new blank Price.
    Return dict<key, value> Price
    """

    return {
        "price_id": "",
        "created": "",
        "state": "",
        "max_price": 0.0,
        "min_price": 0.0,
        "price": 0.0,
        "price_currency": "",
        "formated_price": "",
        "id_article": ""
    }

def validateSchema(document):
    err = validator.validateSchema(PRICE_DB_SCHEMA, document)

    if (len(err) > 0):
        raise errors.MultipleArgumentException(err)
