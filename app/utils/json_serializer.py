# coding=utf_8

import json
import datetime
import bson.objectid as bson


def json_serial(obj):
    """
    Serializer primites types.
    """
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, bson.ObjectId):
        return str(obj)
    raise TypeError("Type %s not serializable" % type(obj))


def dic_to_json(doc):
    """
    Convert from dictionary to a json string
    doc: dict
    result json
    """
    return json.dumps(doc, default=json_serial)


def body_to_dic(body):
    """
    Convert from json string to a dictionary.
    body: string json
    result dict <ket, value>
    """
    return json.loads(body)
