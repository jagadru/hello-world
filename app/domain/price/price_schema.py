import datetime
import numbers

import app.utils.errors as errors
import app.utils.schema_validator as validator

PRICE_DB_SCHEMA = {
    "price_id": {
        "required": True,
        "type": numbers.Real,
        "min": 0
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
    "formated_price": {
        "required": True,
        "type": str,
        "minLen": 1,
        "maxLen": 50
        },
    "state": {
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


def new_price():

    return {
        "price_id": 0,
        "price": 0.0,
        "min_price": 0.0,
        "max_price": 0.0,
        "price_currency": '',
        "formated_price": '',
        "created": datetime.datetime.utcnow(),
        "updated": datetime.datetime.utcnow(),
        "state": '',
        "article_id": '',
    }

def validateSchema(document):
    err = validator.validateSchema(ARTICLE_DB_SCHEMA, document)

    if (len(err) > 0):
        raise errors.MultipleArgumentException(err)
