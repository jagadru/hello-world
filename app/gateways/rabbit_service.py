import pika
from threading import (
    Thread,
    Timer
)

from app.gateways import EVENT
from app.utils import (
    config,
    security,
    json_serializer,
)

def init():
    """
    Inicializa los servicios Rabbit
    """
    initAuth()
    # initCatalog()

def initAuth():
    authConsumer = Thread(target=listen_auth)
    authConsumer.start()

# def initCatalog():
#     catalogConsumer = Thread(target=listen_auth)
#     catalogConsumer.start()

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

def send_new_price(exchange, queue, type, prices):

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.get_rabbit_server_url())
    )

    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='fanout')
    channel.queue_declare(queue = queue)

    message = {
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
