import datetime

import app.utils.errors as errors
import app.utils.schema_validator as validator

DISCOUNT_DB_SCHEMA = {
    "acceptedPaymentMethod": {
        "required": False,
        "type": str,
        "maxLen": 50
    },
    "addOn": {
        "required": False,
        "type": dict
    },
    "availability": {
        "required": True,
        "type": str,
        "maxLen": 50,
    },
    "availabilityEnds": {

    }

}

def newDiscount():
    """
    Create a new empty Discount
    Return a dict<key, value> Discount
    """

    return {
        "acceptedPaymentMethod": "",
        "addOn": "",
        "availability": "",
        "availabilityEnds": "",
        "availabilityStarts": "",
        "elegibleQuantity": "",
        "elegibleRegion": "",
        "gtin": "",
        "inventoryLevel": "",
        "offeredBy": "",
        "price": ""
    }

def validateSchema(document):
    err = validator.validateSchema(DISCOUNT_DB_SCHEMA, document)

    if(len(err) > 0):
        raise errors.MultipleArgumentException(err)
