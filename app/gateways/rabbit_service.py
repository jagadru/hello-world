import json
import pika
from threading import Thread
from threading import Timer

from app.utils import config

def init():
    t = Thread(target=listen_auth_logout, daemon=True)
    t.start()

def listen_auth_logout():
    try:
        # Establish a connection
        connection = pika.BlockingConnection(pika.ConnectionParameters())
        channel = connection.channel()
    except Exception as e:
        print(e)
        Timer(5.0, init).start()
