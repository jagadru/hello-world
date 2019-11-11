import pika
from threading import (
    Thread,
    Timer
)
from app.domain import ACTIVE
from app.domain.price import crud_price as crud

from app.gateways import (
    EVENT,
    MSG_ARTICLE_CHANGE,
    MSG_ARTICLE_EXIST,
)
from app.utils import (
    config,
    security,
    json_serializer,
    schema_validator as validator
)

def init():
    """
    Inicializa los servicios Rabbit
    """
    initAuth()
    initArticle()
    initCatalog()

def initAuth():
    authConsumer = Thread(target=listen_auth)
    authConsumer.start()

def initArticle():
    catalogConsumer = Thread(target=listen_article)
    catalogConsumer.start()

def initCatalog():
    catalogConsumer = Thread(target=listen_catalog)
    catalogConsumer.start()

def listen_auth():
    """
    Básicamente eventos de logout enviados por auth.

    @api {fanout} auth/logout Logout

    @apiGroup RabbitMQ GET

    @apiDescription Escucha de mensajes logout desde auth. Invalida sesiones en cache.

    @apiExample {json} Mensaje
      {
        "type": "article-exist",
        "message" : "tokenId"
      }
    """
    EXCHANGE = "auth"

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.get_rabbit_server_url())
        )
        channel = connection.channel()

        channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout')

        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=EXCHANGE, queue=queue_name)

        def callback(ch, method, properties, body):
            event = json_serializer.body_to_dic(body.decode('utf-8'))
            if(len(json_serializer.validateSchema(EVENT, event)) > 0):
                return

            if (event["type"] == "logout"):
                security.invalidateSession(event["message"])

        print("RabbitMQ Auth conectado")

        channel.basic_consume(queue_name, callback, auto_ack=True)

        channel.start_consuming()
    except Exception:
        print("RabbitMQ Auth desconectado, intentando reconectar en 10'")
        Timer(10.0, initAuth).start()

def listen_article():
    EXCHANGE = "article"
    QUEUE = "article"

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.get_rabbit_server_url())
        )
        channel = connection.channel()
        channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout')
        result = channel.queue_declare(QUEUE, durable=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=EXCHANGE, queue=queue_name)

        def callback(ch, method, properties, body):
            event = json_serializer.body_to_dic(body.decode('utf-8'))
            if(len(validator.validateSchema(EVENT, event)) > 0):
                return

            if (event["type"] == "article-change"):

                message = event["message"]

                if(len(validator.validateSchema(MSG_ARTICLE_CHANGE, message)) > 0):
                    return

                article_id = message['_id']
                print("RabbitMQ Pricing POST article-change article_id: {}".format(article_id))

                try:
                    price = {}
                    price['max_price'] = message['price']
                    price['min_price'] = message['price']
                    price['price'] = message['price']
                    price['price_currency'] = 'ARS'
                    price['article_id'] = article_id
                    price['state'] = ACTIVE
                    crud._addOrUpdatePrice(price)

                except Exception:
                    print('Cannot handle article-change')

        print("RabbitMQ Article conectado")

        channel.basic_consume(queue_name, callback, auto_ack=True)

        channel.start_consuming()

    except Exception as inst:
        print(inst)
        print("RabbitMQ Article desconectado, intentando reconectar en 10'")
        Timer(10.0, initArticle).start()

def listen_catalog():
    EXCHANGE = "catalog"
    QUEUE = "catalog"

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.get_rabbit_server_url())
        )
        channel = connection.channel()
        channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')
        result = channel.queue_declare(QUEUE, durable=False)
        queue_name = result.method.queue
        channel.queue_bind(exchange=EXCHANGE, queue=queue_name)

        def callback(ch, method, properties, body):
            event = json_serializer.body_to_dic(body.decode('utf-8'))
            if(len(validator.validateSchema(EVENT, event)) > 0):
                return

            if (event["type"] == "article-exist"):
                message = event.get('message')

                if(len(validator.validateSchema(MSG_ARTICLE_EXIST, message)) > 0):
                    return

                article_id = message.get('articleId')
                print("RabbitMQ Catalog POST article-exist article_id: {}".format(article_id))

                try:
                    if not message['valid']:
                        crud.del_price(article_id)

                except Exception:
                    print('Cannot handle article-exist')

        print("RabbitMQ Catalog conectado")

        channel.basic_consume(queue_name, callback, auto_ack=True)

        channel.start_consuming()
    except Exception as inst:
        print(inst)
        print("RabbitMQ Catalog desconectado, intentando reconectar en 10'")
        Timer(10.0, initCatalog).start()

def send_new_price(exchange, queue, type, prices):

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.get_rabbit_server_url())
    )

    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='fanout')
    channel.queue_declare(queue = queue)

    message = {
        "exchange": exchange,
        "queue": queue,
        "type": type,
        "message": prices
    }

    channel.basic_publish(
        exchange=exchange,
        routing_key=queue,
        body=json_serializer.dic_to_json(message)
    )

    connection.close()

def send_new_discount(exchange, queue, type, discounts):

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.get_rabbit_server_url()))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type='fanout')
    channel.queue_declare(queue = queue)

    message = {
        "type": type,
        "message": discounts
    }

    channel.basic_publish(
        exchange=exchange,
        routing_key=queue,
        body=json_serializer.dic_to_json(message)
    )

    connection.close()

def send_is_article_valid(exchange, queue, type, price):

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.get_rabbit_server_url())
    )

    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='direct')
    channel.queue_declare(queue = queue)

    article = {}
    article["articleId"] = price["article_id"]
    article["referenceId"] = price["_id"]

    message = {
        "exchange": exchange,
        "queue": queue,
        "type": type,
        "message": article
    }

    channel.basic_publish(
        exchange=exchange,
        routing_key=queue,
        body=json_serializer.dic_to_json(message)
    )
    print("RabbitMQ Catalog GET article-exist catalogId: {}, articleId: {}".format(article["referenceId"], article["articleId"]))
    connection.close()
