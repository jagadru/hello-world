import numbers

EVENT = {
    "type": {
        "required": True,
        "type": str
    },
    "message": {
        "required": True
    }
}

MSG_ARTICLE_CHANGE = {
    "_id": {
        "required": True,
        },
    "name": {
        "required": True,
        "type": str,
        },
    "price": {
        "required": True,
        "type": numbers.Real,
        },
    "description": {
        "required": True,
        "type": str,
        },
    "image": {
        "required": True,
        "type": str,
        },
    "stock": {
        "required": True,
        "type": numbers.Integral,
        },
    "updated": {
        "required": True,
        "type": str,
        },
    "created": {
        "required": True,
        "type": str,
        },
    "enabled": {
        "required": True,
        },
}

MSG_ARTICLE_EXIST = {
    "articleId": {
        "required": True,
        },
    "referenceId": {
        "required": True,
        },
    "valid": {
        "required": True,
        },
}
