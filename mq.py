import pika
import json
import jsonext


def connection_init():
    credentials = pika.PlainCredentials('miffy', 'miffy')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='47.240.41.82', port=5672, credentials=credentials))
    return connection


def connect_and_send(s):
    connection = connection_init()
    channel = connection.channel()
    channel.queue_declare('miffy_queue')
    body = json.dumps(s, cls=jsonext.DateEncoder)
    channel.basic_publish(exchange='', routing_key='miffy_queue', body=body)
    connection.close()
